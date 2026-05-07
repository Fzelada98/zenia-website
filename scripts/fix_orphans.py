#!/usr/bin/env python3
"""Fix orphan pages: detect, build /es/cobertura.html hub, link hub from main footer."""
import re
import sys
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
ES_DIR = REPO / "es"
EN_DIR = REPO / "en"
EXCLUDES = {"node_modules", ".git", "reports", "_audit_", "backend",
            "snippets", "demo", "agents", "ts-beta", "ts-preview", "lead-magnets"}

INTERNAL_HREF_RE = re.compile(r'href=["\'](/[^"\'#?]+\.html)["\']', re.IGNORECASE)
TITLE_RE = re.compile(r'<title>(.*?)</title>', re.DOTALL)


def get_pages():
    files = []
    for path in REPO.rglob("*.html"):
        rel = path.relative_to(REPO)
        if any(part in EXCLUDES or part.startswith(".") for part in rel.parts):
            continue
        files.append(path)
    return files


def url_for(path):
    return "/" + str(path.relative_to(REPO)).replace("\\", "/")


def build_inbound_map(pages):
    inbound = defaultdict(set)
    url_to_path = {url_for(p): p for p in pages}
    for src in pages:
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        src_url = url_for(src)
        for m in INTERNAL_HREF_RE.finditer(content):
            target = m.group(1)
            if target == src_url:
                continue
            if target in url_to_path:
                inbound[target].add(src_url)
    return inbound, url_to_path


def parse_title(path):
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return path.stem
    m = TITLE_RE.search(content)
    if not m:
        return path.stem
    title = m.group(1).strip()
    return title.split("|")[0].strip()


def categorize(path):
    """Return (group_key, label) for grouping in hub."""
    rel = path.relative_to(REPO)
    parts = rel.parts
    if parts[0] == "es":
        name = path.stem
        # crm-{vertical}-{city} or contabilidad-ia-importadora-{city}
        if name.startswith("crm-"):
            tail = name[4:]
            tokens = tail.split("-")
            # heuristic: vertical is first token, but salones-belleza is two
            if tokens[:1] == ["salones"] and len(tokens) >= 2 and tokens[1] == "belleza":
                vertical = "salones-belleza"
            else:
                vertical = tokens[0]
            return ("es-crm-" + vertical, "CRM " + vertical.replace("-", " ").title())
        if name.startswith("contabilidad-ia-importadora"):
            return ("es-contabilidad", "Contabilidad IA Importadoras (ES)")
        return ("es-otros", "Otros recursos en español")
    if parts[0] == "en":
        if path.stem.startswith("ai-bookkeeping-importer"):
            return ("en-bookkeeping", "AI Bookkeeping for Importers (EN)")
        return ("en-otros", "Other English resources")
    if parts[0] == "blog":
        return ("blog", "Blog")
    if parts[0] == "cases":
        return ("cases", "Case studies")
    return ("other", "Otros")


def build_hub(pages, out_path):
    groups = defaultdict(list)
    for p in pages:
        rel = p.relative_to(REPO)
        if rel.name == "index.html" and len(rel.parts) <= 2:
            continue
        if rel.name in {"unsubscribe.html", "cobertura.html"}:
            continue
        group_key, group_label = categorize(p)
        title = parse_title(p)
        groups[(group_key, group_label)].append((url_for(p), title))

    # Sort within each group by URL
    sections_html = []
    for (key, label), items in sorted(groups.items()):
        items.sort()
        links = "\n".join(
            f'      <li><a href="{url}">{title}</a></li>' for url, title in items
        )
        sections_html.append(f"""
  <section class="hub-section">
    <h2>{label} <span class="hub-count">{len(items)}</span></h2>
    <ul class="hub-list">
{links}
    </ul>
  </section>""")

    total = sum(len(v) for v in groups.values())
    body = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cobertura completa | ZENIA</title>
<meta name="description" content="Indice completo de soluciones ZENIA por vertical, ciudad y mercado. Encuentra la pagina especifica para tu sector y region.">
<link rel="canonical" href="https://zeniapartners.com/es/cobertura.html">
<link rel="alternate" hreflang="es" href="https://zeniapartners.com/es/cobertura.html">
<link rel="alternate" hreflang="x-default" href="https://zeniapartners.com/es/cobertura.html">
<meta property="og:type" content="website">
<meta property="og:title" content="Cobertura completa | ZENIA">
<meta property="og:description" content="Indice de soluciones ZENIA por vertical y ciudad.">
<meta property="og:url" content="https://zeniapartners.com/es/cobertura.html">
<meta property="og:site_name" content="ZENIA">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Cobertura completa | ZENIA">
<meta name="twitter:description" content="Indice de soluciones ZENIA por vertical y ciudad.">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" type="image/svg+xml" href="../assets/icons/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles/main.css">
<style>
  .hub-wrap {{ max-width: 1100px; margin: 100px auto 80px; padding: 0 24px; }}
  .hub-wrap h1 {{ font-size: clamp(2rem, 4vw, 2.8rem); color: #F1F5F9; margin-bottom: 12px; }}
  .hub-lead {{ color: #94A3B8; font-size: 1.05rem; max-width: 720px; line-height: 1.7; margin-bottom: 48px; }}
  .hub-section {{ margin-bottom: 56px; }}
  .hub-section h2 {{ color: #F1F5F9; font-size: 1.4rem; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; gap: 12px; }}
  .hub-count {{ font-size: 0.85rem; color: #60A5FA; background: rgba(59,130,246,0.1); padding: 2px 10px; border-radius: 999px; }}
  .hub-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 8px 24px; list-style: none; padding: 0; }}
  .hub-list li {{ padding: 6px 0; }}
  .hub-list a {{ color: #94A3B8; text-decoration: none; font-size: 0.95rem; transition: color 0.2s; }}
  .hub-list a:hover {{ color: #60A5FA; }}
</style>
</head>
<body>
<nav class="nav scrolled" id="nav">
  <div class="nav-inner">
    <a href="/es/" class="nav-logo"><svg class="zenia-mark" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg-v)"/></svg><span class="nav-logo-text">ZENIA</span></a>
    <ul class="nav-links">
      <li><a href="/es/">Inicio</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/es/cobertura.html">Cobertura</a></li>
    </ul>
    <div class="nav-right">
      <div class="nav-cta"><a href="https://wa.me/34677612799" class="btn btn-primary">WhatsApp</a></div>
    </div>
  </div>
</nav>

<main class="hub-wrap">
  <h1>Cobertura completa</h1>
  <p class="hub-lead">{total} paginas de ZENIA organizadas por vertical, ciudad y mercado. Si buscas una solucion especifica para tu sector y region, encuentra la pagina dedicada aqui.</p>
{''.join(sections_html)}
</main>

<footer style="background:#0A0F1C; padding:48px 24px; text-align:center; color:#64748B; border-top:1px solid rgba(255,255,255,0.06);">
  <p>&copy; 2026 ZENIA Partners. <a href="/es/cobertura.html" style="color:#94A3B8;">Cobertura</a> &middot; <a href="/privacy/" style="color:#94A3B8;">Privacidad</a></p>
</footer>
</body>
</html>
"""
    out_path.write_text(body, encoding="utf-8")
    return total


def link_hub_from_pages(pages, hub_url, dry_run=True):
    """Inject a footer link to the hub in any page that doesn't already link to it."""
    fixed = 0
    needle = f'href="{hub_url}"'
    footer_link = (
        f'<div style="text-align:center; padding:16px 24px; background:#0A0F1C; '
        f'color:#64748B; font-size:0.85rem; border-top:1px solid rgba(255,255,255,0.04);">'
        f'<a href="{hub_url}" style="color:#94A3B8; text-decoration:none;">Ver cobertura completa</a>'
        f'</div>'
    )
    for p in pages:
        if p.name == "cobertura.html":
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if needle in content:
            continue
        # Insert before </body>
        if "</body>" not in content:
            continue
        new_content = content.replace("</body>", footer_link + "\n</body>", 1)
        if not dry_run:
            open(p, "w", encoding="utf-8", newline="").write(new_content)
        fixed += 1
    return fixed


def update_sitemap(hub_url):
    sitemap = REPO / "sitemap.xml"
    if not sitemap.exists():
        return False
    content = sitemap.read_text(encoding="utf-8")
    full_url = "https://zeniapartners.com" + hub_url
    if full_url in content:
        return False
    entry = f"  <url>\n    <loc>{full_url}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>\n"
    content = content.replace("</urlset>", entry + "</urlset>")
    sitemap.write_text(content, encoding="utf-8")
    return True


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    pages = get_pages()
    print(f"Total pages scanned: {len(pages)}\n")

    inbound, url_to_path = build_inbound_map(pages)
    orphans = []
    for p in pages:
        u = url_for(p)
        if p.name == "index.html" and len(p.relative_to(REPO).parts) <= 2:
            continue
        if not inbound.get(u):
            orphans.append(u)
    print(f"Orphans detected (no inbound internal links): {len(orphans)}")
    for o in orphans[:10]:
        print(f"  {o}")
    if len(orphans) > 10:
        print(f"  ... +{len(orphans) - 10} more\n")

    hub_url = "/es/cobertura.html"
    hub_path = REPO / "es" / "cobertura.html"

    if apply:
        total = build_hub(pages, hub_path)
        print(f"\nHub written: {hub_path} ({total} links)")
        n = link_hub_from_pages(pages, hub_url, dry_run=False)
        print(f"Footer link added to {n} pages")
        sm = update_sitemap(hub_url)
        print(f"Sitemap updated: {sm}")
    else:
        print(f"\n(dry run) Would build {hub_path} and link from all pages.")
