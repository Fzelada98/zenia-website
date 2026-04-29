"""Shared utilities for Zenia SEO agents.

Wraps Anthropic API, Resend email, env loading, logging, and HTML report rendering.
All three agents (performance, optimizer, strategist) import from here.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ENV = REPO_ROOT / "backend" / ".env"
REPORTS_DIR = REPO_ROOT / "reports" / "seo"
CACHE_DIR = REPORTS_DIR / "cache"
BLOG_DIR = REPO_ROOT / "blog"
SEO_DIR = REPO_ROOT / "seo"

DEFAULT_TO_EMAIL = "fabrizzio.zelada@zeniapartners.com"
DEFAULT_FROM_EMAIL = "Zenia SEO Bot <reports@zeniapartners.com>"

ZENIA_BLUE = "#3B82F6"
ZENIA_INDIGO = "#6366F1"


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def _build_logger() -> logging.Logger:
    logger = logging.getLogger("zenia.seo")
    if logger.handlers:
        return logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(os.environ.get("ZENIA_SEO_LOG_LEVEL", "INFO"))
    logger.propagate = False
    return logger


_logger = _build_logger()


def log(level: str, message: str, **kwargs: Any) -> None:
    """Structured stdout log. `level` in {debug,info,warning,error}."""
    extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
    msg = f"{message} {extra}".strip()
    getattr(_logger, level.lower(), _logger.info)(msg)


# ---------------------------------------------------------------------------
# Env loading
# ---------------------------------------------------------------------------
def load_env() -> dict[str, str]:
    """Load environment variables.

    Priority:
    1. Existing os.environ values (GitHub Actions secrets)
    2. backend/.env file (local dev)

    Returns dict of values resolved (without overwriting existing env).
    """
    resolved: dict[str, str] = {}

    if BACKEND_ENV.exists():
        try:
            for line in BACKEND_ENV.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val
                resolved[key] = val
        except OSError as exc:
            log("warning", "could_not_read_backend_env", error=str(exc))

    # Validate required keys with friendly hint
    for key in ("ANTHROPIC_API_KEY", "RESEND_API_KEY"):
        if not os.environ.get(key):
            log("warning", "missing_env_var", key=key)

    return resolved


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------
def call_anthropic(
    messages: list[dict[str, Any]],
    *,
    model: str = "claude-haiku-4-5",
    max_tokens: int = 4096,
    system: str | None = None,
    temperature: float = 0.3,
    max_retries: int = 3,
) -> str:
    """Call Anthropic Messages API with retry/backoff. Returns assistant text."""
    try:
        from anthropic import Anthropic  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "anthropic package not installed. pip install -r scripts/seo/requirements.txt"
        ) from exc

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    client = Anthropic(api_key=api_key)
    last_err: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            kwargs: dict[str, Any] = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages,
            }
            if system:
                kwargs["system"] = system
            resp = client.messages.create(**kwargs)
            parts = []
            for block in resp.content:
                text = getattr(block, "text", None)
                if text:
                    parts.append(text)
            log(
                "info",
                "anthropic_call_ok",
                model=model,
                input_tokens=getattr(resp.usage, "input_tokens", "?"),
                output_tokens=getattr(resp.usage, "output_tokens", "?"),
            )
            return "\n".join(parts).strip()
        except Exception as exc:  # broad: covers RateLimit, APIError, network
            last_err = exc
            wait = min(2**attempt, 30)
            log("warning", "anthropic_retry", attempt=attempt, wait=wait, error=str(exc))
            time.sleep(wait)

    raise RuntimeError(f"Anthropic call failed after {max_retries} retries: {last_err}")


# ---------------------------------------------------------------------------
# Resend email
# ---------------------------------------------------------------------------
def send_email(
    to: str | list[str],
    subject: str,
    html: str,
    *,
    from_email: str = DEFAULT_FROM_EMAIL,
    attachments: list[dict[str, str]] | None = None,
    max_retries: int = 3,
) -> dict[str, Any]:
    """Send email via Resend API. Returns response JSON."""
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        raise RuntimeError("RESEND_API_KEY not set")

    payload: dict[str, Any] = {
        "from": from_email,
        "to": [to] if isinstance(to, str) else to,
        "subject": subject,
        "html": html,
    }
    if attachments:
        payload["attachments"] = attachments

    last_err: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=30,
            )
            if resp.status_code >= 400:
                raise RuntimeError(f"Resend HTTP {resp.status_code}: {resp.text}")
            data = resp.json()
            log("info", "email_sent", to=payload["to"], subject=subject, id=data.get("id"))
            return data
        except Exception as exc:
            last_err = exc
            wait = min(2**attempt, 20)
            log("warning", "resend_retry", attempt=attempt, wait=wait, error=str(exc))
            time.sleep(wait)

    raise RuntimeError(f"Resend failed after {max_retries} retries: {last_err}")


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------
def read_json(path: Path | str, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        log("error", "json_parse_failed", path=str(p), error=str(exc))
        return default


def write_json(path: Path | str, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


def write_text(path: Path | str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def list_blog_posts() -> list[str]:
    """Return list of HTML files in /blog (filenames only, excluding index)."""
    if not BLOG_DIR.exists():
        return []
    return sorted(
        f.name
        for f in BLOG_DIR.iterdir()
        if f.is_file() and f.suffix == ".html" and f.name != "index.html"
    )


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------
_BASE_CSS = f"""
* {{ box-sizing: border-box; }}
body {{
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #0F172A;
  background: #F8FAFC;
  margin: 0;
  line-height: 1.55;
  font-size: 14px;
}}
.container {{ max-width: 980px; margin: 0 auto; padding: 32px 24px; }}
h1 {{
  font-size: 28px;
  margin: 0 0 4px;
  background: linear-gradient(90deg, {ZENIA_BLUE}, {ZENIA_INDIGO});
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
h2 {{ font-size: 20px; margin: 32px 0 12px; color: #1E293B; border-bottom: 1px solid #E2E8F0; padding-bottom: 6px; }}
h3 {{ font-size: 16px; margin: 18px 0 8px; color: #334155; }}
.subtitle {{ color: #64748B; margin: 0 0 24px; font-size: 13px; }}
.kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 16px 0 24px; }}
.kpi {{ background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; }}
.kpi-label {{ font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.04em; }}
.kpi-value {{ font-size: 22px; font-weight: 700; margin-top: 4px; color: #0F172A; }}
.kpi-delta {{ font-size: 12px; margin-top: 2px; font-weight: 600; }}
.kpi-delta.up {{ color: #059669; }}
.kpi-delta.down {{ color: #DC2626; }}
.kpi-delta.flat {{ color: #94A3B8; }}
table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; border: 1px solid #E2E8F0; }}
th, td {{ padding: 10px 12px; text-align: left; font-size: 13px; border-bottom: 1px solid #F1F5F9; }}
th {{ background: #F8FAFC; font-weight: 600; color: #475569; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }}
tr:last-child td {{ border-bottom: none; }}
td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
.up {{ color: #059669; }}
.down {{ color: #DC2626; }}
.tag {{ display: inline-block; padding: 2px 8px; background: #EFF6FF; color: {ZENIA_BLUE}; border-radius: 4px; font-size: 11px; font-weight: 600; }}
.tag.refresh {{ background: #FEF3C7; color: #B45309; }}
.tag.new {{ background: #D1FAE5; color: #047857; }}
.tag.fix {{ background: #FEE2E2; color: #B91C1C; }}
.callout {{ background: white; border-left: 3px solid {ZENIA_BLUE}; padding: 14px 18px; margin: 16px 0; border-radius: 4px; }}
.callout.warn {{ border-color: #F59E0B; }}
.callout.success {{ border-color: #10B981; }}
ul, ol {{ margin: 8px 0; padding-left: 22px; }}
li {{ margin: 4px 0; }}
code {{ background: #F1F5F9; padding: 2px 6px; border-radius: 3px; font-family: 'SF Mono', Menlo, monospace; font-size: 12px; }}
footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #E2E8F0; color: #94A3B8; font-size: 12px; text-align: center; }}
@media print {{
  body {{ background: white; font-size: 12px; }}
  .container {{ padding: 16px; }}
  table {{ page-break-inside: avoid; }}
}}
@media (max-width: 640px) {{
  .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
"""


def render_html_report(title: str, subtitle: str, body_html: str) -> str:
    """Wrap body content in standard Zenia SEO report shell."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Zenia SEO</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{_BASE_CSS}</style>
</head>
<body>
<div class="container">
  <h1>{title}</h1>
  <p class="subtitle">{subtitle} · generado {now}</p>
  {body_html}
  <footer>Zenia SEO Operating System · automated by Anthropic + Google Search Console</footer>
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Helpers for delta formatting
# ---------------------------------------------------------------------------
def fmt_delta(curr: float, prev: float, *, as_pct: bool = False, decimals: int = 1) -> str:
    """Format week-over-week delta as HTML span with arrow + class."""
    if prev == 0 and curr == 0:
        return '<span class="kpi-delta flat">—</span>'
    if prev == 0:
        return f'<span class="kpi-delta up">▲ new</span>'
    delta = curr - prev
    pct = (delta / prev) * 100 if prev else 0
    cls = "up" if delta > 0 else ("down" if delta < 0 else "flat")
    arrow = "▲" if delta > 0 else ("▼" if delta < 0 else "—")
    if as_pct:
        return f'<span class="kpi-delta {cls}">{arrow} {abs(delta):.{decimals}f}pp</span>'
    return f'<span class="kpi-delta {cls}">{arrow} {abs(pct):.{decimals}f}%</span>'


def fmt_position_delta(curr: float, prev: float) -> str:
    """For position metrics — lower is better, so flip sign semantics."""
    if prev == 0 and curr == 0:
        return '<span class="kpi-delta flat">—</span>'
    delta = curr - prev
    cls = "up" if delta < 0 else ("down" if delta > 0 else "flat")
    arrow = "▲" if delta < 0 else ("▼" if delta > 0 else "—")
    return f'<span class="kpi-delta {cls}">{arrow} {abs(delta):.1f}</span>'


def chunked(seq: list, size: int) -> Iterable[list]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Idempotency lock (avoid duplicate runs on retry)
# ---------------------------------------------------------------------------
def acquire_run_lock(agent: str, ttl_hours: int = 12) -> bool:
    """Returns False if a recent successful run exists (within TTL).

    Used to skip re-sending emails when GitHub Actions retries the same job.
    """
    lock_path = CACHE_DIR / f"{agent}.lock.json"
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    if lock_path.exists():
        try:
            data = json.loads(lock_path.read_text(encoding="utf-8"))
            ts = datetime.fromisoformat(data.get("timestamp", ""))
            age_hours = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
            if age_hours < ttl_hours:
                log("warning", "lock_active_skip", agent=agent, age_hours=round(age_hours, 1))
                return False
        except (ValueError, json.JSONDecodeError):
            pass

    return True


def write_run_lock(agent: str) -> None:
    lock_path = CACHE_DIR / f"{agent}.lock.json"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps({"timestamp": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
