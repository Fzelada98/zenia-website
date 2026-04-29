# Zenia SEO Operating System — Setup Guide

Sistema autónomo de 3 agentes que corre weekly via GitHub Actions y mejora SEO continuamente.

- **Performance** (Sun 22:00 UTC): GSC weekly digest + email
- **Optimizer** (Mon 08:00 UTC): quick-win proposals para URLs en pos 5-15
- **Strategist** (Mon 09:00 UTC): plan semanal + actualiza `content-tracker.json`

Setup one-time. Después corre solo.

---

## 1. Crear proyecto en Google Cloud Console

1. Abrir https://console.cloud.google.com/
2. Click selector de proyecto (top-left) → **New Project**
3. Nombre: `zenia-seo` · Org: dejar en blanco · Click **Create**
4. Esperar ~30s a que se cree, seleccionarlo

## 2. Habilitar Search Console API

1. Menu hamburguesa → **APIs & Services** → **Library**
2. Buscar "Search Console API"
3. Click resultado → **Enable**

## 3. Configurar OAuth consent screen

1. **APIs & Services** → **OAuth consent screen**
2. User Type: **External** → Create
3. App information:
   - App name: `Zenia SEO Bot`
   - User support email: `zeladauriartef@gmail.com`
   - Developer contact: `zeladauriartef@gmail.com`
4. Scopes: skip (los pide el script)
5. Test users: añadir `zeladauriartef@gmail.com` (la cuenta dueña de Search Console)
6. Save & Continue → Back to Dashboard
7. Status: **Testing** (suficiente, no necesitas verificación de Google)

## 4. Crear OAuth Client ID

1. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
2. Application type: **Desktop app**
3. Name: `Zenia SEO Desktop`
4. **Create** → descargar el JSON (boton de download junto al client ID creado)
5. Mover el archivo descargado a:
   ```
   c:\Users\Usuario\AI\zenia-website\backend\client_secret.json
   ```
   (puedes renombrarlo o dejarlo como `client_secret_xxxxx.apps.googleusercontent.com.json`)

## 5. Instalar dependencias Python

```bash
cd c:\Users\Usuario\AI\zenia-website
pip install -r scripts/seo/requirements.txt
```

## 6. Correr OAuth setup script

```bash
cd c:\Users\Usuario\AI\zenia-website
python -m scripts.seo.setup_gsc_oauth
```

Va a:
1. Pedirte path al `client_secret.json` (Enter usa el default `backend/client_secret.json`)
2. Abrir browser → login con `zeladauriartef@gmail.com` → Allow
3. Guardar `backend/token.json`
4. Hacer test query a la API
5. Imprimir 2 strings base64: uno para `GSC_TOKEN_JSON`, otro para `GSC_CREDENTIALS_JSON`

**Copia ambos strings completos** — los necesitas en el siguiente paso.

## 7. Agregar GitHub Secrets

Ir a https://github.com/<TU-USER>/zenia-website/settings/secrets/actions

Crear (o verificar si ya existen):

| Secret name | Value | Notas |
|---|---|---|
| `ANTHROPIC_API_KEY` | (ya existe) | usado por backend tambien |
| `RESEND_API_KEY` | (ya existe) | usado por backend tambien |
| `GSC_TOKEN_JSON` | base64 string del paso 6 | NUEVO |
| `GSC_CREDENTIALS_JSON` | base64 string del paso 6 | NUEVO |

## 8. Test end-to-end manual

1. Ir a **Actions** → **SEO Agents Weekly Cycle**
2. Click **Run workflow** → seleccionar agent: `performance`
3. Esperar ~3-5 min
4. Verificar:
   - Email llega a `fabrizzio.zelada@zeniapartners.com` con asunto `[Zenia SEO] Performance Weekly — YYYY-MM-DD`
   - Commit nuevo en main: `seo(performance): weekly run YYYY-MM-DD`
   - Archivo creado: `reports/seo/weekly/YYYY-MM-DD-performance.html`
5. Repetir con `optimizer` y `strategist`

## 9. Verificar que el cron está activo

En **Actions**, debes ver el workflow "SEO Agents Weekly Cycle" listado. La primera ejecución automática será el próximo domingo 22:00 UTC.

Útil: el indicador de cron en GitHub Actions tarde a veces 5-15 min en disparar (es normal).

---

## Troubleshooting

### Error: `No GSC token found`
Falta `GSC_TOKEN_JSON` en secrets, o está mal pegado. Re-ejecutar paso 6, copiar string completo (sin saltos de línea).

### Error: `Refresh token expired`
Si pasan 6 meses sin uso o cambias contraseña Google, el refresh token expira. Re-correr `setup_gsc_oauth.py` y regenerar secrets.

### Error: `permission denied` para zeniapartners.com
La cuenta Google que autenticaste no tiene acceso a la propiedad GSC. Ir a https://search.google.com/search-console → settings → users → añadir como Owner.

### Email no llega
1. Check spam folder
2. Verificar que dominio `zeniapartners.com` está verified en Resend (DKIM+SPF). Si no, los emails se rechazan silenciosamente.
3. Check logs de Actions run.

### Workflow no dispara automáticamente
GitHub Actions schedules pueden retrasarse hasta 1 hora durante alta carga, o saltearse si el repo está inactivo. Ver `feedback_infra_unreliability.md` — considerar fallback manual via `workflow_dispatch` si crítico.

---

## Costes estimados

| Agent | Modelo | Llamadas/run | Cost/run | Cost/mes |
|---|---|---|---|---|
| Performance | Haiku 4.5 | 1 | ~$0.05 | ~$0.20 |
| Optimizer | Sonnet 4.5 | 10-25 | ~$0.50-1.00 | ~$3-4 |
| Strategist | Sonnet 4.5 | 1 (long context) | ~$0.30 | ~$1.30 |
| **Total** | | | | **~$5/mes** |

GSC API: free (within rate limits). Resend: incluido en free tier (3K emails/mes).
GitHub Actions minutos: ~15min/semana = 60min/mes (free tier 2000min).

---

## Ver tambien

- `seo/ARCHITECTURE.md` — flow + interaccion entre agentes
- `scripts/seo/` — código fuente
- `.github/workflows/seo-agents.yml` — cron schedule
