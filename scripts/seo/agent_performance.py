"""Agent: Performance — weekly GSC digest.

Runs Sunday 22:00 UTC. Pulls last 7 days vs previous 7 days from Search Console,
computes deltas, identifies gainers/losers/new/lost keywords, generates
HTML report and emails Fabrizzio.

Output: reports/seo/weekly/YYYY-MM-DD-performance.html
Output: reports/seo/cache/weekly_report.json (consumed by optimizer + strategist)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from typing import Any

from .gsc_client import get_week_over_week
from .lib import (
    CACHE_DIR,
    DEFAULT_TO_EMAIL,
    REPORTS_DIR,
    acquire_run_lock,
    call_anthropic,
    fmt_delta,
    fmt_position_delta,
    load_env,
    log,
    now_date,
    render_html_report,
    send_email,
    write_run_lock,
    write_text,
)

PILLAR_PATTERNS = ("/blog/crm-para-gimnasios-", "/blog/crm-para-estetica-",
                   "/blog/crm-para-restaurantes-", "/blog/crm-para-ecommerce-")


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------
def _key_index(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {r[key]: r for r in rows if r.get(key)}


def _totals(rows: list[dict[str, Any]]) -> dict[str, float]:
    clicks = sum(r["clicks"] for r in rows)
    imp = sum(r["impressions"] for r in rows)
    pos_weighted = sum(r["position"] * r["impressions"] for r in rows)
    return {
        "clicks": clicks,
        "impressions": imp,
        "ctr": (clicks / imp) if imp else 0.0,
        "position": (pos_weighted / imp) if imp else 0.0,
    }


def _top_n_by(rows: list[dict[str, Any]], field: str, n: int = 10) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda r: r.get(field, 0), reverse=True)[:n]


def _movers(
    curr: list[dict[str, Any]],
    prev: list[dict[str, Any]],
    *,
    min_impressions: int = 50,
    min_position_delta: float = 5.0,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Identify top gainers/losers by position movement."""
    prev_idx = _key_index(prev, "query")
    gainers, losers = [], []

    for r in curr:
        q = r.get("query")
        if not q or r["impressions"] < min_impressions:
            continue
        prev_row = prev_idx.get(q)
        if not prev_row:
            continue
        delta = prev_row["position"] - r["position"]  # positive = improved
        if abs(delta) < min_position_delta:
            continue
        entry = {
            "query": q,
            "curr_pos": round(r["position"], 1),
            "prev_pos": round(prev_row["position"], 1),
            "delta": round(delta, 1),
            "impressions": r["impressions"],
            "clicks": r["clicks"],
        }
        (gainers if delta > 0 else losers).append(entry)

    gainers.sort(key=lambda x: x["delta"], reverse=True)
    losers.sort(key=lambda x: x["delta"])
    return gainers[:5], losers[:5]


def _new_lost(
    curr: list[dict[str, Any]],
    prev: list[dict[str, Any]],
    *,
    min_impressions_new: int = 10,
    min_clicks_lost: int = 1,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    curr_idx = _key_index(curr, "query")
    prev_idx = _key_index(prev, "query")

    new_keywords = []
    for q, r in curr_idx.items():
        if q not in prev_idx and r["impressions"] >= min_impressions_new and r["position"] <= 50:
            new_keywords.append(
                {"query": q, "impressions": r["impressions"], "position": round(r["position"], 1)}
            )
    lost_keywords = []
    for q, r in prev_idx.items():
        if q not in curr_idx and r["clicks"] >= min_clicks_lost:
            lost_keywords.append(
                {"query": q, "prev_clicks": r["clicks"], "prev_position": round(r["position"], 1)}
            )

    new_keywords.sort(key=lambda x: x["impressions"], reverse=True)
    lost_keywords.sort(key=lambda x: x["prev_clicks"], reverse=True)
    return new_keywords[:15], lost_keywords[:15]


def _ctr_anomalies(rows: list[dict[str, Any]], *, min_imp: int = 100) -> list[dict[str, Any]]:
    """Pages with high impressions but low CTR for their position."""
    anomalies = []
    for r in rows:
        if r["impressions"] < min_imp:
            continue
        pos = r["position"]
        # Expected CTR baselines by position bucket (rough industry averages)
        if pos < 3:
            expected = 0.30
        elif pos < 6:
            expected = 0.10
        elif pos < 11:
            expected = 0.04
        else:
            continue
        if r["ctr"] < expected * 0.5:
            anomalies.append(
                {
                    "query": r.get("query") or r.get("page", ""),
                    "position": round(pos, 1),
                    "impressions": r["impressions"],
                    "ctr": round(r["ctr"] * 100, 2),
                    "expected_ctr": round(expected * 100, 2),
                }
            )
    anomalies.sort(key=lambda x: x["impressions"], reverse=True)
    return anomalies[:10]


def _pillar_performance(pages_curr: list[dict[str, Any]], pages_prev: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pillars = []
    prev_idx = _key_index(pages_prev, "page")
    for r in pages_curr:
        page = r.get("page") or ""
        if not any(p in page for p in PILLAR_PATTERNS):
            continue
        prev_row = prev_idx.get(page, {"clicks": 0, "impressions": 0, "position": 0})
        pillars.append(
            {
                "page": page,
                "clicks": r["clicks"],
                "prev_clicks": prev_row.get("clicks", 0),
                "impressions": r["impressions"],
                "prev_impressions": prev_row.get("impressions", 0),
                "position": round(r["position"], 1),
                "prev_position": round(prev_row.get("position", 0) or 0, 1),
            }
        )
    pillars.sort(key=lambda x: x["clicks"], reverse=True)
    return pillars


# ---------------------------------------------------------------------------
# Claude analysis
# ---------------------------------------------------------------------------
def _claude_insights(snapshot: dict[str, Any]) -> list[str]:
    """Ask Haiku for 5 prioritized actionable insights."""
    prompt = f"""Eres analista SEO senior de Zenia Partners (agencia AI+CRM+WhatsApp para SMBs).
Te paso datos GSC week-over-week. Genera **5 insights accionables priorizados** en español.

Cada insight: 1-2 frases, formato "ACCION: [verbo] [objeto] porque [razon basada en data]".
Prioriza por impact x facilidad. NO repitas datos; interpreta.

DATA (JSON):
{json.dumps(snapshot, indent=2, ensure_ascii=False)[:6000]}

Responde SOLO en JSON: {{"insights": ["...", "...", "...", "...", "..."]}}"""

    try:
        resp = call_anthropic(
            messages=[{"role": "user", "content": prompt}],
            model="claude-haiku-4-5",
            max_tokens=1500,
            temperature=0.3,
        )
        # Extract JSON from response
        start = resp.find("{")
        end = resp.rfind("}")
        if start >= 0 and end > start:
            data = json.loads(resp[start : end + 1])
            return data.get("insights", [])
    except Exception as exc:
        log("warning", "claude_insights_failed", error=str(exc))

    return ["No se pudieron generar insights automáticos esta semana (revisar logs)."]


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------
def _render_kpis(curr: dict[str, float], prev: dict[str, float]) -> str:
    return f"""<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Clicks</div>
    <div class="kpi-value">{int(curr['clicks']):,}</div>
    {fmt_delta(curr['clicks'], prev['clicks'])}
  </div>
  <div class="kpi">
    <div class="kpi-label">Impresiones</div>
    <div class="kpi-value">{int(curr['impressions']):,}</div>
    {fmt_delta(curr['impressions'], prev['impressions'])}
  </div>
  <div class="kpi">
    <div class="kpi-label">CTR medio</div>
    <div class="kpi-value">{curr['ctr']*100:.2f}%</div>
    {fmt_delta(curr['ctr']*100, prev['ctr']*100, as_pct=True, decimals=2)}
  </div>
  <div class="kpi">
    <div class="kpi-label">Posicion media</div>
    <div class="kpi-value">{curr['position']:.1f}</div>
    {fmt_position_delta(curr['position'], prev['position'])}
  </div>
</div>"""


def _render_query_table(rows: list[dict[str, Any]], prev_idx: dict[str, dict], title: str) -> str:
    if not rows:
        return f"<h2>{title}</h2><p style='color:#94A3B8'>Sin datos.</p>"
    body = []
    for r in rows:
        prev = prev_idx.get(r["query"], {})
        clicks_delta = fmt_delta(r["clicks"], prev.get("clicks", 0))
        body.append(
            f"<tr><td>{r['query']}</td>"
            f"<td class='num'>{r['clicks']}</td>"
            f"<td class='num'>{clicks_delta}</td>"
            f"<td class='num'>{r['impressions']:,}</td>"
            f"<td class='num'>{r['position']:.1f}</td></tr>"
        )
    return f"""<h2>{title}</h2>
<table>
<thead><tr><th>Query</th><th>Clicks</th><th>Δ W-W</th><th>Impresiones</th><th>Pos.</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""


def _render_movers(gainers: list[dict[str, Any]], losers: list[dict[str, Any]]) -> str:
    def _table(rows, kind):
        if not rows:
            return f"<p style='color:#94A3B8'>Sin {kind}.</p>"
        body = []
        for r in rows:
            cls = "up" if r["delta"] > 0 else "down"
            arrow = "▲" if r["delta"] > 0 else "▼"
            body.append(
                f"<tr><td>{r['query']}</td>"
                f"<td class='num'>{r['prev_pos']} → {r['curr_pos']}</td>"
                f"<td class='num {cls}'>{arrow} {abs(r['delta']):.1f}</td>"
                f"<td class='num'>{r['impressions']:,}</td></tr>"
            )
        return f"""<table><thead><tr><th>Query</th><th>Posicion</th><th>Δ</th><th>Imp.</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""

    return f"""<h2>Movimientos de posicion</h2>
<h3>Top 5 ganadores (subieron 5+ posiciones)</h3>
{_table(gainers, 'gainers')}
<h3>Top 5 perdedores</h3>
{_table(losers, 'losers')}"""


def _render_new_lost(new: list[dict[str, Any]], lost: list[dict[str, Any]]) -> str:
    def _ntable(rows):
        if not rows:
            return "<p style='color:#94A3B8'>Ninguna.</p>"
        body = []
        for r in rows:
            body.append(
                f"<tr><td>{r['query']}</td>"
                f"<td class='num'>{r['impressions']:,}</td>"
                f"<td class='num'>{r['position']:.1f}</td></tr>"
            )
        return f"""<table><thead><tr><th>Query</th><th>Imp.</th><th>Pos.</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""

    def _ltable(rows):
        if not rows:
            return "<p style='color:#94A3B8'>Ninguna.</p>"
        body = []
        for r in rows:
            body.append(
                f"<tr><td>{r['query']}</td>"
                f"<td class='num'>{r['prev_clicks']}</td>"
                f"<td class='num'>{r['prev_position']:.1f}</td></tr>"
            )
        return f"""<table><thead><tr><th>Query</th><th>Clicks W-1</th><th>Pos. W-1</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""

    return f"""<h2>Nuevas y perdidas</h2>
<h3>Nuevas keywords (top 50, no aparecian la semana pasada)</h3>
{_ntable(new)}
<h3>Keywords perdidas (con clicks en W-1)</h3>
{_ltable(lost)}"""


def _render_pillars(pillars: list[dict[str, Any]]) -> str:
    if not pillars:
        return "<h2>Pillar pages</h2><p style='color:#94A3B8'>Sin trafico esta semana en pillars.</p>"
    body = []
    for p in pillars:
        slug = p["page"].split("/")[-1].replace(".html", "")
        clicks_delta = fmt_delta(p["clicks"], p["prev_clicks"])
        imp_delta = fmt_delta(p["impressions"], p["prev_impressions"])
        body.append(
            f"<tr><td>{slug}</td>"
            f"<td class='num'>{p['clicks']}</td>"
            f"<td class='num'>{clicks_delta}</td>"
            f"<td class='num'>{p['impressions']:,}</td>"
            f"<td class='num'>{imp_delta}</td>"
            f"<td class='num'>{p['position']}</td></tr>"
        )
    return f"""<h2>Pillar pages performance</h2>
<table>
<thead><tr><th>Pillar</th><th>Clicks</th><th>Δ</th><th>Imp.</th><th>Δ</th><th>Pos.</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""


def _render_anomalies(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    body = []
    for r in rows:
        body.append(
            f"<tr><td>{r['query']}</td>"
            f"<td class='num'>{r['position']}</td>"
            f"<td class='num'>{r['impressions']:,}</td>"
            f"<td class='num down'>{r['ctr']}%</td>"
            f"<td class='num'>{r['expected_ctr']}%</td></tr>"
        )
    return f"""<h2>CTR anomalies</h2>
<p style="color:#64748B">Queries con muchas impresiones pero CTR muy por debajo del baseline. Candidatos a rewrite de title/meta.</p>
<table>
<thead><tr><th>Query</th><th>Pos.</th><th>Imp.</th><th>CTR actual</th><th>Esperado</th></tr></thead>
<tbody>{''.join(body)}</tbody></table>"""


def _render_insights(insights: list[str]) -> str:
    items = "".join(f"<li>{ins}</li>" for ins in insights)
    return f"""<h2>Insights accionables (Claude)</h2>
<div class="callout"><ol>{items}</ol></div>"""


# ---------------------------------------------------------------------------
# Email body (compact)
# ---------------------------------------------------------------------------
def _email_summary(snapshot: dict[str, Any], insights: list[str], report_path: str) -> str:
    curr = snapshot["totals_curr"]
    prev = snapshot["totals_prev"]
    insight_html = "".join(f"<li>{i}</li>" for i in insights[:5])
    return render_html_report(
        title="Performance Weekly",
        subtitle="Resumen ejecutivo Zenia SEO",
        body_html=f"""
{_render_kpis(curr, prev)}
<h2>5 insights priorizados</h2>
<div class="callout"><ol>{insight_html}</ol></div>
<div class="callout success">
  <strong>Reporte completo:</strong> <code>{report_path}</code><br>
  <small>Commiteado en repo. Ver tambien: optimizer (lunes 8am) + strategist (lunes 9am).</small>
</div>""",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run(*, days: int = 7, send: bool = True, force: bool = False) -> dict[str, Any]:
    load_env()

    if not force and not acquire_run_lock("performance"):
        log("info", "performance_skipped_locked")
        return {"skipped": True}

    log("info", "performance_start", days=days)

    # 1. Pull GSC data
    queries_curr, queries_prev = get_week_over_week(days=days, dimensions=["query"], row_limit=1000)
    pages_curr, pages_prev = get_week_over_week(days=days, dimensions=["page"], row_limit=500)

    # 2. Compute aggregates
    totals_curr = _totals(queries_curr)
    totals_prev = _totals(queries_prev)

    top_clicks = _top_n_by(queries_curr, "clicks", 10)
    top_imp = _top_n_by(queries_curr, "impressions", 10)
    gainers, losers = _movers(queries_curr, queries_prev)
    new_kw, lost_kw = _new_lost(queries_curr, queries_prev)
    anomalies = _ctr_anomalies(queries_curr)
    pillars = _pillar_performance(pages_curr, pages_prev)
    prev_idx = _key_index(queries_prev, "query")

    snapshot = {
        "date": now_date(),
        "totals_curr": totals_curr,
        "totals_prev": totals_prev,
        "top_clicks": top_clicks,
        "top_impressions": top_imp,
        "gainers": gainers,
        "losers": losers,
        "new_keywords": new_kw,
        "lost_keywords": lost_kw,
        "ctr_anomalies": anomalies,
        "pillars": pillars,
        "queries_curr_count": len(queries_curr),
        "pages_curr_count": len(pages_curr),
    }

    # 3. Claude insights
    insights = _claude_insights(
        {
            "totals_curr": totals_curr,
            "totals_prev": totals_prev,
            "top_clicks": top_clicks[:5],
            "gainers": gainers,
            "losers": losers,
            "new_keywords": new_kw[:5],
            "lost_keywords": lost_kw[:5],
            "anomalies": anomalies[:5],
        }
    )
    snapshot["insights"] = insights

    # 4. Render HTML
    body_parts = [
        _render_kpis(totals_curr, totals_prev),
        _render_insights(insights),
        _render_query_table(top_clicks, prev_idx, "Top 10 queries por clicks"),
        _render_query_table(top_imp, prev_idx, "Top 10 queries por impresiones"),
        _render_movers(gainers, losers),
        _render_new_lost(new_kw, lost_kw),
        _render_pillars(pillars),
        _render_anomalies(anomalies),
    ]
    html = render_html_report(
        title="Zenia SEO — Performance Weekly",
        subtitle=f"GSC week-over-week · {totals_curr['clicks']:.0f} clicks · {totals_curr['impressions']:.0f} impresiones",
        body_html="\n".join(body_parts),
    )

    # 5. Save artifacts
    report_path = REPORTS_DIR / "weekly" / f"{now_date()}-performance.html"
    snapshot_path = CACHE_DIR / "weekly_report.json"
    write_text(report_path, html)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    log("info", "performance_report_saved", path=str(report_path))

    # 6. Email
    if send:
        try:
            send_email(
                to=DEFAULT_TO_EMAIL,
                subject=f"[Zenia SEO] Performance Weekly — {now_date()}",
                html=_email_summary(snapshot, insights, str(report_path.relative_to(report_path.parents[3]))),
            )
        except Exception as exc:
            log("error", "email_failed", error=str(exc))

    write_run_lock("performance")
    log("info", "performance_done")
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Zenia SEO Performance Agent")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--no-send", action="store_true", help="Skip email")
    parser.add_argument("--force", action="store_true", help="Bypass idempotency lock")
    args = parser.parse_args()

    try:
        run(days=args.days, send=not args.no_send, force=args.force)
        return 0
    except Exception as exc:
        log("error", "performance_fatal", error=str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
