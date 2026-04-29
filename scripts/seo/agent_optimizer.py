"""Agent: Optimizer — quick-win proposals for URLs in position 5-15.

Runs Monday 08:00 UTC. Reads previous Sunday's weekly snapshot, pulls
GSC query+page data to identify URLs ranking 5-15 with >50 impressions
("almost ranking" zone), fetches each URL's HTML, asks Sonnet for
3 specific actionable fixes (title/meta/content/links).

Report-only — does NOT modify files. Fabrizzio applies manually.

Output: reports/seo/optimizer/YYYY-MM-DD-optimizer.html
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.parse import urlparse

import requests

from .gsc_client import get_query_page_pairs
from .lib import (
    CACHE_DIR,
    DEFAULT_TO_EMAIL,
    REPORTS_DIR,
    acquire_run_lock,
    call_anthropic,
    load_env,
    log,
    now_date,
    render_html_report,
    send_email,
    write_run_lock,
    write_text,
)


# ---------------------------------------------------------------------------
# Candidate selection
# ---------------------------------------------------------------------------
def _select_candidates(
    pairs: list[dict[str, Any]],
    *,
    pos_min: float = 5.0,
    pos_max: float = 15.0,
    min_impressions: int = 50,
    max_urls: int = 25,
) -> list[dict[str, Any]]:
    """Pick top opportunities: best query per URL in 5-15 zone."""
    by_url: dict[str, dict[str, Any]] = {}
    for r in pairs:
        url = r.get("page")
        q = r.get("query")
        if not url or not q:
            continue
        if r["position"] < pos_min or r["position"] > pos_max:
            continue
        if r["impressions"] < min_impressions:
            continue
        existing = by_url.get(url)
        # Prefer the query with most impressions for each URL
        if not existing or r["impressions"] > existing["impressions"]:
            by_url[url] = {
                "url": url,
                "query": q,
                "position": round(r["position"], 1),
                "impressions": r["impressions"],
                "clicks": r["clicks"],
                "ctr": round(r["ctr"] * 100, 2),
            }

    candidates = sorted(by_url.values(), key=lambda x: x["impressions"], reverse=True)
    return candidates[:max_urls]


# ---------------------------------------------------------------------------
# Page fetching + parsing
# ---------------------------------------------------------------------------
def _fetch_page(url: str, *, timeout: int = 15) -> dict[str, str]:
    """Fetch URL and extract title, meta description, H1, first H2s, first paragraph."""
    try:
        from bs4 import BeautifulSoup  # type: ignore
    except ImportError:
        log("error", "bs4_missing")
        return {"error": "beautifulsoup4 not installed"}

    try:
        resp = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ZeniaSEOBot/1.0)"},
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        log("warning", "fetch_failed", url=url, error=str(exc))
        return {"error": str(exc), "url": url}

    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    h1 = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1 = h1_tag.get_text(strip=True)

    h2s = [h.get_text(strip=True) for h in soup.find_all("h2")[:8]]

    first_para = ""
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 80:
            first_para = text[:400]
            break

    word_count = len(soup.get_text().split())

    return {
        "url": url,
        "title": title,
        "title_length": len(title),
        "meta_description": meta_desc,
        "meta_length": len(meta_desc),
        "h1": h1,
        "h2s": h2s,
        "first_paragraph": first_para,
        "word_count": word_count,
    }


# ---------------------------------------------------------------------------
# Claude proposal
# ---------------------------------------------------------------------------
def _propose_fixes(candidate: dict[str, Any], page: dict[str, Any]) -> dict[str, Any]:
    """Ask Sonnet for 3 specific actionable fixes per URL."""
    if "error" in page:
        return {"url": candidate["url"], "error": page["error"], "fixes": []}

    prompt = f"""Eres SEO consultant senior de Zenia Partners (agencia AI+CRM+WhatsApp para SMBs).

URL: {candidate['url']}
Query objetivo: "{candidate['query']}"
Posicion actual: {candidate['position']} (queremos top 3)
Impresiones/sem: {candidate['impressions']}
Clicks/sem: {candidate['clicks']} (CTR {candidate['ctr']}%)

PAGINA ACTUAL:
- Title ({page['title_length']} chars): "{page['title']}"
- Meta desc ({page['meta_length']} chars): "{page['meta_description']}"
- H1: "{page['h1']}"
- H2s: {json.dumps(page['h2s'], ensure_ascii=False)}
- Primer parrafo: "{page['first_paragraph']}"
- Word count: {page['word_count']}

Tu tarea: propon **3 cambios accionables especificos** para subir esta URL de pos {candidate['position']} a top 3.

Formato JSON estricto:
{{
  "fixes": [
    {{"type": "title", "priority": "high|medium|low", "current": "...", "proposed": "...", "rationale": "..."}},
    {{"type": "meta|h1|content_section|internal_link|schema", "priority": "...", "action": "...", "rationale": "..."}},
    ...
  ],
  "estimated_impact": "low|medium|high",
  "effort_minutes": 15
}}

Reglas:
- Title 50-60 chars, meta 145-160, ambos con keyword + benefit
- Si falta seccion clave para satisfacer search intent, propon "content_section" con titulo H2 sugerido + 2-3 bullets
- Si la pagina es thin (<800 words), priorizalo
- Internal links: sugiere link DESDE pillar pages (/blog/crm-para-X-espana-2026.html) a esta URL con anchor especifico
- Tono Zenia: directo, sin fluff, en español

Responde SOLO el JSON."""

    try:
        resp = call_anthropic(
            messages=[{"role": "user", "content": prompt}],
            model="claude-sonnet-4-5",
            max_tokens=2000,
            temperature=0.4,
        )
        start = resp.find("{")
        end = resp.rfind("}")
        if start >= 0 and end > start:
            data = json.loads(resp[start : end + 1])
            return {
                "url": candidate["url"],
                "query": candidate["query"],
                "position": candidate["position"],
                "impressions": candidate["impressions"],
                "fixes": data.get("fixes", []),
                "estimated_impact": data.get("estimated_impact", "medium"),
                "effort_minutes": data.get("effort_minutes", 30),
            }
    except Exception as exc:
        log("warning", "propose_failed", url=candidate["url"], error=str(exc))

    return {"url": candidate["url"], "query": candidate["query"], "fixes": [], "error": "claude_parse_failed"}


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------
def _impact_color(level: str) -> str:
    return {"high": "#059669", "medium": "#D97706", "low": "#94A3B8"}.get(level, "#64748B")


def _render_proposal(proposal: dict[str, Any]) -> str:
    if proposal.get("error"):
        return f"""<div class="callout warn">
<strong>{proposal['url']}</strong> — error: {proposal['error']}
</div>"""

    slug = proposal["url"].split("/")[-1].replace(".html", "")
    fixes_html = []
    for f in proposal.get("fixes", []):
        ftype = f.get("type", "?")
        priority = f.get("priority", "medium")
        prio_color = _impact_color(priority)
        if ftype in ("title", "meta", "h1") and "current" in f:
            body = f"""
<div><strong>Actual:</strong> <code>{f.get('current', '')}</code></div>
<div><strong>Propuesto:</strong> <code>{f.get('proposed', '')}</code></div>
<div style="color:#64748B"><em>{f.get('rationale', '')}</em></div>"""
        else:
            body = f"""
<div><strong>Accion:</strong> {f.get('action', '')}</div>
<div style="color:#64748B"><em>{f.get('rationale', '')}</em></div>"""

        fixes_html.append(
            f"""<li style="margin: 12px 0; padding: 10px; background: #F8FAFC; border-left: 3px solid {prio_color}; border-radius: 4px;">
<span class="tag fix">{ftype}</span> <span class="tag" style="background:{prio_color}20;color:{prio_color}">priority: {priority}</span>
{body}
</li>"""
        )

    impact = proposal.get("estimated_impact", "?")
    effort = proposal.get("effort_minutes", "?")
    impact_color = _impact_color(impact)

    return f"""<div style="background:white;border:1px solid #E2E8F0;border-radius:8px;padding:18px;margin:14px 0;">
<h3 style="margin-top:0">{slug}</h3>
<p style="color:#64748B;margin:4px 0">
  Query: <code>{proposal['query']}</code> · Pos {proposal['position']} · {proposal['impressions']:,} imp/sem ·
  <span style="color:{impact_color};font-weight:600">impact: {impact}</span> · {effort}min
</p>
<ol style="padding:0;list-style:none">{''.join(fixes_html)}</ol>
</div>"""


def _render_top5_summary(proposals: list[dict[str, Any]]) -> str:
    """Top 5 by impressions for email — 'apply this week'."""
    top5 = sorted(
        [p for p in proposals if p.get("fixes")],
        key=lambda x: x.get("impressions", 0),
        reverse=True,
    )[:5]
    items = []
    for i, p in enumerate(top5, 1):
        slug = p["url"].split("/")[-1].replace(".html", "")
        first_fix = p["fixes"][0] if p["fixes"] else {}
        action_summary = first_fix.get("proposed") or first_fix.get("action", "—")
        items.append(
            f"""<li style="margin: 10px 0">
  <strong>#{i} {slug}</strong> (pos {p['position']}, {p['impressions']:,} imp)<br>
  <small style="color:#64748B">→ {first_fix.get('type', '?')}: {action_summary[:120]}</small>
</li>"""
        )
    return f"<ol style='padding-left:20px'>{''.join(items)}</ol>"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run(
    *,
    days: int = 7,
    max_urls: int = 25,
    send: bool = True,
    force: bool = False,
) -> dict[str, Any]:
    load_env()

    if not force and not acquire_run_lock("optimizer"):
        log("info", "optimizer_skipped_locked")
        return {"skipped": True}

    log("info", "optimizer_start", days=days, max_urls=max_urls)

    # 1. Pull query+page pairs from GSC
    pairs = get_query_page_pairs(days=days, row_limit=2000)
    log("info", "gsc_pairs_loaded", count=len(pairs))

    # 2. Select candidates in 5-15 zone
    candidates = _select_candidates(pairs, max_urls=max_urls)
    log("info", "candidates_selected", count=len(candidates))

    if not candidates:
        log("warning", "no_candidates_found")
        body = """<div class="callout warn">
<strong>Sin candidatos esta semana.</strong> No hay URLs en posicion 5-15 con >50 impresiones.
Esto puede significar: poco trafico todavia, o todas las URLs ya estan top 5 o fuera de top 30.
</div>"""
        html = render_html_report(
            title="Zenia SEO — Optimizer Weekly",
            subtitle="Sin oportunidades quick-win esta semana",
            body_html=body,
        )
        report_path = REPORTS_DIR / "optimizer" / f"{now_date()}-optimizer.html"
        write_text(report_path, html)
        return {"candidates": [], "proposals": []}

    # 3. Fetch + propose for each
    proposals = []
    for i, cand in enumerate(candidates, 1):
        log("info", "processing_candidate", i=i, total=len(candidates), url=cand["url"])
        page_data = _fetch_page(cand["url"])
        proposal = _propose_fixes(cand, page_data)
        proposals.append(proposal)

    # 4. Render full report
    valid = [p for p in proposals if p.get("fixes")]
    body_parts = [
        f"""<div class="callout">
<strong>{len(valid)}</strong> URLs analizadas en zona quick-win (pos 5-15, >50 imp/sem).
Estos cambios son report-only. Aplicalos manualmente o por batch en el repo.
</div>"""
    ]
    if valid:
        body_parts.append("<h2>Top 5 quick wins (alta prioridad esta semana)</h2>")
        body_parts.append(_render_top5_summary(valid))
        body_parts.append("<h2>Propuestas detalladas por URL</h2>")
        for p in proposals:
            body_parts.append(_render_proposal(p))

    html = render_html_report(
        title="Zenia SEO — Optimizer Weekly",
        subtitle=f"Quick wins · {len(valid)} URLs · pos 5-15",
        body_html="\n".join(body_parts),
    )
    report_path = REPORTS_DIR / "optimizer" / f"{now_date()}-optimizer.html"
    write_text(report_path, html)

    # Save snapshot for debugging
    cache_path = CACHE_DIR / "optimizer_proposals.json"
    cache_path.write_text(
        json.dumps(proposals, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )

    log("info", "optimizer_report_saved", path=str(report_path))

    # 5. Email summary (top 5)
    if send and valid:
        email_html = render_html_report(
            title="Optimizer Weekly",
            subtitle="Top 5 quick wins para aplicar esta semana",
            body_html=f"""
<div class="callout">
<strong>{len(valid)}</strong> URLs en zona 5-15 analizadas. Los 5 con mayor impresiones primero.
</div>
{_render_top5_summary(valid)}
<div class="callout success">
<strong>Reporte completo:</strong> <code>reports/seo/optimizer/{now_date()}-optimizer.html</code><br>
<small>Repo Zenia. Aplica fixes manualmente o crea batch PR.</small>
</div>""",
        )
        try:
            send_email(
                to=DEFAULT_TO_EMAIL,
                subject=f"[Zenia SEO] Optimizer — {len(valid)} quick wins · {now_date()}",
                html=email_html,
            )
        except Exception as exc:
            log("error", "email_failed", error=str(exc))

    write_run_lock("optimizer")
    log("info", "optimizer_done", proposals_count=len(valid))
    return {"candidates": candidates, "proposals": proposals}


def main() -> int:
    parser = argparse.ArgumentParser(description="Zenia SEO Optimizer Agent")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--max-urls", type=int, default=25)
    parser.add_argument("--no-send", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    try:
        run(days=args.days, max_urls=args.max_urls, send=not args.no_send, force=args.force)
        return 0
    except Exception as exc:
        log("error", "optimizer_fatal", error=str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
