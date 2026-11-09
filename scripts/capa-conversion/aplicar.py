#!/usr/bin/env python3
"""ZENIA, capa de conversión para landings y blog (nov-2026).

Uso:  python3 scripts/capa-conversion/aplicar.py [RAÍZ_DEL_SITIO] [--solo ruta1 ruta2 ...]

Qué hace, página por página (es IDEMPOTENTE: los bloques van entre marcas <!--zx:…-->
y se rehacen en cada pasada, así que cambiar un texto aquí y volver a correrlo actualiza
todas las páginas sin duplicar nada):

  Todas    cabecera con las fuentes de la portada, la hoja /assets/zx-*.css y tres <meta>
           que lee /assets/zx.js (tipo de página, «tu clínica», enlace de WhatsApp);
           /assets/zx.js al final (barra fija + origen de cada lead).
  Landings de ciudad (es/crm-<sector>-<ciudad>.html, 495):
           red de nodos de la portada en lugar del fondo three.js, línea «te respondemos
           en menos de 24 h» bajo los botones, franja de casos reales, llamada intermedia,
           bloque de planes (#planes) y «Ver precios» apuntando a él.
  Landings nacionales y de ciudad (es/crm-<x>.html con precios propios, 42):
           lo mismo menos el bloque de planes (ya traen el suyo).
  Contabilidad (es/contabilidad-ia-*, en/ai-bookkeeping-*), cobertura, ecommerce y
           automatización: marca + barra fija (y en las EN, beacon y formulario).
  Blog:    marca, botón del menú a WhatsApp, tarjeta de llamada a la acción antes del
           tercer H2, tablas que se deslizan dentro de su caja (antes desbordaban la
           página en el móvil) y enlaces de «Ponlo en marcha» solo en el idioma del post.

Los CSS y el JS se copian de esta carpeta a /assets con ?v=VERSION. Al cambiar el CSS o
el JS, subir VERSION para que nadie vea la hoja vieja (GitHub Pages cachea 10 minutos).
"""
import glob
import html as hm
import os
import re
import sys
import urllib.parse

VERSION = '1'
WA_NUM = '34677612799'
CAL = 'https://calendly.com/zeladauriartef/30min'
DIR = os.path.dirname(os.path.abspath(__file__))

FONTS = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600'
         '&amp;family=Space+Grotesk:wght@700&amp;display=swap">')

BEACON = ('<script>document.addEventListener("click",function(e){var t=e.target,'
          'a=t.closest?t.closest(\'a[href*="wa.me"]\'):null;if(!a)return;'
          'try{navigator.sendBeacon("https://gaia-relojes.onrender.com/gwb/lead",'
          'JSON.stringify({site:"zenia",path:location.pathname+location.search,ref:document.referrer||""}))}'
          'catch(r){}},true);</script>')
QUALIFY = '<script src="/assets/qualify.js?v=4" defer></script>'

ICO_WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88M20.46 3.49A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.42"/></svg>')
ICO_OK = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
          '<path d="M3 8.5l3.2 3L13 4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------- sectores
# Landings: el sector viene del nombre del archivo (misma lógica que el guard de SEO).
def vertical_de(s):
    toks = set(s.replace('.html', '').split('-'))
    if 'academia' in s or 'academias' in s: return 'academias'
    if 'veterinar' in s or 'peluquerias-caninas' in s: return 'veterinarias'
    if 'abogad' in s or 'despacho' in s: return 'abogados'
    if 'dentist' in s or 'dental' in s or 'odonto' in s: return 'dentistas'
    if 'fisio' in s: return 'fisios'
    if 'podolog' in s or 'clinica' in s or 'medicina-estetica' in s: return 'clinicas'
    if {'spa', 'spas'} & toks: return 'spas'
    if any(k in s for k in ('estetica', 'peluquer', 'barber', 'belleza', 'unas', 'maquillaje', 'depilacion', 'salon')): return 'salones-belleza'
    if any(k in s for k in ('gimnasio', 'crossfit', 'fitness', 'yoga', 'pilates', 'boxeo', 'entrenador')): return 'gimnasios'
    if any(k in s for k in ('restauran', 'pizzer', 'sushi', 'hamburgues', 'catering', 'asador', 'brunch', 'marisco', 'tapas')): return 'restaurantes'
    if 'cafeter' in s or 'helader' in s: return 'cafeterias'
    if any(k in s for k in ('panader', 'pasteler', 'reposter')): return 'panaderias'
    if any(k in s for k in ('hotel', 'hostal', 'alojamiento', 'camping', 'casa-rural')): return 'hoteles'
    if 'inmobiliar' in s: return 'inmobiliarias'
    if any(k in s for k in ('ecommerce', 'tienda-online', 'dropshipping')): return 'ecommerce'
    if any(k in s for k in ('consultor', 'asesor', 'gestor', 'contab', 'agencia')): return 'consultorias'
    if 'fotograf' in s: return 'fotografos'
    if 'wellness' in s or 'masaj' in s: return 'wellness'
    if any(k in s for k in ('medic', 'psicolog', 'nutricion', 'dietista', 'dermatolog', 'pediatr', 'logoped')): return 'medicos'
    if any(k in s for k in ('retail', 'tienda', 'boutique', 'joyer', 'floreria', 'floristeria', 'libreria', 'optica', 'zapateria')): return 'retail'
    return 'pymes'


NEGOCIO_ES = {
    'abogados': 'tu despacho', 'clinicas': 'tu clínica', 'dentistas': 'tu clínica dental',
    'fisios': 'tu centro de fisioterapia', 'medicos': 'tu consulta', 'veterinarias': 'tu clínica veterinaria',
    'spas': 'tu spa', 'salones-belleza': 'tu salón', 'gimnasios': 'tu gimnasio', 'restaurantes': 'tu restaurante',
    'cafeterias': 'tu cafetería', 'panaderias': 'tu panadería', 'hoteles': 'tu hotel',
    'inmobiliarias': 'tu inmobiliaria', 'ecommerce': 'tu tienda online', 'consultorias': 'tu consultora',
    'fotografos': 'tu estudio', 'wellness': 'tu centro', 'academias': 'tu academia', 'retail': 'tu tienda',
    'pymes': 'tu negocio',
}

# Frase de valor bajo el titular de cada landing de ciudad (sustituye a un párrafo de relleno
# sobre la ciudad que no vendía nada). Lo que el agente hace en ESE sector, sin cifras inventadas.
ACCION_ES = {
    'abogados': 'filtra cada consulta, agenda la primera reunión y hace seguimiento a cada caso',
    'clinicas': 'agenda citas, envía recordatorios y hace seguimiento a cada paciente',
    'dentistas': 'agenda citas, reduce las ausencias con recordatorios y recupera a los pacientes que no vuelven',
    'fisios': 'agenda sesiones, envía recordatorios y hace seguimiento a cada tratamiento',
    'medicos': 'agenda consultas, envía recordatorios y hace seguimiento a cada paciente',
    'veterinarias': 'agenda citas, recuerda las vacunas pendientes y hace seguimiento a cada mascota',
    'spas': 'gestiona reservas, vende bonos y recupera a los clientes que no vuelven',
    'salones-belleza': 'agenda citas, envía recordatorios y recupera a los clientes que no vuelven',
    'gimnasios': 'responde a los interesados, agenda la clase de prueba y recupera a los socios que dejan de venir',
    'restaurantes': 'gestiona reservas, responde dudas del menú y hace volver a tus clientes',
    'cafeterias': 'toma pedidos, responde dudas y fideliza a tus clientes con promociones',
    'panaderias': 'toma encargos, responde dudas y fideliza a tus clientes',
    'hoteles': 'responde a los huéspedes, gestiona reservas directas y ofrece mejoras antes de la llegada',
    'inmobiliarias': 'responde a cada interesado, filtra a los compradores y agenda las visitas',
    'ecommerce': 'resuelve dudas de producto, recupera carritos y hace seguimiento a cada pedido',
    'consultorias': 'filtra cada consulta, agenda la primera reunión y hace seguimiento a cada propuesta',
    'fotografos': 'responde a cada consulta, envía tarifas y agenda las sesiones',
    'wellness': 'gestiona reservas, vende bonos y recupera a los clientes que no vuelven',
    'academias': 'responde a los interesados, agenda la clase de prueba y gestiona las matrículas',
    'retail': 'responde dudas de producto, avisa de novedades y hace volver a tus clientes',
    'pymes': 'responde consultas, agenda citas y hace seguimiento a cada cliente',
}


def lead_ciudad(v, neg):
    return (f'Un agente de IA que atiende por WhatsApp 24/7: {ACCION_ES[v]}. '
            f'Todo queda en un CRM hecho a la medida de {neg}. En marcha en 5 semanas.')


# Blog: los slugs son temas («fideliza-clientes-con-whatsapp»), no sectores; el sustantivo
# solo se pone cuando el slug lo nombra sin duda. Si no, «tu negocio».
BLOG_ES = [
    (('taller',), 'tu taller'), (('autoescuela',), 'tu autoescuela'),
    (('abogad', 'despacho', 'bufete', 'extranjeria'), 'tu despacho'),
    (('dental', 'dentist', 'odonto', 'ortodon'), 'tu clínica dental'),
    (('veterinar',), 'tu clínica veterinaria'), (('fisio',), 'tu centro de fisioterapia'),
    (('psicolog', 'nutricion', 'dietista', 'podolog', 'logoped'), 'tu consulta'),
    (('clinica', 'medicina-estetica', 'medico', 'medica'), 'tu clínica'),
    (('peluquer', 'barber'), 'tu peluquería'),
    (('salon', 'unas', 'belleza', 'estetica', 'centro-de-estetica', 'maquillaje', 'depilacion'), 'tu salón'),
    (('gimnasio', 'crossfit', 'fitness'), 'tu gimnasio'), (('yoga', 'pilates'), 'tu estudio'),
    (('restaurante', 'pizzer', 'hosteler', 'sushi', 'hamburgues', 'catering'), 'tu restaurante'),
    (('cafeter',), 'tu cafetería'), (('panader', 'pasteler'), 'tu panadería'),
    (('hotel', 'hostal', 'alojamiento', 'apartamento-turistico', 'casa-rural'), 'tu alojamiento'),
    (('inmobiliar',), 'tu inmobiliaria'), (('academia', 'escuela-de'), 'tu academia'),
    (('ecommerce', 'tienda-online', 'shopify', 'woocommerce'), 'tu tienda online'),
    (('joyer', 'optica', 'florister', 'tienda-de', 'retail'), 'tu tienda'),
    (('gestoria', 'asesoria', 'contab'), 'tu asesoría'), (('consultor',), 'tu consultora'),
    (('fotograf',), 'tu estudio'), (('concesionario',), 'tu concesionario'), (('agencia',), 'tu agencia'),
]
BLOG_EN = [
    (('dental', 'dentist', 'orthodont'), 'your dental practice'),
    (('-law-', 'law-firm', 'attorney', 'lawyer', 'legal'), 'your law firm'),
    (('veterin', '-vet-', 'vet-clinic'), 'your vet clinic'),
    (('audiolog', 'physio', 'physical-therap', 'chiropract', 'optometr', 'dermatolog', 'clinic', 'medical',
      'therap', 'med-spa', 'medspa', 'practice', 'psychiatr', 'podiatr', 'pediatric', 'doctor'), 'your practice'),
    (('salon', 'barber', 'nail', 'beauty', 'lash', 'brow'), 'your salon'),
    (('-spa', 'spa-'), 'your spa'),
    (('gym', 'fitness', 'crossfit', 'martial-art', 'boxing'), 'your gym'), (('yoga', 'pilates', 'dance-studio'), 'your studio'),
    (('bakery',), 'your bakery'), (('cafe', 'coffee'), 'your café'),
    (('restaurant', 'pizzer', 'catering', 'food-truck'), 'your restaurant'),
    (('hotel', 'hostel', 'vacation-rental', 'airbnb', 'short-term-rental'), 'your property'),
    (('real-estate', 'realtor', 'property-manag', 'brokerage'), 'your agency'),
    (('hvac', 'plumb', 'roof', 'pest', 'tree-service', 'landscap', 'cleaning', 'electric', 'contractor', 'garage',
      'auto-repair', 'moving', 'pool', 'locksmith', 'solar', 'painting', 'remodel'), 'your company'),
    (('ecommerce', 'shopify', 'online-store'), 'your store'), (('retail', 'store', 'boutique', 'jewel'), 'your store'),
    (('school', 'academy', 'tutor', 'driving'), 'your school'), (('photograph',), 'your studio'),
    (('accounting', 'bookkeep', 'cpa', 'tax-'), 'your firm'), (('agency',), 'your agency'),
]


def negocio_blog(slug, en):
    s = '-' + slug.replace('.html', '') + '-'
    for claves, frase in (BLOG_EN if en else BLOG_ES):
        if any(k in s for k in claves):
            return frase
    return 'your business' if en else 'tu negocio'


# ---------------------------------------------------------------- utilidades
def texto(frag):
    return re.sub(r'\s+', ' ', hm.unescape(re.sub(r'<[^>]+>', ' ', frag))).strip()


def esc(s):
    return hm.escape(s, quote=True)


def wa(msg):
    return f'https://wa.me/{WA_NUM}?text=' + urllib.parse.quote(msg, safe='')


def bloque(nombre, contenido):
    return f'<!--zx:{nombre}-->{contenido}<!--/zx:{nombre}-->'


def quitar_bloques(h):
    return re.sub(r'<!--zx:([a-z0-9-]+)-->.*?<!--/zx:\1-->', '', h, flags=re.S)


def cierre_de(h, i, tag='div'):
    """Índice justo después del </tag> que cierra el <tag> que empieza en i."""
    pat = re.compile(r'<(/?)' + tag + r'\b', re.I)
    prof = 0
    for m in pat.finditer(h, i):
        prof += -1 if m.group(1) else 1
        if prof == 0:
            fin = h.find('>', m.end())
            return fin + 1
    return -1


def primer_wa(h, desde=0, excluir_flotante=True):
    for m in re.finditer(r'<a\b[^>]*href="(https://wa\.me/[^"]+)"[^>]*>', h[desde:]):
        if excluir_flotante and ('Contactar por WhatsApp' in m.group(0) or 'data-directo' in m.group(0)):
            continue
        return hm.unescape(m.group(1))
    return ''


# ---------------------------------------------------------------- textos
def proof_html(en):
    if en:
        items = [('/cases/global-watch-buyers-ai-acquisition.html', '831', 'WhatsApp conversations generated across 33 countries', 'Luxury watch buying'),
                 ('/cases/boutique-law-firm-latam.html', '&lt;1 min', 'response time, 24/7, across every LATAM time zone', 'Boutique law firm'),
                 ('/cases/throwin-salt-gaia-ebay-whatsapp.html', '54', 'luxury watches listed on eBay from WhatsApp in 4 weeks', 'AI agent for resale')]
        eb = 'Measured results with real clients'
    else:
        items = [('/es/caso-global-watch-buyers.html', '831', 'conversaciones de WhatsApp captadas en 33 países', 'Compra de relojes de lujo'),
                 ('/es/caso-despacho-boutique.html', '&lt;1 min', 'de respuesta, 24/7, en todos los husos horarios de LATAM', 'Despacho de abogados boutique'),
                 ('/es/caso-throwin-salt-gaia.html', '54', 'relojes de lujo publicados en eBay desde WhatsApp en 4 semanas', 'Agente de IA para reventa')]
        eb = 'Resultados medidos en clientes reales'
    lis = ''.join(f'<li><a href="{u}"><strong>{n}</strong><span>{d}</span><em>{s} &rarr;</em></a></li>' for u, n, d, s in items)
    return (f'\n<section class="zx-proof" aria-label="{esc(eb)}"><div class="container">'
            f'<p class="zx-eyebrow">{eb}</p><ul class="zx-proof-grid">{lis}</ul></div></section>\n')


def micro_html(en):
    t = 'We reply within 24 hours · No commitment' if en else 'Te respondemos en menos de 24 h · Sin compromiso'
    return f'<p class="zx-micro">{ICO_OK}<span>{t}</span></p>'


def mid_html(neg, ciudad, wa_url, en=False):
    donde = f' en {ciudad}' if ciudad else ''
    h2 = f'¿Cómo sería el agente de IA de {neg}{donde}?'
    p = ('Cuéntanos cómo trabajas hoy. Te enseñamos por WhatsApp cómo respondería tu agente, '
         'con tus horarios, tus precios y tu forma de atender.')
    return (f'\n<section class="zx-mid" aria-label="Contacto"><div class="container"><div class="zx-mid-in">'
            f'<div><p class="zx-eyebrow">Tu caso, en una conversación</p><h2>{esc(h2)}</h2><p>{p}</p></div>'
            f'<div class="zx-mid-act"><a class="zx-btn" href="{esc(wa_url)}" target="_blank" rel="noopener" data-zx-src="mid">'
            f'{ICO_WA}<span>Escríbenos por WhatsApp</span></a>'
            f'<a class="zx-link" href="{CAL}" target="_blank" rel="noopener" data-zx-src="mid-cal">o agenda una llamada de 30 min</a></div>'
            f'</div></div></section>\n')


def planes_html(pagina):
    def msg(plan):
        return wa(f'Hola, vengo de vuestra página «{pagina}» y me interesa el plan {plan}')
    planes = [
        ('Starter', 'Para empezar, con hasta 3 usuarios.', '297&nbsp;€', '/mes',
         ['CRM hasta 3 usuarios', 'Integración con WhatsApp Business', '3 automatizaciones activas', 'Soporte por email'],
         'Empezar con Starter', False),
        ('Growth', 'Para negocios en expansión.', '497&nbsp;€', '/mes',
         ['CRM hasta 10 usuarios', 'Agente de IA por WhatsApp', 'Automatizaciones ilimitadas', 'Integraciones omnicanal', 'Soporte prioritario'],
         'Empezar con Growth', True),
        ('Enterprise', 'Para varias sedes o procesos a medida.', '897&nbsp;€', '/mes o más',
         ['Usuarios ilimitados', 'Agentes de IA personalizados', 'Integraciones a medida', 'SLA garantizado', 'Customer success dedicado'],
         'Hablar con el equipo', False),
    ]
    cards = ''
    for nombre, para, precio, per, items, boton, rec in planes:
        tag = '<span class="zx-plan-tag">Recomendado</span>' if rec else ''
        lis = ''.join(f'<li>{i}</li>' for i in items)
        cls = 'zx-btn' if rec else 'zx-btn zx-ghost'
        cards += (f'<article class="zx-plan{" is-rec" if rec else ""}">{tag}<h3>{nombre}</h3><p class="zx-plan-for">{para}</p>'
                  f'<p class="zx-plan-price">{precio}<small>{per}</small></p><ul>{lis}</ul>'
                  f'<a class="{cls}" href="{esc(msg(nombre))}" target="_blank" rel="noopener" data-zx-src="plan-{nombre.lower()}">{boton}</a></article>')
    return (f'\n<section class="zx-planes" id="planes" aria-label="Planes y precios"><div class="container">'
            f'<div class="zx-planes-head"><p class="zx-eyebrow">Planes</p><h2>Planes y precios</h2>'
            f'<p>Sin sorpresas ni letra pequeña. Eliges por tamaño de equipo y el setup se paga una sola vez.</p></div>'
            f'<div class="zx-planes-grid">{cards}</div>'
            f'<p class="zx-planes-note"><strong>Setup único de 997&nbsp;€</strong>: diagnóstico, configuración, integraciones y formación del equipo. '
            f'Permanencia mínima de 3 meses.</p></div></section>\n')


def cta_blog_html(neg, wa_url, en):
    if en:
        eb, t = 'Custom CRM + AI agent', f'Want this running in {neg}?'
        p = ('We build the CRM and the AI agent that answer, book and follow up on WhatsApp, around your process and your tone. '
             'Tell us about your business and we reply within 24 hours.')
        stats = [('/cases/global-watch-buyers-ai-acquisition.html', '831', 'WhatsApp conversations generated for one client'),
                 ('/cases/boutique-law-firm-latam.html', '&lt;1 min', 'response time, 24/7, for a boutique law firm')]
        b, l, lu = 'Message us on WhatsApp', 'See client cases', '/cases/'
    else:
        eb, t = 'CRM a medida + agente de IA', f'¿Quieres esto funcionando en {neg}?'
        p = ('Montamos el CRM y el agente de IA que atienden, agendan y hacen seguimiento por WhatsApp, con tus procesos y tu tono. '
             'Cuéntanos tu caso y te respondemos en menos de 24 h.')
        stats = [('/es/caso-global-watch-buyers.html', '831', 'conversaciones de WhatsApp captadas para un cliente'),
                 ('/es/caso-despacho-boutique.html', '&lt;1 min', 'de respuesta, 24/7, en un despacho de abogados')]
        b, l, lu = 'Escríbenos por WhatsApp', 'Ver casos reales', '/es/casos.html'
    st = ''.join(f'<a href="{u}"><strong>{n}</strong><span>{d}</span></a>' for u, n, d in stats)
    return (f'\n<aside class="zx-cta" aria-label="Zenia"><p class="zx-eyebrow">{eb}</p>'
            f'<p class="zx-cta-t" role="heading" aria-level="3">{esc(t)}</p><p class="zx-cta-p">{p}</p>'
            f'<div class="zx-cta-stats">{st}</div><div class="zx-cta-act">'
            f'<a class="zx-btn" href="{esc(wa_url)}" target="_blank" rel="noopener" data-zx-src="inline">{ICO_WA}<span>{b}</span></a>'
            f'<a class="zx-link" href="{lu}">{l}</a></div></aside>\n')


def cabecera(tipo, hoja, neg, wa_url):
    metas = (f'<meta name="zx-page" content="{tipo}"><meta name="zx-negocio" content="{esc(neg)}">'
             f'<meta name="zx-wa" content="{esc(wa_url)}">')
    return bloque('head', metas + FONTS + f'<link rel="stylesheet" href="/assets/{hoja}?v={VERSION}">\n')


# ---------------------------------------------------------------- tipos de página
def tipo_de(ruta, h):
    base = os.path.basename(ruta)
    if ruta.startswith('blog/'):
        lang = re.search(r'<html[^>]*\blang="([a-zA-Z]+)', h)
        if base == 'index.html' or (lang and lang.group(1).lower()[:2] not in ('es', 'en')):
            return None          # índice del blog y posts en otros idiomas (p. ej. el italiano de Cicero): sin capa
        return 'blog'
    if ruta.startswith('en/ai-bookkeeping-') or ruta.startswith('es/contabilidad-ia-'):
        return 'contab'
    if ruta == 'es/cobertura.html':
        return 'contab'      # misma hoja que contabilidad: main.css + marca, sin bloques
    if ruta in ('es/crm-ecommerce.html', 'es/automatizacion-whatsapp-negocios.html'):
        return 'base'
    if ruta.startswith('es/crm-') and 'class="hero"' in h and '/styles/main.css' in h:
        if 'local-pains' in h and 'city-badge' in h:
            return 'ciudad'
        if 'id="precios"' in h:
            return 'nacional'
    return None


def aplicar(ruta, h, idiomas=None):
    """Devuelve el HTML con la capa aplicada (o el mismo si la página no entra)."""
    tipo = tipo_de(ruta, h)
    if not tipo or '</head>' not in h or '</body>' not in h:
        return h
    h = quitar_bloques(h)
    lang = (re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', h) or [None, 'es'])[1].lower()
    en = lang.startswith('en')
    slug = os.path.basename(ruta)
    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    h1 = texto(h1m.group(1)) if h1m else ''

    if tipo == 'blog':
        h = aplicar_blog(ruta, h, en, h1, idiomas or {})
        return h

    # ---- landings
    pagina = re.split(r'\s*[|]\s*', h1)[0].rstrip('.')[:90] or 'Zenia'
    wa_url = primer_wa(h)
    if not wa_url:
        wa_url = wa(f'Hi, I\'m coming from your page "{pagina}" and I\'d like more information' if en
                    else f'Hola, vengo de vuestra página «{pagina}» y quiero más información')
    if tipo in ('contab',):
        neg = 'your company' if en else ('tu empresa' if 'contabilidad' in ruta else 'tu negocio')
    else:
        neg = NEGOCIO_ES[vertical_de(slug.replace('crm-', '', 1))]
    hoja = 'zx-base.css' if tipo == 'base' else 'zx-landing.css'
    h = h.replace('</head>', cabecera('landing', hoja, neg, wa_url) + '</head>', 1)

    if tipo in ('ciudad', 'nacional'):
        # fondo three.js (solo escritorio, ~600 KB) -> red de nodos de la portada
        h = re.sub(r'(?:<!-- Three\.js animated hero background[^>]*-->\s*)?<script>(?:(?!</script>).)*?three\.min\.js(?:(?!</script>).)*?</script>\s*',
                   '', h, flags=re.S)
        m = re.search(r'<section class="hero"[^>]*>', h)
        if m:
            c = h.find('<div class="container"', m.end())
            if c != -1:
                h = h[:c] + bloque('net', '<div class="hero-net" aria-hidden="true"></div>') + h[c:]
        # línea de confianza bajo los botones de la portada
        m = re.search(r'<div class="(hero-ctas|hero-actions)"', h)
        if m:
            fin = cierre_de(h, m.start())
            if fin != -1:
                h = h[:fin] + bloque('micro', micro_html(en)) + h[fin:]
        # casos reales justo después de la portada
        m = re.search(r'<section class="hero"', h)
        if m:
            fin = h.find('</section>', m.end())
            if fin != -1:
                fin += len('</section>')
                h = h[:fin] + bloque('proof', proof_html(en)) + h[fin:]

    if tipo == 'ciudad':
        cb = re.search(r'class="city-badge">\s*(?:📍\s*)?([^<,]+)', h)
        ciudad = cb.group(1).strip() if cb else ''
        v = vertical_de(slug.replace('crm-', '', 1))
        h = re.sub(r'(<p class="hero-lead"[^>]*>).*?(</p>)', lambda mm: mm.group(1) + '\n      ' + lead_ciudad(v, neg) + '\n    ' + mm.group(2),
                   h, count=1, flags=re.S)
        # el alfiler 📍 de la etiqueta de ciudad no va con la marca (la etiqueta ya dice la ciudad)
        h = re.sub(r'(class="city-badge">)\s*📍\s*', r'\1', h)
        # «Ver precios» y el menú llevaban a la portada; ahora al bloque de planes de aquí
        h = h.replace('href="/es/#precios" class="btn btn-secondary"', 'href="#planes" class="btn btn-secondary"')
        if 'id="precios"' not in h:
            h = h.replace('<a href="#precios">', '<a href="#planes">')
        i = h.find('id="faq"')
        if i == -1:
            mm = re.search(r'<h2[^>]*>\s*Preguntas frecuentes', h)
            i = mm.start() if mm else -1
        s = h.rfind('<section', 0, i) if i != -1 else -1
        if s != -1:
            h = h[:s] + bloque('mid', mid_html(neg, ciudad, wa_url)) + bloque('planes', planes_html(pagina)) + h[s:]
    elif tipo == 'nacional':
        i = h.find('id="precios"')
        s = h.rfind('<section', 0, i) if i != -1 else -1
        if s != -1:
            h = h[:s] + bloque('mid', mid_html(neg, '', wa_url)) + h[s:]

    # el último botón de WhatsApp antes del pie es la llamada final: se etiqueta para medirla
    pie = h.find('<footer')
    if pie != -1 and 'data-zx-src="final"' not in h:
        ult = None
        for mm in re.finditer(r'<a href="https://wa\.me/[^"]*"[^>]*class="btn btn-primary[^"]*"', h[:pie]):
            ult = mm
        if ult and 'data-zx-src' not in ult.group(0):
            h = h[:ult.end()] + ' data-zx-src="final"' + h[ult.end():]

    if en and 'sendBeacon' not in h:
        h = h.replace('</body>', bloque('beacon', BEACON + '\n') + '</body>', 1)
    if en and 'assets/qualify.js' not in h:
        h = h.replace('</body>', bloque('qualify', QUALIFY + '\n') + '</body>', 1)
    js = f'<script src="/assets/zx.js?v={VERSION}" defer></script>'
    if tipo in ('ciudad', 'nacional'):
        js += f'<script src="/js/hero-net.js?v={VERSION}" defer></script>'
    h = h.replace('</body>', bloque('js', js + '\n') + '</body>', 1)
    return h


def aplicar_blog(ruta, h, en, h1, idiomas):
    slug = os.path.basename(ruta)
    tema = re.split(r'[:|]', h1)[0].strip()[:80] or ('this topic' if en else 'este tema')
    m = re.search(r'class="blog-cta".*?href="(https://wa\.me/[^"]+)"', h, re.S)
    wa_url = hm.unescape(m.group(1)) if m else (primer_wa(h) or wa(
        f'Hi, I read your article "{tema}" and I\'d like to see how this would work for my business' if en
        else f'Hola, he leído vuestro artículo «{tema}» y quiero ver cómo aplicarlo en mi negocio'))
    neg = negocio_blog(slug, en)
    h = h.replace('</head>', cabecera('blog', 'zx-blog.css', neg, wa_url) + '</head>', 1)

    # botón del menú: «Empezar» llevaba a la portada; ahora abre WhatsApp desde el artículo
    lbl = ('<span class="zx-l">Message us on </span>WhatsApp' if en else '<span class="zx-l">Escríbenos por </span>WhatsApp')
    nav_btn = (f'<a href="{esc(wa_url)}" class="nav-cta-btn" data-zx-src="nav" target="_blank" rel="noopener">'
               f'{ICO_WA}<span>{lbl}</span></a>')
    h = re.sub(r'<a href="[^"]*" class="nav-cta-btn"[^>]*>.*?</a>', lambda _: nav_btn, h, count=1, flags=re.S)

    # tarjeta antes del tercer H2 del artículo (o del segundo si hay pocos)
    c = h.find('<div class="blog-content">')
    if c != -1:
        fin_art = h.find('class="blog-cta"', c)
        h2s = [x.start() for x in re.finditer(r'<h2\b', h[c:fin_art if fin_art != -1 else len(h)])]
        pos = h2s[2] if len(h2s) >= 4 else (h2s[1] if len(h2s) >= 2 else None)
        if pos is not None:
            p = c + pos
            h = h[:p] + bloque('cta', cta_blog_html(neg, wa_url, en)) + h[p:]

    # tablas: dentro de su propia caja deslizable (antes ensanchaban la página en el móvil)
    if 'zx-table-in' not in h:
        hint = 'Swipe to see the full table →' if en else 'Desliza para ver la tabla completa →'
        h = re.sub(r'(<table\b.*?</table>)',
                   lambda mm: f'<div class="zx-table"><p class="zx-table-hint">{hint}</p><div class="zx-table-in">{mm.group(1)}</div></div>',
                   h, flags=re.S)

    # «Ponlo en marcha en tu negocio»: solo enlaces en el idioma del artículo
    def limpiar(mm):
        blk = mm.group(0)
        lang_post = 'en' if en else 'es'

        def ok(a):
            href = re.search(r'href="([^"]+)"', a).group(1)
            if href.startswith('/es/'):
                return lang_post == 'es'
            if href.startswith('/blog/'):
                otro = idiomas.get(os.path.basename(href))
                return otro is None or otro == lang_post
            return True
        enlaces = re.findall(r'<a\b[^>]*>.*?</a>', blk, re.S)
        buenos = [a for a in enlaces if ok(a)]
        if not buenos:
            return ''
        if len(buenos) != len(enlaces):
            for a in enlaces:
                if a not in buenos:
                    blk = blk.replace(a, '')
            blk = re.sub(r'\n\s*\n', '\n', blk)
        if en:
            blk = blk.replace('<h3>Ponlo en marcha en tu negocio</h3>', '<h3>Put it to work in your business</h3>')
        return blk
    h = re.sub(r'\n?<div class="blog-related" data-zenia-money-links="1">.*?</div>\n?', limpiar, h, flags=re.S)

    h = h.replace('</body>', bloque('js', f'<script src="/assets/zx.js?v={VERSION}" defer></script>\n') + '</body>', 1)
    return h


# ---------------------------------------------------------------- recursos
def compilar_recursos(raiz):
    base = open(os.path.join(DIR, 'zx-base.css'), encoding='utf-8').read()
    for nombre, extra in (('zx-base.css', None), ('zx-landing.css', 'zx-landing.css'), ('zx-blog.css', 'zx-blog.css')):
        out = base + ('\n' + open(os.path.join(DIR, extra), encoding='utf-8').read() if extra else '')
        open(os.path.join(raiz, 'assets', nombre), 'w', encoding='utf-8').write(out)
    js = open(os.path.join(DIR, 'zx.js'), encoding='utf-8').read()
    open(os.path.join(raiz, 'assets', 'zx.js'), 'w', encoding='utf-8').write(js)


def idiomas_blog(raiz):
    res = {}
    for f in glob.glob(os.path.join(raiz, 'blog', '*.html')):
        with open(f, encoding='utf-8') as fh:
            m = re.search(r'<html[^>]*\blang="([a-zA-Z]+)', fh.read(600))
        res[os.path.basename(f)] = (m.group(1).lower()[:2] if m else 'es')
    return res


def procesar(raiz='.', solo=None):
    compilar_recursos(raiz)
    idiomas = idiomas_blog(raiz)
    rutas = solo or sorted(glob.glob(os.path.join(raiz, 'blog', '*.html')) + glob.glob(os.path.join(raiz, 'es', '*.html'))
                           + glob.glob(os.path.join(raiz, 'en', '*.html')))
    tocados = []
    for f in rutas:
        rel = os.path.relpath(f, raiz).replace(os.sep, '/')
        with open(f, encoding='utf-8') as fh:
            h = fh.read()
        n = aplicar(rel, h, idiomas)
        if n != h:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(n)
            tocados.append(rel)
    return tocados


if __name__ == '__main__':
    args = sys.argv[1:]
    raiz = args[0] if args and not args[0].startswith('--') else '.'
    solo = None
    if '--solo' in args:
        solo = [os.path.join(raiz, x) for x in args[args.index('--solo') + 1:]]
    t = procesar(raiz, solo)
    print(f'páginas actualizadas: {len(t)}')
