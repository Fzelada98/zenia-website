#!/usr/bin/env python3
"""Extended SEO autofix: titles, missing meta desc, missing OG/Twitter, hreflang, orphans."""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent

TITLE_RE = re.compile(r'<title>(.*?)</title>', re.DOTALL)
META_DESC_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']\s*/?>', re.IGNORECASE)
META_DESC_ANY_RE = re.compile(r'<meta\s+name=["\']description["\'][^>]*>', re.IGNORECASE)
OG_TITLE_RE = re.compile(r'<meta\s+property=["\']og:title["\']', re.IGNORECASE)
TW_CARD_RE = re.compile(r'<meta\s+name=["\']twitter:card["\']', re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r'</head>', re.IGNORECASE)
HREFLANG_RE = re.compile(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']([^"\']+)["\']\s+href=["\']([^"\']+)["\']', re.IGNORECASE)


def get_all_html_files():
    excludes = {"node_modules", ".git", "reports", "_audit_", "backend",
                "snippets", "demo", "agents", "ts-beta", "ts-preview", "lead-magnets",
                "posts", "unsubscribe.html"}
    files = []
    for path in REPO.rglob("*.html"):
        rel = path.relative_to(REPO)
        if any(part in excludes or part.startswith(".") for part in rel.parts):
            continue
        if rel.name in excludes:
            continue
        files.append(path)
    return files


def shorten_title(title, max_chars=60):
    """Drop trailing '| segment' until under max_chars, keep first segment."""
    title = title.strip()
    if len(title) <= max_chars:
        return title
    # Split by | and progressively drop trailing segments
    parts = [p.strip() for p in title.split("|")]
    while len(parts) > 1 and len(" | ".join(parts)) > max_chars:
        parts.pop()
    candidate = " | ".join(parts)
    if len(candidate) <= max_chars:
        return candidate
    # Still too long: hard truncate at word boundary
    return candidate[:max_chars].rsplit(" ", 1)[0]


def fix_titles(files, dry_run=True):
    fixed = 0
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        m = TITLE_RE.search(content)
        if not m:
            continue
        old = m.group(1).strip()
        if len(old) <= 60:
            continue
        new = shorten_title(old)
        if new == old:
            continue
        new_content = content[:m.start()] + f"<title>{new}</title>" + content[m.end():]
        # Also sync og:title and twitter:title if present
        new_content = re.sub(
            r'(<meta\s+property=["\']og:title["\']\s+content=["\'])[^"\']*(["\'])',
            r'\g<1>' + new + r'\g<2>',
            new_content, flags=re.IGNORECASE
        )
        new_content = re.sub(
            r'(<meta\s+name=["\']twitter:title["\']\s+content=["\'])[^"\']*(["\'])',
            r'\g<1>' + new + r'\g<2>',
            new_content, flags=re.IGNORECASE
        )
        if not dry_run:
            open(f, "w", encoding="utf-8", newline="").write(new_content)
        print(f"  {'(dry) ' if dry_run else ''}{f.relative_to(REPO)}: {len(old)}c -> {len(new)}c")
        fixed += 1
    return fixed


def fix_missing_meta_desc(files, dry_run=True):
    """Find pages with missing/empty meta desc, derive from title or H1."""
    fixed = 0
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        m = META_DESC_RE.search(content)
        has_meta = m is not None and m.group(1).strip() != ""
        if has_meta:
            continue
        # Build description from title
        tm = TITLE_RE.search(content)
        if not tm:
            continue
        title = tm.group(1).strip().split("|")[0].strip()
        desc = (
            f"{title}. ZENIA automatiza WhatsApp, ventas y seguimiento "
            f"24/7 con CRM omnicanal e IA. Implementacion en 5 semanas."
        )[:155]
        new_meta = f'<meta name="description" content="{desc}">'
        if META_DESC_ANY_RE.search(content):
            new_content = META_DESC_ANY_RE.sub(new_meta, content, count=1)
        else:
            new_content = HEAD_CLOSE_RE.sub(new_meta + "\n</head>", content, count=1)
        if not dry_run:
            open(f, "w", encoding="utf-8", newline="").write(new_content)
        print(f"  {'(dry) ' if dry_run else ''}{f.relative_to(REPO)}: meta desc added")
        fixed += 1
    return fixed


def fix_missing_og_twitter(files, dry_run=True):
    """Add og:* and twitter:card tags if missing, using title and meta desc."""
    fixed_og = 0
    fixed_tw = 0
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        has_og = OG_TITLE_RE.search(content) is not None
        has_tw = TW_CARD_RE.search(content) is not None
        if has_og and has_tw:
            continue
        tm = TITLE_RE.search(content)
        dm = META_DESC_RE.search(content)
        if not tm:
            continue
        title = tm.group(1).strip()
        desc = dm.group(1).strip() if dm else title
        og_block = ""
        tw_block = ""
        if not has_og:
            og_block = (
                f'<meta property="og:type" content="website">\n'
                f'<meta property="og:title" content="{title}">\n'
                f'<meta property="og:description" content="{desc}">\n'
                f'<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">\n'
                f'<meta property="og:site_name" content="ZENIA">\n'
            )
            fixed_og += 1
        if not has_tw:
            tw_block = (
                f'<meta name="twitter:card" content="summary_large_image">\n'
                f'<meta name="twitter:title" content="{title}">\n'
                f'<meta name="twitter:description" content="{desc}">\n'
                f'<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">\n'
            )
            fixed_tw += 1
        new_content = HEAD_CLOSE_RE.sub(og_block + tw_block + "</head>", content, count=1)
        if not dry_run:
            open(f, "w", encoding="utf-8", newline="").write(new_content)
        print(f"  {'(dry) ' if dry_run else ''}{f.relative_to(REPO)}: og={not has_og} tw={not has_tw}")
    return fixed_og, fixed_tw


def fix_hreflang_return_tags(files, dry_run=True):
    """Ensure ES landing has self hreflang + x-default. EN counterpart links back if exists."""
    fixed = 0
    for f in files:
        rel = f.relative_to(REPO)
        parts = rel.parts
        if not parts:
            continue
        # Only touch /es/ landings for now
        if parts[0] != "es":
            continue
        content = f.read_text(encoding="utf-8", errors="ignore")
        # Build canonical
        url_path = "/" + str(rel).replace("\\", "/")
        canonical = f"https://zeniapartners.com{url_path}"
        # Check existing hreflang tags
        existing = dict((lang.lower(), href) for lang, href in HREFLANG_RE.findall(content))
        needs_self = "es" not in existing
        needs_default = "x-default" not in existing
        if not (needs_self or needs_default):
            continue
        new_tags = ""
        if needs_self:
            new_tags += f'<link rel="alternate" hreflang="es" href="{canonical}">\n'
        if needs_default:
            new_tags += f'<link rel="alternate" hreflang="x-default" href="{canonical}">\n'
        # Insert before </head>
        new_content = HEAD_CLOSE_RE.sub(new_tags + "</head>", content, count=1)
        if new_content != content:
            if not dry_run:
                open(f, "w", encoding="utf-8", newline="").write(new_content)
            print(f"  {'(dry) ' if dry_run else ''}{rel}: hreflang return-tag added")
            fixed += 1
    return fixed


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    files = get_all_html_files()
    print(f"Scanning {len(files)} HTML files (apply={apply})\n")

    print("=== 1. TITLE SHORTEN (>60c) ===")
    n_titles = fix_titles(files, dry_run=not apply)
    print(f"Titles fixed: {n_titles}\n")

    print("=== 2. MISSING META DESC ===")
    n_meta = fix_missing_meta_desc(files, dry_run=not apply)
    print(f"Meta desc added: {n_meta}\n")

    print("=== 3. MISSING OG / TWITTER ===")
    og, tw = fix_missing_og_twitter(files, dry_run=not apply)
    print(f"OG added: {og} | Twitter added: {tw}\n")

    print("=== 4. HREFLANG RETURN-TAG ===")
    n_hl = fix_hreflang_return_tags(files, dry_run=not apply)
    print(f"Hreflang fixed: {n_hl}\n")

    print(f"TOTAL: titles={n_titles} meta={n_meta} og={og} tw={tw} hreflang={n_hl}")
