# Zenia SEO Operating System — Architecture

3 agentes Python autónomos que corren weekly via GitHub Actions cron, alimentados por Google Search Console + Anthropic API, comunicándose vía artefactos JSON en `reports/seo/cache/`.

---

## Flow weekly

```
SUNDAY 22:00 UTC
+------------------------------------------------------------+
| AGENT: performance                                         |
| - GSC API: 7d curr + 7d prev (queries + pages dimensions)  |
| - Compute: top clicks, gainers, losers, new/lost, anomalies|
| - Claude Haiku: 5 insights priorizados (~$0.05)            |
| - Write: reports/seo/weekly/YYYY-MM-DD-performance.html    |
| - Write: reports/seo/cache/weekly_report.json  <--- shared |
| - Email: fabrizzio.zelada@zeniapartners.com                |
+------------------------------------------------------------+
                            |
                            v (consumed by next 2 agents)
                  weekly_report.json
                            |
        +-------------------+--------------------+
        |                                        |
        v                                        v
MONDAY 08:00 UTC                          MONDAY 09:00 UTC
+--------------------------------+   +---------------------------------+
| AGENT: optimizer               |   | AGENT: strategist               |
| - Read weekly_report.json      |   | - Read weekly_report.json       |
| - GSC: query+page pairs        |   | - GSC: queries + pages + pairs  |
| - Filter: pos 5-15, >50 imp    |   | - Compute: gaps, refreshes      |
| - Fetch each URL (HTTP GET)    |   | - Read seo/LONG-TAIL-KEYWORDS   |
| - Parse: title/meta/H1/H2/p1   |   | - List blog/*.html slugs        |
| - Claude Sonnet x N: 3 fixes   |   | - Claude Sonnet: weekly plan    |
|   per URL (~$0.50-1.00)        |   |   (~$0.30)                      |
| - Write: optimizer.html        |   | - Update content-tracker.json   |
| - Email: top 5 quick wins      |   | - Write: strategy.html          |
|                                |   | - Email: plan with focus        |
| REPORT-ONLY (no file mutations)|   | MUTATES content-tracker.json    |
+--------------------------------+   +---------------------------------+
                                                      |
                                                      v
                                          blog/content-tracker.json
                                                      |
                                                      v
                                       (existing) "Zenia SEO Daily" routine
                                       3x/day publishes pending posts
```

---

## Lifecycle de un post nuevo

1. **Lunes** — Strategist detecta gap, añade post a `content-tracker.json` con `status: pending`
2. **Mar-Sab** — Routine "Zenia SEO Daily" (3x/día) recoge un pending y lo escribe + commitea
3. **Domingo** — Performance mide impresiones/clicks del nuevo post W
4. **Lunes siguiente** — Optimizer puede sugerir fixes, Strategist evalúa para refresh
5. **Loop continuo**

---

## Interacciones con sistemas existentes

### Lo que ya tiene Zenia (no toco)
- `backend/server.js` (Render): API publica, no afectado
- `.github/workflows/seo-weekly-report.yml`: report node.js distinto, mantenerlo o deprecar
- `.github/workflows/seo-boost.yml`: indexing API + internal linking on push
- `.github/workflows/seo-health.yml`: lighthouse cron
- Routine "Zenia SEO Daily": consume `content-tracker.json`, no toco

### Lo nuevo se integra via
- **Read**: `seo/LONG-TAIL-KEYWORDS.md`, `blog/*.html` filenames
- **Write**: `blog/content-tracker.json` (append nuevos posts pending)
- **Write**: `reports/seo/{weekly,optimizer,strategy,cache}/`

### Decisión: OAuth user creds vs Service Account
Repo ya usa `GSC_SERVICE_ACCOUNT_JSON` en otros workflows. Este sistema usa **OAuth user credentials** (más permisos, más fácil setup interactivo via `setup_gsc_oauth.py`). Ambos pueden coexistir sin conflicto.

Si quieres unificar a service account, hay que:
1. Compartir el GSC site con el service account email
2. Cambiar `gsc_client.authenticate()` para usar `from google.oauth2 import service_account`
3. Reemplazar secret `GSC_TOKEN_JSON` por `GSC_SERVICE_ACCOUNT_JSON`

---

## Cost model

| Item | Modelo / unidad | $/run | Runs/mes | $/mes |
|---|---|---|---|---|
| Performance Claude | Haiku 4.5 (1 call, ~3K input + 1K output) | $0.05 | 4 | $0.20 |
| Optimizer Claude | Sonnet 4.5 (15-25 calls, ~2K in + 1K out each) | $0.75 | 4 | $3.00 |
| Strategist Claude | Sonnet 4.5 (1 call, ~8K in + 3K out) | $0.30 | 4 | $1.20 |
| GSC API | free | $0 | — | $0 |
| Resend | free tier | $0 | — | $0 |
| Actions minutes | ~15min/run × 3 = 45/sem | free | — | $0 |
| **Total** | | | | **~$4.40/mes** |

Si el optimizer escala a 50 URLs (más tráfico): ~$1.50/run = $6/mes optimizer solo. Total budget cap razonable: **$10/mes**.

---

## Idempotency

Cada agente escribe lock file en `reports/seo/cache/{agent}.lock.json` con timestamp.
Si vuelve a correr dentro de 12h, hace skip (evita emails duplicados en retries de Actions).
Bypass con flag `--force` (usado siempre en CI para que el cron no quede bloqueado por un run anterior).

---

## Rate limits

- **GSC API**: 1.200 queries/min/proyecto. `gsc_client.py` mete 250ms sleep entre paginated calls. Daily quota 50K queries/proyecto.
- **Anthropic Tier 2**: 50 req/min. Optimizer hace 15-25 calls secuenciales (2-4min wall time, dentro del límite).
- **Resend**: 100 emails/day free. Usamos 3 emails/semana → trivial.

---

## Failure modes y mitigación

| Failure | Detection | Mitigación |
|---|---|---|
| GSC token expired | `gsc_client.authenticate()` raise | Re-correr `setup_gsc_oauth.py`, update secrets |
| Anthropic 429 / 5xx | retry+backoff in `lib.call_anthropic` | hasta 3 reintentos exponential |
| Resend 4xx | retry+backoff in `lib.send_email` | hasta 3 reintentos |
| URL fetch timeout (Optimizer) | `_fetch_page` returns `{"error": ...}` | proposal vacío para esa URL, otras procesan |
| Sonnet returns invalid JSON | try/except en parser | fixes vacíos para esa URL, sigue |
| GitHub Actions cron miss | (silent — feedback_infra_unreliability) | manual `workflow_dispatch` fallback |
| Push race con otros workflows | git pull --rebase + retry x3 | en step "Commit reports" |

---

## Extensiones futuras

Cosas que NO está aún pero serían siguientes pasos:

- **Auto-apply fixes**: optimizer crea PR con cambios en lugar de report-only
- **Backlink monitoring**: nuevo agente `agent_backlinks` con Ahrefs API
- **Competitor delta**: comparar GSC con scraping competidores top
- **Slack notifications**: ya hay infra Resend, agregar webhook Slack opcional
- **Pillar refresh playbook**: detectar pillar pages estancadas y disparar refresh agresivo

---

## Estructura de archivos

```
zenia-website/
├── scripts/seo/
│   ├── __init__.py
│   ├── lib.py                   # shared: Anthropic, Resend, HTML, logging, locks
│   ├── gsc_client.py            # GSC API wrapper + cache
│   ├── agent_performance.py     # weekly digest
│   ├── agent_optimizer.py       # quick wins pos 5-15
│   ├── agent_strategist.py      # plan + tracker updates
│   ├── setup_gsc_oauth.py       # one-time OAuth helper
│   └── requirements.txt
├── reports/seo/
│   ├── weekly/                  # YYYY-MM-DD-performance.html
│   ├── optimizer/               # YYYY-MM-DD-optimizer.html
│   ├── strategy/                # YYYY-MM-DD-strategy.html
│   └── cache/                   # weekly_report.json + locks
├── seo/
│   ├── AGENTS-SETUP.md          # OAuth setup guide
│   ├── ARCHITECTURE.md          # this file
│   ├── CLUSTER-TOPOLOGY.md      # (existing)
│   └── LONG-TAIL-KEYWORDS.md    # (existing, consumed by strategist)
├── .github/workflows/
│   └── seo-agents.yml           # cron Sun 22 UTC + Mon 08/09 UTC
└── blog/
    └── content-tracker.json     # mutated by strategist
```
