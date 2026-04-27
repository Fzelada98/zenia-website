#!/usr/bin/env python3
"""Fix landing page hero sections to match home page polish.

Adds:
- WebGL canvas animated background (hero-bg div)
- Centered hero content
- Three.js + animation.js scripts (loaded async after page load on desktop)

Idempotent: detects already-fixed pages and skips.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ES = ROOT / "es"

MARKER_ATTR = 'data-hero-fixed="true"'

# What we replace
OLD_HERO_PATTERN = re.compile(
    r'<section class="hero" style="padding: 120px 24px 80px;">\s*<div class="container">',
    re.DOTALL
)

NEW_HERO_OPEN = (
    '<section class="hero" id="hero" '+MARKER_ATTR+'>\n'
    '  <div class="hero-bg"><canvas id="glsl-canvas"></canvas><div class="hero-bg-top"></div></div>\n'
    '  <div class="container" style="position: relative; z-index: 2; text-align: center;">'
)

# Hero-cta div needs to be centered (currently uses display: flex with flex-wrap: wrap)
OLD_CTAS = re.compile(
    r'<div class="hero-ctas" style="display: flex; gap: 12px; flex-wrap: wrap;">'
)
NEW_CTAS = '<div class="hero-ctas" style="display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;">'

# Hero lead margin needs to be auto for centering
OLD_LEAD = re.compile(
    r'<p class="hero-lead" style="font-size: 1\.15rem; color: #94A3B8; max-width: 720px; line-height: 1\.7; margin: 20px 0 32px;">'
)
NEW_LEAD = '<p class="hero-lead" style="font-size: 1.15rem; color: #94A3B8; max-width: 720px; line-height: 1.7; margin: 20px auto 32px;">'

# Three.js animation loader script (inserted before </body>)
ANIMATION_SCRIPT = '''
<!-- Three.js animated hero background (desktop only, loads 3s after pageload) -->
<script>
if (window.innerWidth > 768) {
  window.addEventListener('load', function() {
    setTimeout(function() {
      var s1 = document.createElement('script');
      s1.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
      s1.onload = function() {
        setTimeout(function() {
          var s2 = document.createElement('script');
          s2.src = '/js/animation.js';
          document.body.appendChild(s2);
        }, 100);
      };
      document.body.appendChild(s1);
    }, 3000);
  });
}
</script>
'''


def fix(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    if MARKER_ATTR in html:
        return False

    original = html
    html, n1 = OLD_HERO_PATTERN.subn(NEW_HERO_OPEN, html)
    html = OLD_CTAS.sub(NEW_CTAS, html)
    html = OLD_LEAD.sub(NEW_LEAD, html)

    if n1 == 0:
        return False  # didn't match the expected pattern

    # Inject animation script before </body> (only if not already present)
    if "Three.js animated hero background" not in html:
        html = html.replace("</body>", ANIMATION_SCRIPT + "\n</body>", 1)

    if html == original:
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True


def main():
    files = sorted(ES.glob("*.html"))
    # skip index.html and standalone non-landing pages? No, all landings.
    fixed = 0
    skipped = 0
    for path in files:
        if path.name == "index.html":
            continue
        # Standalone vertical landings (without city) might have a different hero
        if fix(path):
            fixed += 1
        else:
            skipped += 1
    print(f"Fixed: {fixed}")
    print(f"Skipped (already fixed or different structure): {skipped}")


if __name__ == "__main__":
    main()
