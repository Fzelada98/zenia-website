"""
Generate programmatic landings for the AI bookkeeping vertical.
- English landings under /en/ai-bookkeeping-importer-{city}.html (USA diaspora cities)
- Spanish landings under /es/contabilidad-ia-importadora-{ciudad}.html (LATAM + USA)

Each landing leverages the published case study at /cases/whatsapp-bookkeeping-importer.html
Generates ~30 landings + appends to sitemap.xml.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_DIR = os.path.join(ROOT, "en")
ES_DIR = os.path.join(ROOT, "es")
SITEMAP = os.path.join(ROOT, "sitemap.xml")
LASTMOD = "2026-05-04"

# (slug, display name, country, locale_anchor)
USA_CITIES = [
    ("miami", "Miami, FL", "USA"),
    ("doral", "Doral, FL", "USA"),
    ("hialeah", "Hialeah, FL", "USA"),
    ("houston", "Houston, TX", "USA"),
    ("dallas", "Dallas, TX", "USA"),
    ("atlanta", "Atlanta, GA", "USA"),
    ("orlando", "Orlando, FL", "USA"),
    ("tampa", "Tampa, FL", "USA"),
    ("new-york", "New York, NY", "USA"),
    ("newark", "Newark, NJ", "USA"),
    ("los-angeles", "Los Angeles, CA", "USA"),
    ("san-diego", "San Diego, CA", "USA"),
    ("chicago", "Chicago, IL", "USA"),
    ("phoenix", "Phoenix, AZ", "USA"),
    ("charlotte", "Charlotte, NC", "USA"),
]

LATAM_CITIES = [
    ("miami", "Miami"),
    ("doral", "Doral"),
    ("houston", "Houston"),
    ("atlanta", "Atlanta"),
    ("orlando", "Orlando"),
    ("nueva-york", "Nueva York"),
    ("los-angeles", "Los Angeles"),
    ("lima", "Lima"),
    ("bogota", "Bogotá"),
    ("medellin", "Medellín"),
    ("cali", "Cali"),
    ("cdmx", "Ciudad de México"),
    ("caracas", "Caracas"),
    ("guayaquil", "Guayaquil"),
    ("santiago", "Santiago"),
]


def en_template(city_slug, city_name, related):
    title = f"AI Bookkeeping for Importers in {city_name} | WhatsApp + Live Books | ZENIA"
    desc = f"AI bookkeeping for importers and cross-border SMBs in {city_name}. WhatsApp-native assistant that turns Zelle screenshots into live bookkeeping in 8 seconds. Three cash buckets calculated automatically. Zero Excel."
    canonical = f"https://zeniapartners.com/en/ai-bookkeeping-importer-{city_slug}.html"

    faq_items = [
        ("Does this work for importers based in {c}?".format(c=city_name),
         f"Yes. We work with cross-border importers, distributors and food businesses receiving Zelle and wire transfers across the US, including {city_name}. The system adapts to local schedules, language (English and Spanish, including regional slang), and the operational rhythm of LATAM-USA trade."),
        ("How much does it cost?",
         "Standard setup is $1,500 with monthly hosting and support starting at $250. Custom multi-tenant builds for accountants serving multiple PYMEs are quoted separately."),
        ("How fast can we go live?",
         "Two to four weeks from signature. Week 1 is discovery and category mapping to your operation. Week 2 is system build (categories, dashboards, integrations). Week 3-4 is training and go-live with you and your team."),
        ("Does it integrate with my current accounting software?",
         "The system writes to a live Google Sheets repository that any external accountant can read directly. We can export to QuickBooks, Alegra, Siigo or your local ERP at month-end. Your accountant keeps their workflow."),
        ("Is my client and supplier data safe?",
         "Yes. The data lives in your private Google Sheet under your account. We never touch your books beyond the implementation. Full audit log with timestamps for every action. Compliant with US privacy standards."),
        ("Do I need technical knowledge?",
         "Zero. You forward Zelle screenshots to a WhatsApp number the way you would send a photo to a friend. The assistant handles classification, deduplication and dashboard updates. The owner provides direction; the assistant handles bookkeeping discipline."),
    ]

    faq_jsonld_items = ", ".join(
        f'{{"@type": "Question", "name": {repr(q)}, "acceptedAnswer": {{"@type": "Answer", "text": {repr(a)}}}}}'
        for q, a in faq_items
    )

    related_html = "\n            ".join(
        f'<a href="/en/ai-bookkeeping-importer-{rs}.html" class="related-link">AI bookkeeping in {rn}</a>'
        for rs, rn, _c in related
    )

    faq_html = "\n      ".join(
        f'<details class="faq-item"><summary class="faq-q">{q}</summary><div class="faq-a">{a}</div></details>'
        for q, a in faq_items
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="ZENIA">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" type="image/svg+xml" href="../assets/icons/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles/main.css">

<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Service", "name": "ZENIA AI bookkeeping for importers in {city_name}", "provider": {{"@type": "Organization", "name": "ZENIA", "url": "https://zeniapartners.com"}}, "areaServed": {{"@type": "City", "name": "{city_name}"}}, "serviceType": "AI bookkeeping for cross-border SMBs", "description": "{desc}"}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{faq_jsonld_items}]}}</script>

<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('consent','default',{{'analytics_storage':'denied','ad_storage':'denied','wait_for_update':500}});</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HP0VQSEL68"></script>
<script>gtag('js',new Date());gtag('config','G-HP0VQSEL68');</script>

<style>
  .city-badge {{ display: inline-block; padding: 6px 14px; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 999px; color: #60A5FA; font-size: 0.85rem; font-weight: 600; margin-bottom: 20px; }}
  .local-pains {{ background: rgba(239, 68, 68, 0.05); border-left: 3px solid #EF4444; padding: 24px 28px; border-radius: 0 12px 12px 0; margin: 40px 0; }}
  .local-pains h3 {{ color: #F87171; font-size: 1.1rem; margin-bottom: 16px; }}
  .local-pains ul {{ list-style: none; padding: 0; }}
  .local-pains li {{ padding: 10px 0 10px 28px; position: relative; color: #CBD5E1; }}
  .local-pains li:before {{ content: "✗"; position: absolute; left: 0; color: #EF4444; font-weight: bold; }}
  .case-callout {{ background: linear-gradient(145deg, rgba(59,130,246,0.08), rgba(99,102,241,0.04)); border: 1px solid rgba(59,130,246,0.2); border-radius: 16px; padding: 28px 32px; margin: 40px 0; }}
  .case-callout h3 {{ color: #93C5FD; font-size: 1rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; }}
  .case-callout p {{ color: #CBD5E1; line-height: 1.7; margin-bottom: 16px; }}
  .case-callout a {{ color: #60A5FA; font-weight: 600; }}
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

<nav class="nav scrolled" id="nav">
  <div class="nav-inner">
    <a href="/" class="nav-logo"><svg class="zenia-mark" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg-v)"/></svg><span class="nav-logo-text">ZENIA</span></a>
    <ul class="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/cases/whatsapp-bookkeeping-importer.html">Case Studies</a></li>
      <li><a href="/blog/">Blog</a></li>
    </ul>
    <div class="nav-right">
      <div class="nav-cta"><a href="https://calendly.com/zeladauriartef/30min" class="btn btn-primary" target="_blank" rel="noopener">Book a Call</a></div>
    </div>
  </div>
</nav>

<section class="section" style="padding: 80px 24px 40px;">
  <div class="container" style="max-width: 900px;">
    <div class="city-badge">AI Bookkeeping &middot; {city_name}</div>
    <h1 class="hero-title" style="font-size: 2.4rem; line-height: 1.2; color: #F1F5F9;">AI bookkeeping for importers and cross-border SMBs in {city_name}</h1>
    <p class="hero-lead" style="color: #CBD5E1; font-size: 1.15rem; line-height: 1.7; margin-top: 20px;">
      Forward your Zelle screenshots to WhatsApp. Get live bookkeeping with three cash buckets calculated automatically. No more late-night Excel.
    </p>
    <div style="margin-top: 28px;">
      <a href="https://calendly.com/zeladauriartef/30min" class="btn btn-primary" target="_blank" rel="noopener" style="font-size: 1.05rem;">Book a 15 min strategy call</a>
    </div>
  </div>
</section>

<section class="section" style="padding: 40px 24px;">
  <div class="container" style="max-width: 900px;">
    <div class="local-pains">
      <h3>The pain we hear from importers in {city_name}</h3>
      <ul>
        <li>Hundreds of Zelle screenshots scattered across WhatsApp threads, no central log</li>
        <li>Notion or Excel sheets that drift out of sync every week</li>
        <li>Late-night reconciliation before the close of the month</li>
        <li>No clear cash position across bank, in-transit inventory and receivables</li>
        <li>Loan and supplier debt tracked informally, monthly interest calculated mentally</li>
        <li>Multi-leg deliveries impossible to map cleanly to accounting categories</li>
      </ul>
    </div>

    <div class="case-callout">
      <h3>Real Case Study</h3>
      <p>A cross-border importer in your situation replaced their entire manual bookkeeping with a WhatsApp-native AI assistant. Captures go in, books update live, three cash buckets calculated automatically. From 6+ hours of weekly Excel to zero data-entry.</p>
      <a href="/cases/whatsapp-bookkeeping-importer.html">Read the full case study &rarr;</a>
    </div>

    <h2 class="section-title" style="margin-top: 50px; margin-bottom: 20px; color: #F1F5F9;">What you get with ZENIA in {city_name}</h2>
    <ul style="color: #CBD5E1; line-height: 1.9; padding-left: 20px;">
      <li><strong>Computer vision on every Zelle / Bank of America screenshot.</strong> Multi-transfer captures handled automatically</li>
      <li><strong>16 accounting categories</strong> tuned to import operations: client receipts, logistics, payroll, customs, transit gratuities, loan interest, capital paydowns, tanker disbursements, returns, credit sales, credit collections, fees</li>
      <li><strong>Three-bucket cash traceability</strong> calculated in real time: bank, capital in transit (trucks/inventory), accounts receivable</li>
      <li><strong>Loan tracker</strong> with original capital, monthly interest, paid-to-date and live balance for each lender</li>
      <li><strong>Revolving supplier credit</strong> modeled as a separate sub-section that updates each cycle</li>
      <li><strong>Tanker / delivery intelligence:</strong> when you report a closure (cash recovered + credit sales by client), the system distributes amounts automatically</li>
      <li><strong>Spanish + English fluency</strong>, including regional slang. Talk natural; the assistant understands</li>
      <li><strong>Multi-image batching:</strong> drop 20 captures at once, get a clean batch summary</li>
      <li><strong>Persistent context</strong> across days and time gaps; memory backed by your spreadsheet</li>
      <li><strong>Audit log with timestamps</strong> for every action (CREATE, UPDATE, DELETE), ready for tax review</li>
      <li><strong>Executive dashboard</strong> with live KPIs, daily cashflow, top fifteen clients, debt exposure, three cash buckets at the top</li>
    </ul>
  </div>
</section>

<section class="section" style="padding: 60px 24px; background: rgba(255,255,255,0.02);">
  <div class="container">
    <h2 class="section-title" id="faq" style="text-align: center; margin-bottom: 40px;">Frequently asked questions</h2>
    <div class="faq-grid">
      {faq_html}
    </div>
  </div>
</section>

<section class="section" style="padding: 60px 24px;">
  <div class="container" style="text-align: center;">
    <h2 class="section-title">Ready to put your bookkeeping on autopilot in {city_name}?</h2>
    <p style="color: #94A3B8; font-size: 1.1rem; margin: 20px 0 32px;">
      Book a 15 min strategy call. We'll walk through your operation and show you what your dashboard would look like.
    </p>
    <a href="https://calendly.com/zeladauriartef/30min" class="btn btn-primary" target="_blank" rel="noopener" style="font-size: 1.05rem;">Book a Strategy Call</a>
  </div>
</section>

<section class="section" style="padding: 40px 24px;">
  <div class="container">
    <h3 style="color: #F1F5F9; margin-bottom: 20px;">Other cities</h3>
    <div class="related-links">
      {related_html}
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-logo"><svg class="zenia-mark zenia-mark--sm" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg2-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg2-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg2-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg2-v)"/></svg><span>ZENIA</span></div>
        <p class="footer-tagline">Go Beyond</p>
      </div>
      <div class="footer-columns">
        <div class="footer-col">
          <h3 class="footer-heading">Company</h3>
          <ul>
            <li><a href="/about.html">About</a></li>
            <li><a href="/cases/whatsapp-bookkeeping-importer.html">Case Studies</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="mailto:fabrizzio.zelada@zeniapartners.com">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3 class="footer-heading">Languages</h3>
          <ul>
            <li><a href="/">English</a></li>
            <li><a href="/es/">Espa&ntilde;ol</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 ZENIA. All rights reserved.</p>
    </div>
  </div>
</footer>

</body>
</html>
"""


def es_template(city_slug, city_name, related):
    title = f"Contabilidad con IA para importadoras en {city_name} | WhatsApp + Libros vivos | ZENIA"
    desc = f"Contabilidad automatizada con IA para importadoras y PYMEs en {city_name} que reciben Zelle y transferencias. Asistente por WhatsApp que convierte capturas en libros vivos en 8 segundos. Tres buckets de efectivo calculados automaticamente. Cero Excel manual."
    canonical = f"https://zeniapartners.com/es/contabilidad-ia-importadora-{city_slug}.html"

    faq_items = [
        (f"¿Sirve para importadoras o distribuidoras en {city_name}?",
         f"Sí. Trabajamos con importadoras, distribuidoras y PYMEs de comercio cross-border que reciben Zelle y transferencias en USA y LATAM, incluida {city_name}. El sistema se adapta a tu idioma (español con modismos regionales), tu vertical y tu ritmo operativo."),
        ("¿Cuánto cuesta?",
         "El setup estándar es $1,500 USD con hosting y soporte mensual desde $250. Para contadores que llevan libros de varios PYMEs ofrecemos planes multi-tenant con cotización a medida."),
        ("¿En cuánto tiempo está operativo?",
         "Entre 2 y 4 semanas desde la firma. Semana 1 es descubrimiento y mapeo de categorías a tu operación. Semana 2 es construcción del sistema (categorías, dashboards, integraciones). Semanas 3-4 entrenamiento contigo y go-live."),
        ("¿Se integra con mi software contable actual?",
         "El sistema escribe a un repositorio vivo en Google Sheets que cualquier contador externo puede leer directamente. Exportamos a QuickBooks, Alegra, Siigo o tu ERP local al cierre del mes. Tu contador mantiene su flujo."),
        ("¿Mis datos de clientes y proveedores están seguros?",
         "Sí. La data vive en tu Google Sheet privado bajo tu cuenta. Nosotros no tocamos tus libros más allá de la implementación. Audit log completo con timestamps para cada acción. Cumple estándares de privacidad USA y GDPR."),
        ("¿Necesito conocimientos técnicos?",
         "Cero. Reenvías la captura del Zelle a un número de WhatsApp como si se la mandaras a una amiga. La asistente clasifica, deduplica y actualiza el dashboard. Tú diriges; ella se encarga de la disciplina contable."),
    ]

    faq_jsonld_items = ", ".join(
        f'{{"@type": "Question", "name": {repr(q)}, "acceptedAnswer": {{"@type": "Answer", "text": {repr(a)}}}}}'
        for q, a in faq_items
    )

    related_html = "\n            ".join(
        f'<a href="/es/contabilidad-ia-importadora-{rs}.html" class="related-link">Contabilidad IA en {rn}</a>'
        for rs, rn in related
    )

    faq_html = "\n      ".join(
        f'<details class="faq-item"><summary class="faq-q">{q}</summary><div class="faq-a">{a}</div></details>'
        for q, a in faq_items
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="es" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="ZENIA">
<meta property="og:locale" content="es_US">
<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="theme-color" content="#0A0F1C">
<link rel="icon" type="image/svg+xml" href="../assets/icons/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles/main.css">

<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Service", "name": "ZENIA contabilidad con IA para importadoras en {city_name}", "provider": {{"@type": "Organization", "name": "ZENIA", "url": "https://zeniapartners.com"}}, "areaServed": {{"@type": "City", "name": "{city_name}"}}, "serviceType": "Contabilidad automatizada con IA", "description": "{desc}"}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{faq_jsonld_items}]}}</script>

<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('consent','default',{{'analytics_storage':'denied','ad_storage':'denied','wait_for_update':500}});</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HP0VQSEL68"></script>
<script>gtag('js',new Date());gtag('config','G-HP0VQSEL68');</script>

<style>
  .city-badge {{ display: inline-block; padding: 6px 14px; background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 999px; color: #60A5FA; font-size: 0.85rem; font-weight: 600; margin-bottom: 20px; }}
  .local-pains {{ background: rgba(239, 68, 68, 0.05); border-left: 3px solid #EF4444; padding: 24px 28px; border-radius: 0 12px 12px 0; margin: 40px 0; }}
  .local-pains h3 {{ color: #F87171; font-size: 1.1rem; margin-bottom: 16px; }}
  .local-pains ul {{ list-style: none; padding: 0; }}
  .local-pains li {{ padding: 10px 0 10px 28px; position: relative; color: #CBD5E1; }}
  .local-pains li:before {{ content: "✗"; position: absolute; left: 0; color: #EF4444; font-weight: bold; }}
  .case-callout {{ background: linear-gradient(145deg, rgba(59,130,246,0.08), rgba(99,102,241,0.04)); border: 1px solid rgba(59,130,246,0.2); border-radius: 16px; padding: 28px 32px; margin: 40px 0; }}
  .case-callout h3 {{ color: #93C5FD; font-size: 1rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; }}
  .case-callout p {{ color: #CBD5E1; line-height: 1.7; margin-bottom: 16px; }}
  .case-callout a {{ color: #60A5FA; font-weight: 600; }}
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

<nav class="nav scrolled" id="nav">
  <div class="nav-inner">
    <a href="/es/" class="nav-logo"><svg class="zenia-mark" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg-v)"/></svg><span class="nav-logo-text">ZENIA</span></a>
    <ul class="nav-links">
      <li><a href="/es/">Inicio</a></li>
      <li><a href="/cases/whatsapp-bookkeeping-importer.html">Casos</a></li>
      <li><a href="/blog/">Blog</a></li>
    </ul>
    <div class="nav-right">
      <div class="nav-cta"><a href="https://calendly.com/zeladauriartef/30min" class="btn btn-primary" target="_blank" rel="noopener">Agenda llamada</a></div>
    </div>
  </div>
</nav>

<section class="section" style="padding: 80px 24px 40px;">
  <div class="container" style="max-width: 900px;">
    <div class="city-badge">Contabilidad con IA &middot; {city_name}</div>
    <h1 class="hero-title" style="font-size: 2.4rem; line-height: 1.2; color: #F1F5F9;">Contabilidad con IA para importadoras y PYMEs en {city_name}</h1>
    <p class="hero-lead" style="color: #CBD5E1; font-size: 1.15rem; line-height: 1.7; margin-top: 20px;">
      Reenvía las capturas de Zelle por WhatsApp. Recibe libros vivos con tres buckets de efectivo calculados automaticamente. Sin Excel a las 2 a.m.
    </p>
    <div style="margin-top: 28px;">
      <a href="https://calendly.com/zeladauriartef/30min" class="btn btn-primary" target="_blank" rel="noopener" style="font-size: 1.05rem;">Agenda 15 min de descubrimiento</a>
    </div>
  </div>
</section>

<section class="section" style="padding: 40px 24px;">
  <div class="container" style="max-width: 900px;">
    <div class="local-pains">
      <h3>El dolor de las importadoras y PYMEs en {city_name}</h3>
      <ul>
        <li>Capturas de Zelle dispersas en chats de WhatsApp, sin registro central</li>
        <li>Excel o Notion que se descuadran cada semana</li>
        <li>Reconciliacion mensual a las 2 a.m. antes del cierre</li>
        <li>Sin claridad de donde esta el efectivo: banco, gandolas en transito, cuentas por cobrar</li>
        <li>Prestamos y deudas con proveedores tracked manualmente, intereses calculados de cabeza</li>
        <li>Multi-tramo (camion sale, conductor cobra en ruta, ventas a credito) imposible de mapear a categorias limpias</li>
      </ul>
    </div>

    <div class="case-callout">
      <h3>Caso real publicado</h3>
      <p>Una importadora cross-border en una situacion identica reemplazo todo su flujo manual con un asistente de IA por WhatsApp. Captura entra, libros se actualizan en vivo, tres buckets de efectivo calculados automaticamente. De 6+ horas semanales en Excel a cero data-entry.</p>
      <a href="/cases/whatsapp-bookkeeping-importer.html">Lee el caso completo &rarr;</a>
    </div>

    <h2 class="section-title" style="margin-top: 50px; margin-bottom: 20px; color: #F1F5F9;">Lo que recibes con ZENIA en {city_name}</h2>
    <ul style="color: #CBD5E1; line-height: 1.9; padding-left: 20px;">
      <li><strong>Vision por computadora</strong> en cada captura de Zelle / Bank of America. Multi-transferencia automatica</li>
      <li><strong>16 categorias contables</strong> tuneadas a operacion de importacion: cobros, logistica, planilla, aduana, viaticos, intereses, capital, entregas a gandola, retornos, ventas a credito, cobros de credito, fees</li>
      <li><strong>Trazabilidad de efectivo en 3 buckets</strong> calculados en tiempo real: banco, capital en transito (gandolas), cuentas por cobrar</li>
      <li><strong>Tracker de prestamos</strong> con capital original, interes mensual, pagado YTD y saldo vivo por prestamista</li>
      <li><strong>Credito rotativo de proveedor</strong> modelado como sub-seccion separada que cambia cada ciclo</li>
      <li><strong>Inteligencia de gandolas:</strong> cuando reportas un cierre (efectivo recuperado + ventas a credito por cliente), el sistema distribuye los montos automaticamente</li>
      <li><strong>Espanol e ingles fluidos</strong> con modismos regionales (chevere, vaina, verdes, lukas, fino). Habla natural; la asistente entiende</li>
      <li><strong>Multi-imagen en lote:</strong> manda 20 capturas de una y recibe un resumen limpio</li>
      <li><strong>Memoria persistente</strong> entre dias y horas; respaldada por tu Sheet</li>
      <li><strong>Audit log con timestamps</strong> en cada accion (CREATE, UPDATE, DELETE), listo para revision fiscal</li>
      <li><strong>Dashboard ejecutivo</strong> con KPIs vivos, cashflow diario, top 15 pagadores, exposicion de deuda y los 3 buckets arriba</li>
    </ul>
  </div>
</section>

<section class="section" style="padding: 60px 24px; background: rgba(255,255,255,0.02);">
  <div class="container">
    <h2 class="section-title" id="faq" style="text-align: center; margin-bottom: 40px;">Preguntas frecuentes</h2>
    <div class="faq-grid">
      {faq_html}
    </div>
  </div>
</section>

<section class="section" style="padding: 60px 24px;">
  <div class="container" style="text-align: center;">
    <h2 class="section-title">¿Listo para poner tu contabilidad en piloto automatico en {city_name}?</h2>
    <p style="color: #94A3B8; font-size: 1.1rem; margin: 20px 0 32px;">
      Agenda una llamada de 15 minutos. Caminamos juntos por tu operacion y te mostramos como se veria tu dashboard.
    </p>
    <a href="https://calendly.com/zeladauriartef/30min" class="btn btn-primary" target="_blank" rel="noopener" style="font-size: 1.05rem;">Agenda llamada estrategica</a>
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

<footer class="footer">
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-logo"><svg class="zenia-mark zenia-mark--sm" viewBox="0 0 140 140" fill="none"><defs><linearGradient id="zg2-b" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2563EB"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient><linearGradient id="zg2-v" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366F1"/><stop offset="100%" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="28" fill="#0F172A"/><path d="M 70 18 Q 18 18 18 38 L 18 57 Q 18 63 24 63 L 88 63 Z" fill="url(#zg2-b)"/><path d="M 70 122 Q 122 122 122 102 L 122 83 Q 122 77 116 77 L 52 77 Z" fill="url(#zg2-v)"/></svg><span>ZENIA</span></div>
        <p class="footer-tagline">Go Beyond</p>
      </div>
      <div class="footer-columns">
        <div class="footer-col">
          <h3 class="footer-heading">Empresa</h3>
          <ul>
            <li><a href="/es/">Inicio</a></li>
            <li><a href="/cases/whatsapp-bookkeeping-importer.html">Casos</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="mailto:fabrizzio.zelada@zeniapartners.com">Contacto</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h3 class="footer-heading">Idiomas</h3>
          <ul>
            <li><a href="/">English</a></li>
            <li><a href="/es/">Espa&ntilde;ol</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 ZENIA. Todos los derechos reservados.</p>
    </div>
  </div>
</footer>

</body>
</html>
"""


def main():
    written_files = []

    # Generate EN landings
    for i, (slug, name, country) in enumerate(USA_CITIES):
        related = [USA_CITIES[(i + 1) % len(USA_CITIES)],
                   USA_CITIES[(i + 2) % len(USA_CITIES)],
                   USA_CITIES[(i + 3) % len(USA_CITIES)],
                   USA_CITIES[(i + 4) % len(USA_CITIES)]]
        html = en_template(slug, name, related)
        path = os.path.join(EN_DIR, f"ai-bookkeeping-importer-{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        written_files.append(("en", slug, name))

    # Generate ES landings
    for i, (slug, name) in enumerate(LATAM_CITIES):
        related = [LATAM_CITIES[(i + 1) % len(LATAM_CITIES)],
                   LATAM_CITIES[(i + 2) % len(LATAM_CITIES)],
                   LATAM_CITIES[(i + 3) % len(LATAM_CITIES)],
                   LATAM_CITIES[(i + 4) % len(LATAM_CITIES)]]
        html = es_template(slug, name, related)
        path = os.path.join(ES_DIR, f"contabilidad-ia-importadora-{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        written_files.append(("es", slug, name))

    print(f"Generated {len(written_files)} landings")
    print(f"  EN: {len(USA_CITIES)} in /en/")
    print(f"  ES: {len(LATAM_CITIES)} in /es/")

    # Update sitemap
    new_urls = []
    for lang, slug, name in written_files:
        if lang == "en":
            url = f"https://zeniapartners.com/en/ai-bookkeeping-importer-{slug}.html"
        else:
            url = f"https://zeniapartners.com/es/contabilidad-ia-importadora-{slug}.html"
        new_urls.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

    with open(SITEMAP, "r", encoding="utf-8") as f:
        sitemap_content = f.read()

    block = "\n  <!-- AI Bookkeeping landings (programmatic, vertical pivot 2026-05-04) -->\n" + "\n".join(new_urls) + "\n"
    if "AI Bookkeeping landings" not in sitemap_content:
        sitemap_content = sitemap_content.replace("</urlset>", block + "</urlset>")
        with open(SITEMAP, "w", encoding="utf-8") as f:
            f.write(sitemap_content)
        print(f"Sitemap updated with {len(new_urls)} new URLs")
    else:
        print("Sitemap already had block, skipping")


if __name__ == "__main__":
    main()
