# -*- coding: utf-8 -*-
"""
Programmatic SEO Generator: City x Vertical landings
Generates 90 landing pages (15 cities x 6 verticals) for local SEO domination.

Pattern: /es/crm-{vertical}-{city}.html
Example: /es/crm-restaurantes-madrid.html

Each page has:
- Unique H1 with city + vertical
- City-specific lead paragraph
- City-specific pain points (business density, local competition)
- Reused vertical pain points + solution
- City-specific FAQ entries
- Links to main vertical page (for authority juice)
- Schema LocalBusiness + Service
"""

import os
import sys
import json

# Reuse shared components from generate-landings.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module

# We cannot import generate-landings.py directly (hyphen in name)
# so we exec it to get the constants/functions we need
script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generate-landings.py')
_shared = {}
with open(script_path, 'r', encoding='utf-8') as f:
    exec(f.read(), _shared)

NAV_SVG_LOGO = _shared['NAV_SVG_LOGO']
FOOTER_SVG_LOGO = _shared['FOOTER_SVG_LOGO']
WA_SVG_PATH = _shared['WA_SVG_PATH']
ICONS = _shared['ICONS']
render_nav = _shared['render_nav']
render_footer = _shared['render_footer']
render_whatsapp_float = _shared.get('render_whatsapp_float', lambda: '')
render_cookie_consent = _shared.get('render_cookie_consent', lambda: '')
render_pricing = _shared.get('render_pricing', lambda: '')
VERTICALS = _shared['VERTICALS']

# =============================================================================
# 15 CITIES WITH LOCAL CONTEXT
# =============================================================================

PROGRAMMATIC_CITIES = [
    # Spain (10)
    {
        "slug": "madrid", "city": "Madrid", "country": "España",
        "pymes": "500.000", "highlight": "capital de negocios, sector servicios lidera",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "barcelona", "city": "Barcelona", "country": "España",
        "pymes": "450.000", "highlight": "turismo, gastronomía y tech",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "valencia", "city": "Valencia", "country": "España",
        "pymes": "180.000", "highlight": "tercera ciudad, comercio local fuerte",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "sevilla", "city": "Sevilla", "country": "España",
        "pymes": "130.000", "highlight": "hub del sur, hostelería y servicios",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "malaga", "city": "Málaga", "country": "España",
        "pymes": "120.000", "highlight": "Málaga Tech Park y Costa del Sol",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "bilbao", "city": "Bilbao", "country": "España",
        "pymes": "70.000", "highlight": "industria y servicios profesionales",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "zaragoza", "city": "Zaragoza", "country": "España",
        "pymes": "85.000", "highlight": "logística, retail y manufactura",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "murcia", "city": "Murcia", "country": "España",
        "pymes": "60.000", "highlight": "agro, comercio y servicios",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "palma", "city": "Palma de Mallorca", "country": "España",
        "pymes": "55.000", "highlight": "turismo, hostelería premium",
        "locale": "es_ES", "market": "spain"
    },
    {
        "slug": "las-palmas", "city": "Las Palmas", "country": "España",
        "pymes": "50.000", "highlight": "comercio, turismo Canarias",
        "locale": "es_ES", "market": "spain"
    },
    # LATAM (5)
    {
        "slug": "lima", "city": "Lima", "country": "Perú",
        "pymes": "850.000", "highlight": "hub LATAM Pacífico, e-commerce en crecimiento",
        "locale": "es_PE", "market": "latam"
    },
    {
        "slug": "bogota", "city": "Bogotá", "country": "Colombia",
        "pymes": "600.000", "highlight": "capital financiera, fintech y retail",
        "locale": "es_CO", "market": "latam"
    },
    {
        "slug": "cdmx", "city": "Ciudad de México", "country": "México",
        "pymes": "1.200.000", "highlight": "mercado LATAM más grande, sector servicios masivo",
        "locale": "es_MX", "market": "latam"
    },
    {
        "slug": "santiago", "city": "Santiago", "country": "Chile",
        "pymes": "400.000", "highlight": "Cono Sur, tech y retail premium",
        "locale": "es_CL", "market": "latam"
    },
    {
        "slug": "buenos-aires", "city": "Buenos Aires", "country": "Argentina",
        "pymes": "700.000", "highlight": "gastronomía, servicios creativos y tech",
        "locale": "es_AR", "market": "latam"
    },
]

# =============================================================================
# 6 MAIN VERTICALS FOR PROGRAMMATIC
# =============================================================================

MAIN_VERTICAL_SLUGS = [
    "crm-restaurantes",
    "crm-gimnasios",
    "crm-salones-belleza",
    "crm-retail",
    "crm-clinicas",
    "crm-abogados",
]

VERTICAL_LABELS = {
    "crm-restaurantes": {
        "label": "restaurantes", "short": "restaurante",
        "emoji_free": "hostelería", "kw": "CRM para restaurantes"
    },
    "crm-gimnasios": {
        "label": "gimnasios", "short": "gimnasio",
        "emoji_free": "fitness", "kw": "CRM para gimnasios"
    },
    "crm-salones-belleza": {
        "label": "salones de belleza", "short": "salón",
        "emoji_free": "belleza y estética", "kw": "CRM para salones de belleza"
    },
    "crm-retail": {
        "label": "tiendas retail", "short": "tienda",
        "emoji_free": "retail y comercio", "kw": "CRM para retail"
    },
    "crm-clinicas": {
        "label": "clínicas", "short": "clínica",
        "emoji_free": "salud y wellness", "kw": "CRM para clínicas"
    },
    "crm-abogados": {
        "label": "despachos de abogados", "short": "despacho",
        "emoji_free": "servicios legales", "kw": "CRM para abogados"
    },
}


# =============================================================================
# HTML GENERATOR — combo city x vertical
# =============================================================================

def generate_combo_page(city, vertical_slug):
    v_meta = VERTICAL_LABELS[vertical_slug]
    vertical = next(v for v in VERTICALS if v["slug"] == vertical_slug)

    label = v_meta["label"]
    short = v_meta["short"]
    kw = v_meta["kw"]
    city_name = city["city"]
    country = city["country"]

    slug = f"{vertical_slug}-{city['slug']}"
    title = f"{kw} en {city_name} | IA y WhatsApp | ZENIA"
    # Meta title max 60
    if len(title) > 60:
        title = f"{kw} {city_name} | ZENIA"

    meta_desc = f"{kw} en {city_name}. Agente de IA para WhatsApp que automatiza reservas, ventas y seguimiento 24/7. Implementación en 5 semanas. ZENIA."[:155]

    canonical = f"https://zeniapartners.com/es/{slug}.html"
    og_url = canonical

    h1_main = f"{kw} en {city_name}"
    lead = f"Los {label} en {city_name} operan en un mercado con {city['pymes']} PYMEs: {city['highlight']}. Los que responden primero por WhatsApp y automatizan seguimiento captan más clientes y retienen mejor. ZENIA despliega ese sistema en 5 semanas."

    # City-specific pain points (tailored hooks)
    city_pains = [
        f"Tu {short} en {city_name} compite con cientos de opciones. Si no respondes en 5 minutos, el cliente ya agendó con otro.",
        f"Los clientes en {city_name} usan WhatsApp antes que email o llamada. Sin sistema omnicanal, pierdes leads todos los días.",
        f"La rotación de clientes en {label} de {city_name} es alta. Sin seguimiento automatizado, el cliente se olvida de ti y vuelve al de siempre.",
    ]

    # Generate FAQ with city-specific entries
    faqs = [
        {
            "q": f"¿ZENIA funciona para {label} en {city_name}?",
            "a": f"Sí. Operamos con {label} en toda {country}, incluido {city_name}. El agente se adapta al contexto local: horarios, idioma, canales usados por tus clientes, integraciones con plataformas locales."
        },
        {
            "q": f"¿Cuánto cuesta implementar ZENIA para mi {short} en {city_name}?",
            "a": "Plan Starter desde 297€/mes + 997€ setup único. Plan Growth 497€/mes recomendado para locales con alto volumen. Plan Enterprise a medida para cadenas con múltiples localizaciones."
        },
        {
            "q": "¿En cuánto tiempo está operativo?",
            "a": "5 semanas desde la firma. Semana 1-2: diagnóstico y configuración. Semana 3-4: entrenamiento del agente con tu catálogo y procesos. Semana 5: lanzamiento y ajustes."
        },
        {
            "q": "¿Se integra con mi herramienta actual?",
            "a": "Sí. Conectamos con WhatsApp Business API, Instagram, calendarios, CRMs existentes, Shopify, reservas online y sistemas POS más usados. Si tienes un caso específico, lo validamos en el diagnóstico."
        },
        {
            "q": f"¿Mis datos de clientes en {city_name} están seguros?",
            "a": "Sí. Cumplimos GDPR y LOPDGDD. Los datos se alojan en infraestructura europea, encriptación end-to-end, y tú eres el propietario de la base de datos."
        },
        {
            "q": f"¿Necesito conocimientos técnicos para usar ZENIA?",
            "a": "No. Nosotros configuramos, entrenamos al agente con tu operativa y te entregamos un panel simple para ver conversaciones, métricas y ajustar plantillas si quieres."
        },
    ]

    faq_html = '\n'.join([
        f'''<details class="faq-item">
          <summary class="faq-q">{faq['q']}</summary>
          <div class="faq-a">{faq['a']}</div>
        </details>'''
        for faq in faqs
    ])

    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
            }
            for faq in faqs
        ]
    }, ensure_ascii=False)

    service_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"ZENIA {kw} en {city_name}",
        "provider": {"@type": "Organization", "name": "ZENIA", "url": "https://zeniapartners.com"},
        "areaServed": {"@type": "City", "name": city_name},
        "serviceType": kw,
        "description": meta_desc
    }, ensure_ascii=False)

    # Internal links: to main vertical + 3 other cities
    other_cities = [c for c in PROGRAMMATIC_CITIES if c["slug"] != city["slug"]][:3]
    related_html = '\n'.join([
        f'<a href="/es/{vertical_slug}-{c["slug"]}.html" class="related-link">{kw} en {c["city"]}</a>'
        for c in other_cities
    ]) + f'\n<a href="/es/{vertical_slug}.html" class="related-link">{kw} (guía nacional)</a>'

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="es" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{og_url}">
<meta property="og:site_name" content="ZENIA">
<meta property="og:locale" content="{city['locale']}">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="author" content="ZENIA">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" type="image/svg+xml" href="../assets/icons/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles/main.css">

<script type="application/ld+json">{service_schema}</script>
<script type="application/ld+json">{faq_schema}</script>

<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'wait_for_update': 500
  }});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HP0VQSEL68"></script>
<script>
  gtag('js', new Date());
  gtag('config', 'G-HP0VQSEL68');
</script>

<style>
  .city-badge {{ display: inline-block; padding: 6px 14px; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 999px; color: #60A5FA; font-size: 0.85rem; font-weight: 600; margin-bottom: 20px; }}
  .local-pains {{ background: rgba(239, 68, 68, 0.05); border-left: 3px solid #EF4444; padding: 24px 28px; border-radius: 0 12px 12px 0; margin: 40px 0; }}
  .local-pains h3 {{ color: #F87171; font-size: 1.1rem; margin-bottom: 16px; }}
  .local-pains ul {{ list-style: none; padding: 0; }}
  .local-pains li {{ padding: 10px 0 10px 28px; position: relative; color: #CBD5E1; }}
  .local-pains li:before {{ content: "✗"; position: absolute; left: 0; color: #EF4444; font-weight: bold; }}
  .related-links {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 40px 0; }}
  .related-link {{ padding: 10px 16px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #94A3B8; text-decoration: none; font-size: 0.9rem; transition: all 0.3s; }}
  .related-link:hover {{ border-color: #3B82F6; color: #F1F5F9; }}
  .faq-grid {{ max-width: 800px; margin: 0 auto; }}
  .faq-item {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; }}
  .faq-q {{ font-weight: 600; color: #F1F5F9; cursor: pointer; }}
  .faq-a {{ color: #94A3B8; margin-top: 12px; line-height: 1.7; }}
</style>
</head>
<body>

{render_nav()}

<section class="hero" style="padding: 120px 24px 80px;">
  <div class="container">
    <span class="city-badge">📍 {city_name}, {country}</span>
    <h1 class="section-title" style="font-size: clamp(2rem, 5vw, 3.5rem);">
      <span class="text-gradient">{kw}</span> en {city_name}
    </h1>
    <p class="hero-lead" style="font-size: 1.15rem; color: #94A3B8; max-width: 720px; line-height: 1.7; margin: 20px 0 32px;">
      {lead}
    </p>
    <div class="hero-ctas" style="display: flex; gap: 12px; flex-wrap: wrap;">
      <a href="https://wa.me/34677612799" class="btn btn-primary">Habla con nosotros por WhatsApp</a>
      <a href="/es/#precios" class="btn btn-secondary">Ver precios</a>
    </div>
  </div>
</section>

<section class="section" style="padding: 60px 24px;">
  <div class="container">
    <div class="local-pains">
      <h3>El problema real en {city_name}</h3>
      <ul>
        <li>{city_pains[0]}</li>
        <li>{city_pains[1]}</li>
        <li>{city_pains[2]}</li>
      </ul>
    </div>

    <h2 class="section-title" style="margin-top: 60px;">Cómo ZENIA resuelve esto en {city_name}</h2>
    <p style="color: #94A3B8; line-height: 1.8; max-width: 720px;">
      Desplegamos un agente de IA personalizado para tu {short} que responde por WhatsApp 24/7 con el tono y procesos de tu negocio. Gestiona reservas, agenda, consultas y seguimiento sin que tengas que contratar más personal. Se integra con tus herramientas actuales y se entrena con tu catálogo, horarios y reglas.
    </p>

    <h3 style="margin-top: 40px; color: #F1F5F9;">Implementación en 5 semanas</h3>
    <ul style="color: #94A3B8; line-height: 1.8; padding-left: 24px;">
      <li><strong style="color: #F1F5F9;">Semana 1-2:</strong> Diagnóstico de tu operativa actual en {city_name}, mapeo de procesos, conexión de canales.</li>
      <li><strong style="color: #F1F5F9;">Semana 3-4:</strong> Entrenamiento del agente con tu catálogo, tono de marca, FAQs y reglas de negocio.</li>
      <li><strong style="color: #F1F5F9;">Semana 5:</strong> Lanzamiento, monitoreo 24/7, ajustes finos según data real.</li>
    </ul>
  </div>
</section>

<section class="section" style="padding: 60px 24px; background: rgba(255,255,255,0.02);">
  <div class="container">
    <h2 class="section-title">Preguntas frecuentes</h2>
    <div class="faq-grid">
      {faq_html}
    </div>
  </div>
</section>

<section class="section" style="padding: 60px 24px;">
  <div class="container" style="text-align: center;">
    <h2 class="section-title">¿Listo para automatizar tu {short} en {city_name}?</h2>
    <p style="color: #94A3B8; font-size: 1.1rem; margin: 20px 0 32px;">
      Habla con nosotros por WhatsApp y te mostramos cómo sería tu agente de IA en acción.
    </p>
    <a href="https://wa.me/34677612799" class="btn btn-primary" style="font-size: 1.05rem;">Empezar por WhatsApp</a>
  </div>
</section>

<section class="section" style="padding: 40px 24px;">
  <div class="container">
    <h3 style="color: #F1F5F9; margin-bottom: 20px;">Otras ciudades</h3>
    <div class="related-links">
      {related_html}
    </div>
  </div>
</section>

{render_footer()}
</body>
</html>'''


# =============================================================================
# GENERATE
# =============================================================================

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))
    count = 0
    for city in PROGRAMMATIC_CITIES:
        for vertical_slug in MAIN_VERTICAL_SLUGS:
            slug = f"{vertical_slug}-{city['slug']}"
            filepath = os.path.join(output_dir, f"{slug}.html")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(generate_combo_page(city, vertical_slug))
            count += 1
            print(f"  [{count}] Created: es/{slug}.html")

    print(f"\n✓ Total: {count} city x vertical programmatic landings generated")
