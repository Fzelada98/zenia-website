"""Google Search Console API wrapper for Zenia.

Provides authentication (OAuth user-credentials flow) and convenience methods
for query/page analytics. Caches responses to disk to avoid re-querying within
the same day.

Site URL: sc-domain:zeniapartners.com (domain property, set via env GSC_SITE_URL).
"""
from __future__ import annotations

import base64
import json
import os
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from .lib import CACHE_DIR, log

GSC_SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
DEFAULT_SITE_URL = "sc-domain:zeniapartners.com"


# ---------------------------------------------------------------------------
# Credential helpers
# ---------------------------------------------------------------------------
def _decode_b64_or_raw(value: str) -> str:
    """Allow secrets to be either raw JSON or base64-encoded JSON."""
    value = value.strip()
    if value.startswith("{"):
        return value
    try:
        return base64.b64decode(value).decode("utf-8")
    except Exception:
        return value


def _load_token_from_env() -> dict[str, Any] | None:
    raw = os.environ.get("GSC_TOKEN_JSON")
    if not raw:
        return None
    try:
        return json.loads(_decode_b64_or_raw(raw))
    except json.JSONDecodeError as exc:
        log("error", "gsc_token_env_invalid", error=str(exc))
        return None


def _load_token_from_disk() -> dict[str, Any] | None:
    candidates = [
        Path(__file__).resolve().parent / "token.json",
        Path(__file__).resolve().parents[2] / "backend" / "token.json",
        Path(__file__).resolve().parents[2] / "token.json",
    ]
    for p in candidates:
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                log("error", "gsc_token_disk_invalid", path=str(p), error=str(exc))
    return None


def _load_credentials_json() -> dict[str, Any] | None:
    """Load the OAuth client_secret.json (used for refresh)."""
    raw = os.environ.get("GSC_CREDENTIALS_JSON")
    if raw:
        try:
            return json.loads(_decode_b64_or_raw(raw))
        except json.JSONDecodeError:
            pass
    candidates = [
        Path(__file__).resolve().parent / "client_secret.json",
        Path(__file__).resolve().parents[2] / "backend" / "client_secret.json",
    ]
    for p in candidates:
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    return None


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
def authenticate():
    """Build authenticated GSC API client. Returns googleapiclient resource."""
    try:
        from google.oauth2.credentials import Credentials  # type: ignore
        from google.auth.transport.requests import Request  # type: ignore
        from googleapiclient.discovery import build  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "google-api-python-client not installed. pip install -r scripts/seo/requirements.txt"
        ) from exc

    token = _load_token_from_env() or _load_token_from_disk()
    if not token:
        raise RuntimeError(
            "No GSC token found. Set GSC_TOKEN_JSON env var or run setup_gsc_oauth.py first."
        )

    client_secret = _load_credentials_json()
    client_info: dict[str, Any] = {}
    if client_secret:
        installed = client_secret.get("installed") or client_secret.get("web") or {}
        client_info = {
            "client_id": installed.get("client_id"),
            "client_secret": installed.get("client_secret"),
            "token_uri": installed.get("token_uri", "https://oauth2.googleapis.com/token"),
        }

    creds = Credentials(
        token=token.get("token") or token.get("access_token"),
        refresh_token=token.get("refresh_token"),
        token_uri=token.get("token_uri") or client_info.get("token_uri"),
        client_id=token.get("client_id") or client_info.get("client_id"),
        client_secret=token.get("client_secret") or client_info.get("client_secret"),
        scopes=token.get("scopes") or GSC_SCOPES,
    )

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            log("info", "gsc_token_refreshed")
        except Exception as exc:
            log("error", "gsc_token_refresh_failed", error=str(exc))
            raise

    service = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    return service


# ---------------------------------------------------------------------------
# Search Analytics queries
# ---------------------------------------------------------------------------
def _site_url() -> str:
    return os.environ.get("GSC_SITE_URL", DEFAULT_SITE_URL)


def _cache_key(name: str, **params: Any) -> Path:
    today = date.today().isoformat()
    parts = "_".join(f"{k}-{v}" for k, v in sorted(params.items()))
    safe = parts.replace("/", "_").replace(":", "_")[:100]
    return CACHE_DIR / f"gsc_{name}_{today}_{safe}.json"


def get_search_analytics(
    start_date: str,
    end_date: str,
    *,
    dimensions: list[str] | None = None,
    row_limit: int = 1000,
    use_cache: bool = True,
    filters: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Query Search Analytics. Returns list of {key1, key2, ..., clicks, impressions, ctr, position}.

    Uses date-keyed disk cache to avoid duplicate API calls on same day.
    Handles pagination automatically up to row_limit total rows.
    """
    dimensions = dimensions or ["query"]
    cache_path = _cache_key(
        "analytics",
        start=start_date,
        end=end_date,
        dims="-".join(dimensions),
        rows=row_limit,
        filters=hash(json.dumps(filters or [], sort_keys=True)),
    )

    if use_cache and cache_path.exists():
        log("info", "gsc_cache_hit", path=cache_path.name)
        return json.loads(cache_path.read_text(encoding="utf-8"))

    service = authenticate()
    site = _site_url()
    all_rows: list[dict[str, Any]] = []
    start_row = 0
    page_size = min(row_limit, 25000)

    while len(all_rows) < row_limit:
        body: dict[str, Any] = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": page_size,
            "startRow": start_row,
            "type": "web",
        }
        if filters:
            body["dimensionFilterGroups"] = [{"filters": filters}]

        # naive rate-limit guard: max 5 calls/sec
        time.sleep(0.25)

        try:
            resp = service.searchanalytics().query(siteUrl=site, body=body).execute()
        except Exception as exc:
            log("error", "gsc_query_failed", error=str(exc))
            break

        rows = resp.get("rows", [])
        if not rows:
            break

        for row in rows:
            keys = row.get("keys", [])
            entry = {dim: keys[i] if i < len(keys) else None for i, dim in enumerate(dimensions)}
            entry.update(
                {
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": row.get("ctr", 0.0),
                    "position": row.get("position", 0.0),
                }
            )
            all_rows.append(entry)

        if len(rows) < page_size:
            break
        start_row += page_size

    all_rows = all_rows[:row_limit]
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(all_rows, ensure_ascii=False), encoding="utf-8")
    log("info", "gsc_query_ok", rows=len(all_rows), dims=dimensions)
    return all_rows


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------
def _date_range(days: int, offset: int = 0) -> tuple[str, str]:
    end = date.today() - timedelta(days=offset)
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def get_top_queries(days: int = 7, *, offset: int = 0, row_limit: int = 500) -> list[dict[str, Any]]:
    start, end = _date_range(days, offset)
    return get_search_analytics(start, end, dimensions=["query"], row_limit=row_limit)


def get_top_pages(days: int = 7, *, offset: int = 0, row_limit: int = 500) -> list[dict[str, Any]]:
    start, end = _date_range(days, offset)
    return get_search_analytics(start, end, dimensions=["page"], row_limit=row_limit)


def get_query_page_pairs(
    days: int = 7, *, offset: int = 0, row_limit: int = 1000
) -> list[dict[str, Any]]:
    start, end = _date_range(days, offset)
    return get_search_analytics(
        start, end, dimensions=["query", "page"], row_limit=row_limit
    )


def get_url_metrics(url: str, days: int = 7) -> dict[str, Any]:
    start, end = _date_range(days)
    rows = get_search_analytics(
        start,
        end,
        dimensions=["query"],
        row_limit=200,
        filters=[{"dimension": "page", "operator": "equals", "expression": url}],
        use_cache=True,
    )
    if not rows:
        return {"url": url, "clicks": 0, "impressions": 0, "ctr": 0, "position": 0, "queries": []}
    total_clicks = sum(r["clicks"] for r in rows)
    total_imp = sum(r["impressions"] for r in rows)
    avg_pos = sum(r["position"] * r["impressions"] for r in rows) / max(total_imp, 1)
    avg_ctr = total_clicks / max(total_imp, 1)
    return {
        "url": url,
        "clicks": total_clicks,
        "impressions": total_imp,
        "ctr": avg_ctr,
        "position": round(avg_pos, 2),
        "queries": rows[:50],
    }


def get_week_over_week(
    days: int = 7,
    *,
    dimensions: list[str] | None = None,
    row_limit: int = 1000,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (current_week, previous_week) as parallel lists."""
    dimensions = dimensions or ["query"]
    curr_start, curr_end = _date_range(days, offset=0)
    prev_start, prev_end = _date_range(days, offset=days)
    curr = get_search_analytics(curr_start, curr_end, dimensions=dimensions, row_limit=row_limit)
    prev = get_search_analytics(prev_start, prev_end, dimensions=dimensions, row_limit=row_limit)
    return curr, prev
