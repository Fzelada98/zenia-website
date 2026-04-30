#!/usr/bin/env python3
"""SEO Auto-Fix: detecta y corrige issues identificados por Ahrefs audit.

Funciones:
1. Broken internal links: crawl repo + check si target file existe en disco
2. Meta descriptions >155 chars: las trunca a 150 + ...
3. Titles >60 chars: los flagea (no auto-fix, requiere humano)
4. Submit URLs a IndexNow API (free)

Run from repo root: py scripts/seo_autofix.py
"""
import csv
import os
import re
import sys
import json
from pathlib import Path
from urllib.parse import urlparse, unquote

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent

INTERNAL_HREF_RE = re.compile(r'href=["\'](/[^"\']*\.html)["\']', re.IGNORECASE)
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.DOTALL)
META_DESC_RE = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', re.IGNORECASE)


def get_all_html_files():
    """List all .html files in repo (excluding node_modules, reports/, etc)."""
    excludes = {"node_modules", ".git", "reports", "_audit_", "backend"}
    files = []
    for path in REPO.rglob("*.html"):
        rel = path.relative_to(REPO)
        if any(part in excludes or part.startswith(".") for part in rel.parts):
            continue
        files.append(path)
    return files


def url_to_filepath(url):
    """Convert URL like /blog/foo.html to filesystem path."""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if path.startswith("/"):
        path = path[1:]
    return REPO / path


def find_broken_links(files):
    """For each file, find internal links and check if target exists."""
    broken = []  # list of (source_file, broken_url, line_num_approx)
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        for m in INTERNAL_HREF_RE.finditer(content):
            url = m.group(1)
            target = url_to_filepath(url)
            if not target.exists():
                # find approx line number
                line_num = content[:m.start()].count("\n") + 1
                broken.append({
                    "source": str(f.relative_to(REPO)),
                    "broken_url": url,
                    "line": line_num,
                })
    return broken


def find_long_meta_descs(files, max_chars=155):
    """Find meta descriptions exceeding max_chars."""
    long_metas = []
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        m = META_DESC_RE.search(content)
        if m:
            desc = m.group(1)
            if len(desc) > max_chars:
                long_metas.append({
                    "file": str(f.relative_to(REPO)),
                    "length": len(desc),
                    "desc": desc[:80] + "...",
                })
    return long_metas


def find_long_titles(files, max_chars=60):
    """Find titles exceeding max_chars (Google SERP cutoff)."""
    long_titles = []
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        m = TITLE_RE.search(content)
        if m:
            title = m.group(1).strip()
            if len(title) > max_chars:
                long_titles.append({
                    "file": str(f.relative_to(REPO)),
                    "length": len(title),
                    "title": title,
                })
    return long_titles


def build_basename_map(files):
    """Build map {basename.html: '/correct/path/basename.html'} for all html files."""
    bmap = {}
    for f in files:
        rel = f.relative_to(REPO)
        # URL-style path: forward slashes + leading /
        url_path = "/" + str(rel).replace("\\", "/")
        basename = f.name
        # If multiple files share basename, prefer one in es/ over blog/
        if basename in bmap:
            existing = bmap[basename]
            if "/es/" in url_path and "/es/" not in existing:
                bmap[basename] = url_path
        else:
            bmap[basename] = url_path
    return bmap


def fix_broken_links(broken_list, all_files, dry_run=True):
    """Smart fix: redirect to correct path if file exists elsewhere; else remove anchor."""
    bmap = build_basename_map(all_files)

    fixes_per_file = {}
    for entry in broken_list:
        fixes_per_file.setdefault(entry["source"], []).append(entry["broken_url"])

    redirected = 0
    removed = 0

    for src, urls in fixes_per_file.items():
        path = REPO / src
        content = path.read_text(encoding="utf-8", errors="ignore")
        new_content = content

        for url in urls:
            basename = url.rsplit("/", 1)[-1]
            correct_path = bmap.get(basename)

            if correct_path and correct_path != url:
                # REDIRECT: replace the broken URL with the correct one
                new_content = new_content.replace(f'href="{url}"', f'href="{correct_path}"')
                new_content = new_content.replace(f"href='{url}'", f"href='{correct_path}'")
                redirected += 1
            else:
                # REMOVE: file doesn't exist anywhere, strip the anchor
                pattern = re.compile(
                    r'<a\s+[^>]*?href=["\']' + re.escape(url) + r'["\'][^>]*?>(.*?)</a>',
                    re.DOTALL | re.IGNORECASE
                )
                new_content, n = pattern.subn(r'\1', new_content)
                removed += n

        if new_content != content:
            if not dry_run:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(new_content)
            print(f"  {'(dry) ' if dry_run else ''}{src}: redirected/removed broken links")

    return {"redirected": redirected, "removed": removed}


def truncate_long_metas(long_list, max_chars=150, dry_run=True):
    """Truncate meta descriptions exceeding max_chars to ... with ellipsis."""
    fixed = 0
    by_file = {entry["file"]: entry for entry in long_list}
    for fname, entry in by_file.items():
        path = REPO / fname
        content = path.read_text(encoding="utf-8", errors="ignore")

        m = META_DESC_RE.search(content)
        if not m:
            continue
        old_desc = m.group(1)
        if len(old_desc) <= max_chars:
            continue
        # Truncate cleanly at last word boundary before max_chars
        new_desc = old_desc[:max_chars].rsplit(" ", 1)[0]
        if not new_desc.endswith((".", "!", "?")):
            new_desc += "..."

        new_content = content[:m.start()] + f'<meta name="description" content="{new_desc}">' + content[m.end():]

        if not dry_run:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new_content)
        print(f"  {'(dry) ' if dry_run else ''}{fname}: {len(old_desc)}c -> {len(new_desc)}c")
        fixed += 1

    return fixed


def main():
    apply = "--apply" in sys.argv
    print(f"Mode: {'APPLY (writes changes)' if apply else 'DRY RUN (preview only)'}\n")

    files = get_all_html_files()
    print(f"Scanning {len(files)} HTML files...\n")

    # 1. Broken links
    print("=" * 60)
    print("1. BROKEN INTERNAL LINKS")
    print("=" * 60)
    broken = find_broken_links(files)
    print(f"Found {len(broken)} broken internal links\n")
    if broken:
        # Group by source for clarity
        by_source = {}
        for entry in broken:
            by_source.setdefault(entry["source"], []).append(entry)
        # Show top 20 sources
        sorted_sources = sorted(by_source.items(), key=lambda x: -len(x[1]))
        print("Top sources by broken link count:")
        for src, entries in sorted_sources[:20]:
            print(f"  {src}: {len(entries)} broken")
            for e in entries[:3]:
                print(f"    -> {e['broken_url']}")
            if len(entries) > 3:
                print(f"    ... ({len(entries) - 3} more)")
        print()
        # Apply fix
        result = fix_broken_links(broken, files, dry_run=not apply)
        print(f"\n{'(dry) ' if not apply else ''}Redirected {result['redirected']} URLs to correct path")
        print(f"{'(dry) ' if not apply else ''}Removed {result['removed']} dead anchors (no replacement found)")

    # 2. Long meta descriptions
    print("\n" + "=" * 60)
    print("2. META DESCRIPTIONS > 155 chars")
    print("=" * 60)
    long_metas = find_long_meta_descs(files)
    print(f"Found {len(long_metas)} files with meta description > 155 chars")
    if long_metas:
        sorted_metas = sorted(long_metas, key=lambda x: -x["length"])
        print("Top 10 longest:")
        for m in sorted_metas[:10]:
            print(f"  {m['file']}: {m['length']}c")
        print()
        fixed = truncate_long_metas(long_metas, dry_run=not apply)
        print(f"\n{'(dry) ' if not apply else ''}Truncated {fixed} meta descriptions")

    # 3. Long titles (REPORT only, no auto-fix)
    print("\n" + "=" * 60)
    print("3. TITLES > 60 chars (manual review)")
    print("=" * 60)
    long_titles = find_long_titles(files)
    print(f"Found {len(long_titles)} files with title > 60 chars")
    for t in long_titles[:10]:
        print(f"  {t['file']}: {t['length']}c")
        print(f"    \"{t['title'][:80]}...\"")

    # 4. Save broken links report for IndexNow submission later
    print("\n" + "=" * 60)
    print("4. EXPORT REPORTS")
    print("=" * 60)
    report_dir = REPO / "reports" / "seo" / "autofix"
    report_dir.mkdir(parents=True, exist_ok=True)
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    with open(report_dir / f"{today}-broken-links.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "broken_url", "line"])
        writer.writeheader()
        writer.writerows(broken)
    print(f"  Saved: reports/seo/autofix/{today}-broken-links.csv")

    with open(report_dir / f"{today}-long-metas.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "length", "desc"])
        writer.writeheader()
        writer.writerows(long_metas)
    print(f"  Saved: reports/seo/autofix/{today}-long-metas.csv")

    with open(report_dir / f"{today}-long-titles.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "length", "title"])
        writer.writeheader()
        writer.writerows(long_titles)
    print(f"  Saved: reports/seo/autofix/{today}-long-titles.csv")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Broken links found: {len(broken)} {'(fixed)' if apply else '(dry run)'}")
    print(f"Long metas found: {len(long_metas)} {'(truncated)' if apply else '(dry run)'}")
    print(f"Long titles found: {len(long_titles)} (manual review needed)")
    print()
    if not apply:
        print("To apply fixes: py scripts/seo_autofix.py --apply")


if __name__ == "__main__":
    main()
