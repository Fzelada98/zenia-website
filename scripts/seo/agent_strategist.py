"""Agent: Strategist — weekly content plan + content-tracker updates.

Runs Monday 09:00 UTC. Reads weekly snapshot + GSC data + existing posts
+ long-tail keyword backlog. Asks Sonnet for: 3 NEW posts, 3 REFRESH
candidates, 3 priority keywords for the week. Updates blog/content-tracker.json
so the existing "Zenia SEO Daily" routine picks them up automatically.

Output: reports/seo/strategy/YYYY-MM-DD-strategy.html
Output: blog/content-tracker.json (updated)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any

from .gsc_client import get_query_page_pairs, get_top_pages, get_top_queries
from .lib import (
    BLOG_DIR,
    CACHE_DIR,
    DEFAULT_TO_EMAIL,
    REPORTS_DIR,
    SEO_DIR,
    acquire_run_lock,
    call_anthropic,
    list_blog_posts,
    load_env,
    log,
    now_date,
    read_json,
    render_html_report,
    send_email,
    write_json,
    write_run_lock,
    write_text,
)


# ---------------------------------------------------------------------------
# Gap analysis
# ---------------------------------------------------------------------------
def _identify_gaps(
    queries: list[dict[str, Any]],
    pairs: list[dict[str, Any]],
    *,
    min_impressions: int = 100,
    pos_threshold: float = 30.0,
) -> list[dict[str, Any]]:
    """Queries with high impressions but no Zenia URL ranking top 30."""
    by_query: dict[str, dict[str, Any]] = {}
    for r in pairs:
        q = r.get("query")
        if not q:
            continue
        if q not in by_query or r["position"] < by_query[q]["best_position"]:
            by_query[q] = {
                "query": q,
                "best_position": r["position"],
                "impressions": r.get("impressions", 0),
            }

    gaps = []
    for r in queries:
        q = r.get("query")
        if not q or r["impressions"] < min_impressions:
            continue
        best = by_query.get(q, {}).get("best_position", 100)
        if best > pos_threshold:
            gaps.append(
                {
                    "query": q,
                    "impressions": r["impressions"],
                    "best_position": round(best, 1),
                    "clicks": r.get("clicks", 0),
                }
            )
    gaps.sort(key=lambda x: x["impressions"], reverse=True)
    return gaps[:20]


def _identify_refresh_candidates(
    pages_curr: list[dict[str, Any]], previous_snapshot: dict[str, Any] | None
) -> list[dict[str, Any]]:
    """Pages with traffic but stagnant or losing, OR > 6 months old."""
    six_months_seconds = 6 * 30 * 24 * 3600
    now = datetime.now(timezone.utc).timestamp()
    candidates = []

    for r in pages_curr:
        page = r.get("page", "")
        if "/blog/" not in page:
            continue
        slug = page.rstrip("/").split("/")[-1]
        local_path = BLOG_DIR / slug
        age_days = None
        if local_path.exists():
            try:
                mtime = local_path.stat().st_mtime
                age_days = (now - mtime) / 86400
            except OSError:
                pass

        # Stagnant traffic or old + decent impressions
        if r.get("impressions", 0) < 100:
            continue

        reasons = []
        if age_days and age_days > 180:
            reasons.append(f"sin actualizar {int(age_days)}d")
        if r.get("position", 0) > 8 and r.get("impressions", 0) > 200:
            reasons.append(f"estancado pos {r['position']:.1f} con {r['impressions']:,} imp")

        if reasons:
            candidates.append(
                {
                    "page": page,
                    "slug": slug.replace(".html", ""),
                    "impressions": r["impressions"],
                    "clicks": r["clicks"],
                    "position": round(r["position"], 1),
                    "age_days": int(age_days) if age_days else None,
                    "reasons": reasons,
                }
            )

    candidates.sort(key=lambda x: x["impressions"], reverse=True)
    return candidates[:15]


# ---------------------------------------------------------------------------
# Inputs assembly
# ---------------------------------------------------------------------------
def _load_long_tail_keywords() -> str:
    path = SEO_DIR / "LONG-TAIL-KEYWORDS.md"
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")[:8000]  # cap to keep prompt bounded
    except OSError:
        return ""


def _load_existing_slugs() -> list[str]:
    return [f.replace(".html", "") for f in list_blog_posts()]


def _load_weekly_snapshot() -> dict[str, Any] | None:
    return read_json(CACHE_DIR / "weekly_report.json")


# ---------------------------------------------------------------------------
# Claude planner
# ---------------------------------------------------------------------------
def _build_plan(context: dict[str, Any]) -> dict[str, Any]:
    """Ask Sonnet for the weekly content plan."""
    prompt = f"""Eres SEO content strategist senior de Zenia Partners.

Zenia: agencia AI+CRM+WhatsApp para SMBs. Verticales: gimnasios, estetica, restaurantes, ecommerce.
Mercados: España (principal), Peru, LATAM, USA. Idioma blog: español (long-tail SEO).

ESTADO ACTUAL:
- Blog tiene {context['existing_count']} posts publicados.
- 4 pillar pages live: /blog/crm-para-{{gimnasios,estetica,restaurantes,ecommerce}}-espana-2026.html
- Esta semana: {context['totals']['clicks']} clicks, {context['totals']['impressions']} impresiones, pos media {context['totals']['position']:.1f}

CONTENT GAPS (queries con impresiones pero ninguna URL Zenia en top 30):
{json.dumps(context['gaps'][:15], indent=2, ensure_ascii=False)}

CANDIDATOS A REFRESH (posts con trafico pero estancados u obsoletos):
{json.dumps(context['refresh_candidates'][:10], indent=2, ensure_ascii=False)}

INSIGHTS WEEKLY (del agente performance):
{json.dumps(context.get('insights', []), indent=2, ensure_ascii=False)}

LONG-TAIL KEYWORDS BACKLOG (extracto):
{context['long_tail_excerpt'][:3500]}

POSTS EXISTENTES (slugs, evita duplicar):
{json.dumps(context['existing_slugs'][:50], indent=2, ensure_ascii=False)}

TU TAREA: genera plan semanal en JSON estricto:

{{
  "new_posts": [
    {{
      "slug": "kebab-case-slug",
      "title": "Title H1 sugerido (50-60 chars)",
      "keyword_target": "keyword principal",
      "secondary_keywords": ["k1", "k2"],
      "cluster": "gimnasios|estetica|restaurantes|ecommerce",
      "tier": 1,
      "outline": ["H2 seccion 1", "H2 seccion 2", ...],
      "rationale": "por que este post (gap, volumen, intent)"
    }},
    ... (3 posts)
  ],
  "refreshes": [
    {{
      "slug": "slug-existente",
      "changes": ["cambio 1", "cambio 2", "cambio 3"],
      "rationale": "..."
    }},
    ... (3 refreshes)
  ],
  "priority_keywords": [
    {{"keyword": "...", "rationale": "..."}},
    ... (3 keywords)
  ],
  "weekly_focus": "una frase con el foco estrategico de la semana"
}}

Reglas:
- new_posts: priorizar gaps con > 200 impresiones. NO duplicar slugs existentes.
- Cluster correcto, tier 1 si keyword volumen >100, tier 2 si <100.
- refreshes: pick los 3 con mayor ROI (trafico actual + facilidad de mejora).
- priority_keywords: las 3 mas estrategicas para atacar via outreach/links/etc esta semana.
- Tono Zenia: directo, anti-fluff, español neutro (NO mexicanismos).

Responde SOLO el JSON."""

    try:
        resp = call_anthropic(
            messages=[{"role": "user", "content": prompt}],
            model="claude-sonnet-4-5",
            max_tokens=3500,
            temperature=0.5,
        )
        start = resp.find("{")
        end = resp.rfind("}")
        if start >= 0 and end > start:
            return json.loads(resp[start : end + 1])
    except Exception as exc:
        log("error", "claude_plan_failed", error=str(exc))

    return {"new_posts": [], "refreshes": [], "priority_keywords": [], "weekly_focus": ""}


# ---------------------------------------------------------------------------
# Content tracker updates
# ---------------------------------------------------------------------------
def _update_content_tracker(plan: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    """Append new_posts to blog/content-tracker.json with status='pending'."""
    tracker_path = BLOG_DIR / "content-tracker.json"
    tracker = read_json(tracker_path, default={"posts": []}) or {"posts": []}
    existing_slugs = {p.get("slug") for p in tracker.get("posts", [])}

    added = []
    for np in plan.get("new_posts", []):
        slug = np.get("slug", "").strip()
        if not slug or slug in existing_slugs:
            continue
        entry = {
            "slug": slug,
            "title": np.get("title", ""),
            "keyword": np.get("keyword_target", ""),
            "secondary_keywords": np.get("secondary_keywords", []),
            "outline": np.get("outline", []),
            "cluster": np.get("cluster", ""),
            "tier": np.get("tier", 2),
            "status": "pending",
            "source": "strategist-agent",
            "added": now_date(),
        }
        tracker["posts"].append(entry)
        added.append(entry)

    tracker["lastRun"] = datetime.now(timezone.utc).isoformat()
    tracker["lastStrategistRun"] = datetime.now(timezone.utc).isoformat()

    if not dry_run and added:
        write_json(tracker_path, tracker)
        log("info", "tracker_updated", added=len(added), slugs=[a["slug"] for a in added])

    return {"added": added, "total_posts": len(tracker["posts"])}


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------
def _render_focus(focus: str) -> str:
    if not focus:
        return ""
    return f"""<div class="callout success">
<strong>Foco semanal:</strong> {focus}
</div>"""


def _render_new_posts(posts: list[dict[str, Any]]) -> str:
    if not posts:
        return "<h2>Posts nuevos a escribir</h2><p style='color:#94A3B8'>Sin propuestas esta semana.</p>"
    items = []
    for i, p in enumerate(posts, 1):
        outline = "".join(f"<li>{h}</li>" for h in p.get("outline", []))
        secondary = ", ".join(p.get("secondary_keywords", []))
        items.append(
            f"""<div style="background:white;border:1px solid #E2E8F0;border-radius:8px;padding:16px;margin:12px 0">
<h3 style="margin-top:0">#{i} <span class="tag new">{p.get('cluster', '')}</span> {p.get('title', '')}</h3>
<p><code>{p.get('slug', '')}</code> · keyword: <strong>{p.get('keyword_target', '')}</strong> · tier {p.get('tier', 2)}</p>
{f"<p><small>Secondary: {secondary}</small></p>" if secondary else ""}
<details><summary style="cursor:pointer;color:#3B82F6">Outline ({len(p.get('outline', []))} secciones)</summary>
<ol>{outline}</ol></details>
<p style="color:#64748B"><em>{p.get('rationale', '')}</em></p>
</div>"""
        )
    return f"<h2>Posts nuevos a escribir esta semana</h2>{''.join(items)}"


def _render_refreshes(refs: list[dict[str, Any]]) -> str:
    if not refs:
        return "<h2>Posts a refrescar</h2><p style='color:#94A3B8'>Ninguno.</p>"
    items = []
    for i, r in enumerate(refs, 1):
        changes = "".join(f"<li>{c}</li>" for c in r.get("changes", []))
        items.append(
            f"""<div style="background:white;border:1px solid #E2E8F0;border-radius:8px;padding:16px;margin:12px 0">
<h3 style="margin-top:0">#{i} <span class="tag refresh">refresh</span> {r.get('slug', '')}</h3>
<ol>{changes}</ol>
<p style="color:#64748B"><em>{r.get('rationale', '')}</em></p>
</div>"""
        )
    return f"<h2>Posts existentes a refrescar</h2>{''.join(items)}"


def _render_priority_keywords(kws: list[dict[str, Any]]) -> str:
    if not kws:
        return ""
    body = []
    for k in kws:
        body.append(
            f"<tr><td><strong>{k.get('keyword', '')}</strong></td><td>{k.get('rationale', '')}</td></tr>"
        )
    return f"""<h2>Keywords prioritarias semana</h2>
<table><thead><tr><th>Keyword</th><th>Por que</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""


def _render_gaps(gaps: list[dict[str, Any]]) -> str:
    if not gaps:
        return ""
    body = []
    for g in gaps[:10]:
        body.append(
            f"<tr><td>{g['query']}</td><td class='num'>{g['impressions']:,}</td><td class='num'>{g['best_position']}</td></tr>"
        )
    return f"""<h2>Content gaps detectados (top 10)</h2>
<p style="color:#64748B">Queries con buenas impresiones pero ninguna URL Zenia en top 30. Oportunidades de post nuevo o link interno agresivo.</p>
<table><thead><tr><th>Query</th><th>Impresiones</th><th>Mejor pos.</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""


def _render_tracker_update(update: dict[str, Any]) -> str:
    added = update.get("added", [])
    if not added:
        return ""
    items = "".join(f"<li><code>{a['slug']}</code> — {a['title']}</li>" for a in added)
    return f"""<div class="callout success">
<strong>{len(added)} posts añadidos a content-tracker.json</strong> (status: pending). La routine
"Zenia SEO Daily" los recogera y publicara en su proximo run 3x/dia.
<ul>{items}</ul>
</div>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run(*, days: int = 7, send: bool = True, dry_run: bool = False, force: bool = False) -> dict[str, Any]:
    load_env()

    if not force and not acquire_run_lock("strategist"):
        log("info", "strategist_skipped_locked")
        return {"skipped": True}

    log("info", "strategist_start", days=days, dry_run=dry_run)

    # 1. Pull GSC + existing data
    queries = get_top_queries(days=days, row_limit=500)
    pages_curr = get_top_pages(days=days, row_limit=300)
    pairs = get_query_page_pairs(days=days, row_limit=2000)

    # 2. Identify opportunities
    gaps = _identify_gaps(queries, pairs)
    refresh_candidates = _identify_refresh_candidates(pages_curr, _load_weekly_snapshot())

    # 3. Build context
    weekly = _load_weekly_snapshot() or {}
    totals = weekly.get("totals_curr") or {
        "clicks": sum(q["clicks"] for q in queries),
        "impressions": sum(q["impressions"] for q in queries),
        "position": (
            sum(q["position"] * q["impressions"] for q in queries)
            / max(sum(q["impressions"] for q in queries), 1)
        ),
    }

    context = {
        "existing_count": len(list_blog_posts()),
        "existing_slugs": _load_existing_slugs(),
        "totals": totals,
        "gaps": gaps,
        "refresh_candidates": refresh_candidates,
        "insights": weekly.get("insights", []),
        "long_tail_excerpt": _load_long_tail_keywords(),
    }

    # 4. Plan via Sonnet
    plan = _build_plan(context)
    log(
        "info",
        "plan_generated",
        new=len(plan.get("new_posts", [])),
        refresh=len(plan.get("refreshes", [])),
        priority_kw=len(plan.get("priority_keywords", [])),
    )

    # 5. Update content-tracker
    tracker_update = _update_content_tracker(plan, dry_run=dry_run)

    # 6. Render HTML report
    body_parts = [
        _render_focus(plan.get("weekly_focus", "")),
        _render_tracker_update(tracker_update),
        _render_new_posts(plan.get("new_posts", [])),
        _render_refreshes(plan.get("refreshes", [])),
        _render_priority_keywords(plan.get("priority_keywords", [])),
        _render_gaps(gaps),
    ]
    html = render_html_report(
        title="Zenia SEO — Strategy Weekly",
        subtitle=f"Plan de contenido · {len(plan.get('new_posts', []))} nuevos · {len(plan.get('refreshes', []))} refresh",
        body_html="\n".join(body_parts),
    )
    report_path = REPORTS_DIR / "strategy" / f"{now_date()}-strategy.html"
    write_text(report_path, html)

    # Save snapshot
    cache_path = CACHE_DIR / "strategy_plan.json"
    cache_path.write_text(
        json.dumps({"plan": plan, "context": {k: v for k, v in context.items() if k != "long_tail_excerpt"}}, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    log("info", "strategy_report_saved", path=str(report_path))

    # 7. Email
    if send:
        email_body = "\n".join(
            [
                _render_focus(plan.get("weekly_focus", "")),
                _render_tracker_update(tracker_update),
                _render_new_posts(plan.get("new_posts", [])),
                _render_refreshes(plan.get("refreshes", [])),
                _render_priority_keywords(plan.get("priority_keywords", [])),
            ]
        )
        email_html = render_html_report(
            title="Strategy Weekly",
            subtitle="Plan de contenido Zenia",
            body_html=email_body
            + f"""<div class="callout success">
<strong>Reporte completo:</strong> <code>reports/seo/strategy/{now_date()}-strategy.html</code>
</div>""",
        )
        try:
            send_email(
                to=DEFAULT_TO_EMAIL,
                subject=f"[Zenia SEO] Strategy Weekly — {now_date()}",
                html=email_html,
            )
        except Exception as exc:
            log("error", "email_failed", error=str(exc))

    write_run_lock("strategist")
    log("info", "strategist_done")
    return {"plan": plan, "tracker_update": tracker_update}


def main() -> int:
    parser = argparse.ArgumentParser(description="Zenia SEO Strategist Agent")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--no-send", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to content-tracker")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    try:
        run(days=args.days, send=not args.no_send, dry_run=args.dry_run, force=args.force)
        return 0
    except Exception as exc:
        log("error", "strategist_fatal", error=str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
