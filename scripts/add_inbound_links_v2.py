#!/usr/bin/env python3
"""Add contextual inbound links from related blogs/landings to the 3 new pillars
(estética, restaurantes, ecommerce).

Same insertion strategy as v1 (after first <p> in <div class="blog-content">
for blogs, end of "Cómo ZENIA resuelve" section for es/ landings).
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

# pillar_url => list of (file, anchor_sentence)
PILLARS = {
    "/blog/crm-para-estetica-espana-2026.html": [
        ("blog/crm-belleza-salon-estetica.html",
         'Para una visión más profunda con comparativa de 8 software y FAQ, lee nuestra <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar de CRM para estética España 2026</a>.'),
        ("blog/fidelizacion-clientas-estetica.html",
         'La fidelización es uno de los 10 pilares del CRM moderno: revisa nuestra <a href="/blog/crm-para-estetica-espana-2026.html">guía completa CRM para estética 2026</a> con tabla comparativa de software.'),
        ("blog/programa-fidelizacion-centro-estetica-puntos.html",
         'Si quieres ver el panorama completo de CRM, no solo fidelización, lee la <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
        ("blog/gestion-citas-centro-estetica-automatica.html",
         'La gestión de citas es solo una parte del CRM moderno: revisa nuestra <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a> con comparativa de 8 software.'),
        ("blog/gestion-citas-spa-whatsapp-automatico.html",
         'Para una visión más amplia incluyendo fidelización, upselling y dashboards, lee la <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
        ("blog/crm-peluqueria-software-gestion.html",
         'Si tu centro combina peluquería con tratamientos de estética, revisa también nuestra <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética 2026</a>.'),
        ("blog/agenda-online-peluqueria-whatsapp.html",
         'La agenda online es la base, pero el CRM completo va más allá: lee nuestra <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
        ("blog/marketing-salon-de-unas-redes-sociales.html",
         'Para integrar marketing en redes con CRM y WhatsApp, revisa nuestra <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
        # City landings estética
        ("es/crm-salones-belleza-madrid.html",
         'Antes de elegir herramienta, revisa nuestra <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a> con comparativa de 8 software.'),
        ("es/crm-salones-belleza-barcelona.html",
         'Para profundizar en la decisión, lee la <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
        ("es/crm-salones-belleza-valencia.html",
         'Antes de decidir CRM, revisa la <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
        ("es/crm-spas-madrid.html",
         'Para ver el panorama completo, revisa la <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
        ("es/crm-spas-barcelona.html",
         'Para profundizar antes de elegir, lee la <a href="/blog/crm-para-estetica-espana-2026.html">guía pillar CRM para estética España 2026</a>.'),
    ],
    "/blog/crm-para-restaurantes-espana-2026.html": [
        ("blog/crm-restaurantes-guia-completa.html",
         'Esta guía cubre los fundamentos. Para una visión completa con comparativa de 8 software del mercado, revisa nuestra <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        ("blog/automatizar-reservas-restaurante-whatsapp.html",
         'La automatización de reservas es solo una de las 10 funcionalidades del CRM moderno: lee nuestra <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        ("blog/chatbot-whatsapp-restaurantes.html",
         'Para integrar el agente de IA de WhatsApp con tu CRM completo, revisa nuestra <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        ("blog/fidelizacion-clientes-restaurante-2026.html",
         'La fidelización es uno de los 10 pilares del CRM: revisa nuestra <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a> con comparativa de software.'),
        ("blog/gestion-mesas-restaurante-inteligente.html",
         'Para ver cómo se integra la gestión de mesas con CRM, fidelización y agente IA, lee la <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        ("blog/marketing-digital-restaurantes-pequenos.html",
         'Si quieres unir marketing digital con CRM y WhatsApp, revisa nuestra <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        # City landings restaurantes
        ("es/crm-restaurantes-madrid.html",
         'Antes de elegir, revisa nuestra <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a> con comparativa de 8 software.'),
        ("es/crm-restaurantes-barcelona.html",
         'Para profundizar antes de decidir, lee la <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        ("es/crm-restaurantes-valencia.html",
         'Antes de elegir CRM, revisa la <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        ("es/crm-restaurantes-sevilla.html",
         'Para profundizar en la decisión, lee la <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
        ("es/crm-restaurantes-bilbao.html",
         'Antes de elegir, revisa la <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a> con tabla comparativa.'),
        ("es/crm-restaurantes-malaga.html",
         'Para profundizar antes de decidir, lee la <a href="/blog/crm-para-restaurantes-espana-2026.html">guía pillar CRM para restaurantes España 2026</a>.'),
    ],
    "/blog/crm-para-ecommerce-espana-2026.html": [
        ("blog/automatizacion-ecommerce-ia.html",
         'La automatización es una pieza del CRM ecommerce. Para el panorama completo con comparativa de 8 software, lee nuestra <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a>.'),
        ("blog/agente-ia-ventas-ecommerce.html",
         'El agente IA es una de las 10 funcionalidades del CRM ecommerce moderno: revisa nuestra <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a>.'),
        ("blog/automatizacion-ia-pymes.html",
         'Si tu pyme es ecommerce o tienes tienda online, revisa también nuestra <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a> con tabla comparativa de 8 software.'),
        ("blog/ai-agents-business-operations.html",
         'For ecommerce-specific implementation, see our (Spanish) <a href="/blog/crm-para-ecommerce-espana-2026.html">CRM for ecommerce Spain 2026 pillar guide</a> with full software comparison.'),
        ("blog/automatizacion-retail-tiendas-ia.html",
         'Para ecommerce puro (no retail físico), revisa nuestra <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a>.'),
        ("blog/automatizacion-whatsapp-negocios.html",
         'Si tu caso es ecommerce, lee la <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a> con integraciones Shopify/Woo/Tiendanube.'),
        # City landings ecommerce
        ("es/crm-ecommerce-madrid.html",
         'Antes de elegir, revisa nuestra <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a> con comparativa de 8 software.'),
        ("es/crm-ecommerce-barcelona.html",
         'Para profundizar en la decisión, lee la <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a>.'),
        ("es/crm-ecommerce-bogota.html",
         'Antes de elegir CRM, revisa la <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a>.'),
        ("es/crm-ecommerce-cdmx.html",
         'Para ver el panorama completo, lee la <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a>.'),
        ("es/crm-ecommerce-lima.html",
         'Para profundizar antes de decidir, lee la <a href="/blog/crm-para-ecommerce-espana-2026.html">guía pillar CRM para ecommerce España 2026</a>.'),
    ],
}


def insert_blog_style(content, anchor_sentence):
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
    pattern = re.compile(r'(<h2 class="section-title"[^>]*>C[óo]mo ZENIA[^<]*</h2>.*?</section>)', re.DOTALL)
    m = pattern.search(content)
    if not m:
        pattern2 = re.compile(r'(<h2 class="section-title"[^>]*>[^<]*</h2>)', re.DOTALL)
        m = pattern2.search(content)
        if not m:
            return None
    end_pos = m.end()
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
    total_inserted = 0
    total_skipped = 0
    for pillar_url, targets in PILLARS.items():
        print(f"\n=== {pillar_url} ===")
        for fname, anchor_sentence in targets:
            path = REPO / fname
            if not path.exists():
                print(f"SKIP not found: {fname}")
                total_skipped += 1
                continue
            content = path.read_text(encoding="utf-8")
            if pillar_url in content:
                print(f"SKIP already linked: {fname}")
                total_skipped += 1
                continue

            if fname.startswith("es/"):
                new_content = insert_landing_style(content, anchor_sentence)
            else:
                new_content = insert_blog_style(content, anchor_sentence)

            if new_content is None:
                print(f"SKIP no insertion point: {fname}")
                total_skipped += 1
                continue

            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new_content)
            print(f"OK   {fname}")
            total_inserted += 1

    print(f"\n=== TOTAL: {total_inserted} inserted, {total_skipped} skipped ===")


if __name__ == "__main__":
    main()
