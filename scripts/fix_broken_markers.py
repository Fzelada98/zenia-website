#!/usr/bin/env python3
"""Fix broken HTML markers that ended up inside tag attributes.

Replaces:
- `<section class="hero" id="hero" <!-- ZENIA_HERO_FIXED -->>` (invalid)
- `<section class="section" style="...; <!-- ZENIA_INTERNAL_LINKS_BLOGS -->">` (invalid CSS)
- `<div ... <!-- ZENIA_INTERNAL_LINKS_LANDINGS -->">` (invalid CSS)

With clean data-attributes:
- `<section class="hero" id="hero" data-hero-fixed="true">`
- `<section class="section" style="..." data-zenia-internal-links="blogs">`
- `<div ... data-zenia-internal-links="landings">`
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ES = ROOT / "es"
BLOG = ROOT / "blog"


def fix_file(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    original = html

    # Fix hero marker: `id="hero" <!-- ZENIA_HERO_FIXED -->>` -> `id="hero" data-hero-fixed="true">`
    html = re.sub(
        r'<section class="hero" id="hero" <!-- ZENIA_HERO_FIXED -->>',
        '<section class="hero" id="hero" data-hero-fixed="true">',
        html
    )

    # Fix internal links blogs marker (in style attribute on <section>)
    html = re.sub(
        r'<section class="section" style="padding: 40px 24px; <!-- ZENIA_INTERNAL_LINKS_BLOGS -->">',
        '<section class="section" style="padding: 40px 24px;" data-zenia-internal-links="blogs">',
        html
    )

    # Fix internal links landings marker (in style attribute on <div>)
    html = re.sub(
        r'(<div style="background: rgba\(255,255,255,0\.04\); border: 1px solid rgba\(255,255,255,0\.08\); border-radius: 12px; padding: 24px; margin: 40px 0;) <!-- ZENIA_INTERNAL_LINKS_LANDINGS -->">',
        r'\1" data-zenia-internal-links="landings">',
        html
    )

    if html == original:
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    fixed = 0
    for path in list(ES.glob("*.html")) + list(BLOG.glob("*.html")):
        if fix_file(path):
            fixed += 1
    print(f"Fixed {fixed} files")


if __name__ == "__main__":
    main()
