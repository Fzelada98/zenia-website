#!/usr/bin/env python3
"""Add contextual inbound links to the new gimnasios pillar page from related content.

Inserts a contextual sentence linking to /blog/crm-para-gimnasios-espana-2026.html
into 8 gimnasios blog posts + top 5 city landings.

Each insertion is placed inside `<div class="blog-content">` after the first paragraph
to maximize SEO weight (in-body links beat sidebar links).
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent
PILLAR_URL = "/blog/crm-para-gimnasios-espana-2026.html"

# (file, custom anchor sentence to insert)
TARGETS = [
    ("blog/crm-gimnasio-guia.html",
     'Si buscas un punto de partida más amplio antes de profundizar en este tema, revisa nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar de CRM para gimnasios España 2026</a>, donde comparamos 8 software del mercado.'),
    ("blog/crm-gimnasios-fitness.html",
     'Para una visión más completa con tabla comparativa de 8 software, lee nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar CRM para gimnasios 2026</a>.'),
    ("blog/automatizar-cobros-gimnasio-whatsapp.html",
     'La automatización de cobros es solo una parte del CRM moderno: nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía completa de CRM para gimnasios 2026</a> cubre las 10 funcionalidades imprescindibles + comparativa de software.'),
    ("blog/captacion-leads-gimnasio-instagram-whatsapp.html",
     'Una vez captas el lead, el CRM cierra el ciclo: revisa nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar de CRM para gimnasios España 2026</a> para ver cómo se gestiona el funnel completo.'),
    ("blog/customer-retention-gym-ai.html",
     'For a comprehensive guide on selecting the right CRM (Spanish), see our <a href="/blog/crm-para-gimnasios-espana-2026.html">CRM for Gyms Spain 2026 pillar</a> with full software comparison.'),
    ("blog/retencion-clientes-gimnasio-ia.html",
     'La retención es uno de los 10 pilares de un buen CRM gym. Lee nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía completa CRM para gimnasios España 2026</a> para ver el resto.'),
    ("blog/retencion-socios-gimnasio-estrategias.html",
     'Estas 7 estrategias funcionan mejor cuando el CRM las soporta de fábrica. Nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar CRM para gimnasios 2026</a> compara 8 software para identificar cuál encaja con tu operativa.'),
    ("blog/software-gestion-gimnasio-2026.html",
     'Si quieres una comparativa más profunda con tabla de 8 software y FAQ, revisa nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar de CRM para gimnasios España 2026</a>.'),
    # City landings (top 5)
    ("es/crm-gimnasios-madrid.html",
     'Si quieres profundizar en cómo elegir CRM antes de decidir, revisa la <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar CRM para gimnasios España 2026</a>.'),
    ("es/crm-gimnasios-barcelona.html",
     'Para una visión más completa con comparativa de software, lee la <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar CRM para gimnasios España 2026</a>.'),
    ("es/crm-gimnasios-bilbao.html",
     'Antes de decidir CRM, revisa nuestra <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar de CRM para gimnasios España 2026</a> con comparativa de 8 software.'),
    ("es/crm-gimnasios-valencia.html",
     'Para profundizar en la decisión, revisa la <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar CRM para gimnasios España 2026</a>.'),
    ("es/crm-gimnasios-malaga.html",
     'Para profundizar antes de elegir, revisa la <a href="/blog/crm-para-gimnasios-espana-2026.html">guía pillar CRM para gimnasios España 2026</a> con tabla comparativa de software.'),
]


def insert_blog_style(content, anchor_sentence):
    """For blog/ files with <div class='blog-content'>"""
    pattern = re.compile(
        r'(<div class="blog-content">\s*(?:<[^>]+>\s*)*?<p>[^<]*(?:<[^/p][^>]*>[^<]*</[^>]+>)*[^<]*</p>)',
        re.DOTALL
    )
    m = pattern.search(content)
    if not m:
        pattern2 = re.compile(r'(<div class="blog-content">)')
        m = pattern2.search(content)
        if not m:
            return None
    new_paragraph = f'\n\n    <p class="pillar-callout"><strong>Lee también:</strong> {anchor_sentence}</p>\n'
    return content[:m.end()] + new_paragraph + content[m.end():]


def insert_landing_style(content, anchor_sentence):
    """For es/ city landings with <section class='section'> structure.
    Insert paragraph at the end of the 'Cómo ZENIA resuelve esto' section,
    right before the closing </section>."""
    # Find the closing </ul> after the "Implementación" section, then </div> </section>
    # Simpler: find the second </section> (after hero + first content section)
    pattern = re.compile(r'(<h2 class="section-title"[^>]*>C[óo]mo ZENIA[^<]*</h2>.*?</section>)', re.DOTALL)
    m = pattern.search(content)
    if not m:
        # Fallback: insert after first H2
        pattern2 = re.compile(r'(<h2 class="section-title"[^>]*>[^<]*</h2>)', re.DOTALL)
        m = pattern2.search(content)
        if not m:
            return None
    # Insert just before the </section> at the end of the matched block
    end_pos = m.end()
    # Find the actual position of </section> within the match
    section_close_pos = content.rfind("</section>", m.start(), end_pos)
    if section_close_pos == -1:
        section_close_pos = end_pos
    new_paragraph = (
        f'\n  <div class="container" style="margin-top: 24px;">\n'
        f'    <p style="color: #94A3B8; line-height: 1.8; max-width: 720px; padding: 16px 20px; '
        f'border-left: 3px solid #6366F1; background: rgba(99, 102, 241, 0.08);">'
        f'<strong style="color: #F1F5F9;">Lee también:</strong> {anchor_sentence}</p>\n  </div>\n'
    )
    return content[:section_close_pos] + new_paragraph + content[section_close_pos:]


def main():
    inserted = 0
    skipped = 0
    for fname, anchor_sentence in TARGETS:
        path = REPO / fname
        if not path.exists():
            print(f"SKIP not found: {fname}")
            skipped += 1
            continue
        content = path.read_text(encoding="utf-8")
        if PILLAR_URL in content and fname != "blog/crm-para-gimnasios-espana-2026.html":
            print(f"SKIP already linked: {fname}")
            skipped += 1
            continue

        if fname.startswith("es/"):
            new_content = insert_landing_style(content, anchor_sentence)
        else:
            new_content = insert_blog_style(content, anchor_sentence)

        if new_content is None:
            print(f"SKIP no insertion point: {fname}")
            skipped += 1
            continue

        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_content)
        print(f"OK   {fname}")
        inserted += 1

    print(f"\nDone. {inserted} inserted, {skipped} skipped.")


if __name__ == "__main__":
    main()
