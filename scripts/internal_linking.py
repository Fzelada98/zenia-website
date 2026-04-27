#!/usr/bin/env python3
"""Internal linking re-architecture for ZENIA Partners.

Adds cross-cluster links between blog posts and landings:
- Blog posts → related landings (city × vertical) of same cluster
- Landings → related blog posts of same cluster

Runs idempotent: detects existing links and skips if already present.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
ES = ROOT / "es"
TRACKER = BLOG / "content-tracker.json"

# Map cluster slug -> vertical landing slug
CLUSTER_TO_VERTICAL = {
    "restaurantes": "crm-restaurantes",
    "gimnasios": "crm-gimnasios",
    "belleza": "crm-salones-belleza",
    "estetica": "crm-salones-belleza",
    "clinicas": "crm-clinicas",
    "wellness": "crm-wellness",
    "abogados": "crm-abogados",
    "retail": "crm-retail",
    "ecommerce": "crm-ecommerce",
    "inmobiliarias": "crm-inmobiliarias",
    "academias": "crm-academias",
    "general": None,
}

# Top cities per vertical for landing recommendations
TOP_CITIES_PER_VERTICAL = {
    "crm-restaurantes": ["madrid", "barcelona", "lima"],
    "crm-gimnasios": ["madrid", "barcelona", "bogota"],
    "crm-salones-belleza": ["madrid", "barcelona", "cdmx"],
    "crm-clinicas": ["madrid", "barcelona", "lima"],
    "crm-abogados": ["madrid", "barcelona", "bogota"],
    "crm-retail": ["madrid", "barcelona", "cdmx"],
    "crm-cafeterias": ["madrid", "barcelona", "lima"],
    "crm-hoteles": ["madrid", "barcelona", "lima"],
    "crm-wellness": ["madrid", "barcelona", "lima"],
    "crm-ecommerce": ["madrid", "barcelona", "cdmx"],
    "crm-inmobiliarias": ["madrid", "barcelona", "lima"],
    "crm-academias": ["madrid", "barcelona", "lima"],
}


def load_tracker():
    with open(TRACKER, "r", encoding="utf-8") as f:
        return json.load(f)


def index_blog_by_cluster():
    """Build a map: cluster -> list of (slug, keyword) of published blog posts."""
    data = load_tracker()
    by_cluster = defaultdict(list)
    for p in data["posts"]:
        if p.get("status") == "published" and p.get("slug") != "index":
            by_cluster[p.get("cluster", "general")].append((p["slug"], p["keyword"]))
    return by_cluster


def keyword_to_anchor(keyword):
    """Capitalize first letter of each word for anchor text."""
    return keyword[0].upper() + keyword[1:] if keyword else keyword


# ---------- LANDING ENHANCEMENT ----------

LANDING_BLOG_BLOCK_MARKER = 'data-zenia-internal-links="blogs"'


def enhance_landing(path: Path, by_cluster):
    """Inject blog-related links section in a landing page."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    if LANDING_BLOG_BLOCK_MARKER in html:
        return False  # already enhanced

    # Detect cluster from filename: crm-{vertical}[-{city}].html
    name = path.stem
    cluster = None
    for c, v in CLUSTER_TO_VERTICAL.items():
        if v and (name == v or name.startswith(v + "-")):
            cluster = c
            break

    if not cluster:
        # Check direct mapping (crm-cafeterias, crm-hoteles, etc.)
        for c_key in ["cafeterias", "hoteles", "academias", "consultorias",
                       "ecommerce", "fotografos", "inmobiliarias", "medicos",
                       "wellness", "veterinarias", "dentistas", "fisios", "spas",
                       "panaderias"]:
            if name == f"crm-{c_key}" or name.startswith(f"crm-{c_key}-"):
                cluster = c_key
                break

    if not cluster:
        return False

    blogs = by_cluster.get(cluster, [])
    if not blogs:
        # Try general
        blogs = by_cluster.get("general", [])[:3]
    blogs = blogs[:3]
    if not blogs:
        return False

    links_html = "\n      ".join(
        f'<a href="/blog/{slug}.html" class="related-link">{keyword_to_anchor(kw)}</a>'
        for slug, kw in blogs
    )

    new_section = f"""
<section class="section" style="padding: 40px 24px;" {LANDING_BLOG_BLOCK_MARKER}>
  <div class="container">
    <h3 style="color: #F1F5F9; margin-bottom: 20px;">Recursos relacionados</h3>
    <div class="related-links">
      {links_html}
      <a href="/blog/" class="related-link">Ver todos los recursos →</a>
    </div>
  </div>
</section>

<footer class="footer">"""

    new_html = html.replace("<footer class=\"footer\">", new_section, 1)
    if new_html == html:
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    return True


# ---------- BLOG ENHANCEMENT ----------

BLOG_LANDING_BLOCK_MARKER = 'data-zenia-internal-links="landings"'


def enhance_blog(path: Path, by_cluster, posts_meta):
    """Inject related-landings section in a blog post."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    if BLOG_LANDING_BLOCK_MARKER in html:
        return False

    slug = path.stem
    cluster = posts_meta.get(slug, "general")
    vertical = CLUSTER_TO_VERTICAL.get(cluster)

    if not vertical:
        return False

    # Pick top 3 city-specific landings for this vertical + 1 national landing
    cities = TOP_CITIES_PER_VERTICAL.get(vertical, ["madrid", "barcelona", "lima"])
    landings = []
    for city in cities:
        landing_path = ES / f"{vertical}-{city}.html"
        if landing_path.exists():
            city_display = city.replace("-", " ").title()
            landings.append((f"/es/{vertical}-{city}.html", f"{vertical.replace('crm-', 'CRM ').replace('-', ' ').title()} en {city_display}"))
    # National
    national_path = ES / f"{vertical}.html"
    if national_path.exists():
        landings.append((f"/es/{vertical}.html", f"{vertical.replace('crm-', 'CRM ').replace('-', ' ').title()} (guía nacional)"))

    if not landings:
        return False

    links_html = "\n      ".join(
        f'<a href="{href}" style="display: inline-block; margin: 4px 8px 4px 0; padding: 8px 14px; background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3); border-radius: 8px; color: #60A5FA; text-decoration: none; font-size: 0.9rem;">{label} →</a>'
        for href, label in landings
    )

    new_section = f"""
<div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px; margin: 40px 0;" {BLOG_LANDING_BLOCK_MARKER}>
  <h3 style="color: #F1F5F9; margin-bottom: 12px; font-size: 1.05rem;">¿En qué ciudad operas?</h3>
  <p style="color: #94A3B8; margin-bottom: 16px; font-size: 0.95rem;">Personalizamos la implementación según tu mercado local. Ve la guía específica para tu ciudad:</p>
  <div>
      {links_html}
  </div>
</div>

</article>"""

    new_html = html.replace("</article>", new_section, 1)
    if new_html == html:
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_html)
    return True


def main():
    print("=== Internal linking pass ===\n")

    by_cluster = index_blog_by_cluster()
    print("Blog posts by cluster:")
    for c, posts in by_cluster.items():
        print(f"  {c}: {len(posts)} posts")
    print()

    # Build slug -> cluster map for blog enhancement
    data = load_tracker()
    posts_meta = {p["slug"]: p.get("cluster", "general") for p in data["posts"]}

    # Process landings
    landing_files = sorted(ES.glob("*.html"))
    landing_count = 0
    for path in landing_files:
        if enhance_landing(path, by_cluster):
            landing_count += 1
    print(f"Enhanced {landing_count} landings with blog cross-links")

    # Process blog posts
    blog_files = sorted([p for p in BLOG.glob("*.html") if p.name != "index.html"])
    blog_count = 0
    for path in blog_files:
        if enhance_blog(path, by_cluster, posts_meta):
            blog_count += 1
    print(f"Enhanced {blog_count} blog posts with landing cross-links")

    print(f"\nTotal pages cross-linked: {landing_count + blog_count}")


if __name__ == "__main__":
    main()
