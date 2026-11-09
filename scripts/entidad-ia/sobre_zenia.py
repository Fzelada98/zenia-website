#!/usr/bin/env python3
"""Genera es/sobre-zenia.html: la página «quiénes somos» en español (nov-2026).

Es la página que recuperan ChatGPT, Gemini, Claude o Perplexity cuando alguien pregunta qué es
Zenia Partners o quién hace agentes de IA y CRM por WhatsApp para pymes: datos verificables
(qué hace, precios, plazo, países, casos con cifras, fundador, contacto), respuesta primero y
FAQ con su JSON-LD. Usa el esqueleto de una landing nacional (menú, pie, cookies, beacon de
leads, formulario) y la capa de conversión le pone después la marca y la barra fija.
Uso: python3 scripts/entidad-ia/sobre_zenia.py [RAÍZ]
"""
import html as hm
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


capa = cargar('capa', os.path.join(AQUI, '..', 'capa-conversion', 'aplicar.py'))
ent = cargar('ent', os.path.join(AQUI, 'aplicar.py'))

URL = 'https://zeniapartners.com/es/sobre-zenia.html'
TITULO = 'Sobre Zenia Partners: CRM a medida y agentes de IA | ZENIA'
DESC = ('Zenia Partners es una agencia de IA en Madrid que construye CRM a medida y agentes de IA por WhatsApp '
        'para pymes de España y Latinoamérica. Precios, plazos y casos reales.')
WA = capa.wa('Hola, vengo de la página «Sobre Zenia Partners» y quiero más información')

FAQ = [
    ('¿Qué es Zenia Partners?',
     'Una agencia de inteligencia artificial con sede en Madrid que construye, para cada negocio, un CRM a medida y un agente de IA que atiende, agenda y vende por WhatsApp las 24 horas. Trabaja con pymes de España y Latinoamérica.'),
    ('¿Cuánto cuesta?',
     'Los precios están publicados: Starter 297 € al mes, Growth 497 € al mes (incluye el agente de IA por WhatsApp) y Enterprise desde 897 € al mes, más un setup único de 997 € y una permanencia mínima de 3 meses.'),
    ('¿Cuánto tarda en estar funcionando?',
     'Unas cinco semanas desde la firma: diagnóstico y conexión de canales, diseño del CRM y entrenamiento del agente, y lanzamiento con ajustes sobre datos reales.'),
    ('¿Funciona con las herramientas que ya uso?',
     'Sí. Se conecta con WhatsApp Business API, Instagram, calendarios, CRMs existentes, sistemas de reservas, TPV y las herramientas habituales de cada sector. Los casos concretos se validan en el diagnóstico.'),
    ('¿Es un bot de respuestas fijas?',
     'No. Es un agente de IA entrenado con la información del negocio: entiende el mensaje, consulta disponibilidad, registra al cliente en el CRM y pasa a una persona del equipo lo que no debe resolver solo.'),
    ('¿En qué países trabajan?',
     'En España y en toda Latinoamérica de habla hispana (Perú, México, Colombia, Chile, Argentina, Ecuador, Uruguay y Bolivia), y también con clientes en Estados Unidos y Suiza. En español y en inglés.'),
    ('¿Mis datos están seguros?',
     'Sí. Se cumple el RGPD y la normativa local, los datos se alojan en infraestructura europea con cifrado y el cliente es el propietario de su base de datos.'),
]

QUE = [
    ('CRM a medida', 'Diseñado alrededor de cómo vende y atiende tu negocio: ficha de cada cliente, historial, citas o reservas, campañas y seguimiento automático. No una plantilla adaptada a la fuerza.'),
    ('Agente de IA por WhatsApp', 'Propio para tu negocio, sobre WhatsApp Business API. Responde en segundos a cualquier hora, cualifica, agenda, confirma, recuerda y recupera clientes, con el tono de tu marca.'),
    ('Integración con lo que ya usas', 'Agenda, catálogo, reservas, pagos o tu CRM actual. El agente trabaja dentro de tus herramientas en lugar de obligarte a cambiarlas.'),
]
PASOS = [
    ('01', 'Diagnóstico', 'Semanas 1 y 2: entendemos tu operativa, mapeamos procesos y conectamos los canales.'),
    ('02', 'CRM y agente', 'Semanas 3 y 4: diseñamos el CRM y entrenamos al agente con tu catálogo, horarios y reglas.'),
    ('03', 'Lanzamiento', 'Semana 5: sale en vivo y ajustamos con datos reales de tus clientes.'),
]
CIUDADES = [('Madrid', 'crm-madrid'), ('Barcelona', 'crm-barcelona'), ('Valencia', 'crm-valencia'), ('Lima', 'crm-lima'),
            ('Ciudad de México', 'crm-cdmx'), ('Monterrey', 'crm-monterrey'), ('Bogotá', 'crm-bogota'), ('Medellín', 'crm-medellin'),
            ('Santiago', 'crm-santiago'), ('Buenos Aires', 'crm-buenos-aires'), ('Montevideo', 'crm-montevideo'),
            ('Quito', 'crm-quito'), ('Guayaquil', 'crm-guayaquil'), ('Miami', 'crm-miami')]


def cuerpo():
    e = hm.escape
    btn_wa = (f'<a href="{e(WA)}" class="btn btn-primary" target="_blank" rel="noopener">Escríbenos por WhatsApp</a>')
    hero = (
        '<section class="hero" id="hero">\n  <div class="hero-bg"><div class="hero-bg-top"></div></div>\n'
        '  <div class="container" style="position: relative; z-index: 2; text-align: center;">\n'
        '    <span class="city-badge">Agencia de IA · Madrid</span>\n'
        '    <h1 class="section-title">Zenia Partners <span class="text-gradient">CRM a medida y agentes de IA</span></h1>\n'
        '    <p class="hero-subtitle">Somos una agencia de inteligencia artificial con sede en Madrid. Para cada negocio construimos '
        'un CRM hecho a su medida y un agente de IA que atiende, agenda y vende por WhatsApp las 24 horas. Trabajamos con pymes de '
        'España y Latinoamérica.</p>\n'
        f'    <div class="hero-actions">{btn_wa}<a href="/es/casos.html" class="btn btn-secondary">Ver casos reales</a></div>\n'
        '  </div>\n</section>\n')
    cards = ''.join(f'<div class="opp-card"><h3>{t}</h3><p>{d}</p></div>' for t, d in QUE)
    que = ('\n<section class="section" id="que-hacemos">\n  <div class="container">\n'
           '    <h2 class="section-title">Qué hacemos</h2>\n'
           '    <p class="section-desc">Dos piezas que trabajan juntas, montadas para tu negocio y funcionando en unas cinco semanas.</p>\n'
           f'    <div class="opp-grid" style="margin-top:40px">{cards}</div>\n  </div>\n</section>\n')
    pasos = ''.join(f'<div class="process-step"><div class="step-number">{n}</div><h3>{t}</h3><p>{d}</p></div>' for n, t, d in PASOS)
    como = ('\n<section class="section" id="como-trabajamos">\n  <div class="container text-center">\n'
            '    <h2 class="section-title">Cómo trabajamos</h2>\n'
            '    <p class="section-desc">Pocos clientes a la vez, como mucho tres implantaciones simultáneas, para que cada proyecto tenga atención directa.</p>\n'
            f'    <div class="process-steps" style="grid-template-columns:repeat(3,1fr);margin-top:48px">{pasos}</div>\n  </div>\n</section>\n')
    chips = ''.join(f'<a href="/es/{s}.html" class="related-link">{c}</a>' for c, s in CIUDADES if os.path.exists(f'es/{s}.html'))
    donde = ('\n<section class="section" id="donde">\n  <div class="container">\n'
             '    <h2 class="section-title">Dónde trabajamos</h2>\n'
             '    <p class="section-desc">En España y en toda Latinoamérica de habla hispana, y con clientes en Estados Unidos y Suiza. '
             'Trabajamos en remoto, en español y en inglés.</p>\n'
             f'    <div class="related-links">{chips}<a href="/es/cobertura.html" class="related-link">Todas las ciudades y sectores</a></div>\n'
             '    <h3 style="margin-top:48px">Quién está detrás</h3>\n'
             '    <p>Zenia Partners la fundó Fabrizzio Zelada Uriarte en Madrid en 2025. Escríbele directamente a '
             '<a href="mailto:fabrizzio.zelada@zeniapartners.com">fabrizzio.zelada@zeniapartners.com</a> o por '
             f'<a href="{e(WA)}" target="_blank" rel="noopener">WhatsApp</a>.</p>\n  </div>\n</section>\n')
    faqs = ''.join(f'<details class="faq-item"><summary class="faq-q">{q}</summary><div class="faq-a">{a}</div></details>' for q, a in FAQ)
    faq = ('\n<section class="section" id="faq" style="background: rgba(255,255,255,0.02);">\n  <div class="container">\n'
           '    <h2 class="section-title">Preguntas frecuentes</h2>\n'
           f'    <div class="faq-grid">{faqs}</div>\n  </div>\n</section>\n')
    cierre = ('\n<section class="section">\n  <div class="container" style="text-align: center;">\n'
              '    <h2 class="section-title">¿Hablamos de tu negocio?</h2>\n'
              '    <p class="section-desc">Cuéntanos cómo trabajas hoy y te enseñamos cómo sería tu CRM y tu agente. Te respondemos en menos de 24 h.</p>\n'
              f'    <div class="hero-actions" style="margin-top:32px">{btn_wa}'
              '<a href="https://calendly.com/zeladauriartef/30min" class="btn btn-secondary" target="_blank" rel="noopener">Agendar una llamada de 30 min</a></div>\n'
              '  </div>\n</section>\n')
    return (hero + que + como + capa.planes_html('Sobre Zenia Partners') + donde + faq + cierre)


def ldjson():
    about = {'@context': 'https://schema.org', '@type': 'AboutPage', '@id': URL + '#pagina', 'name': 'Sobre Zenia Partners',
             'url': URL, 'inLanguage': 'es', 'description': DESC, 'mainEntity': {'@id': ent.ID},
             'isPartOf': {'@type': 'WebSite', '@id': 'https://zeniapartners.com/#website'}}
    org = {'@context': 'https://schema.org', **ent.org('es')}
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': 'es',
           'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    bloques = [json.dumps(x, ensure_ascii=False).replace('</', '<\\/') for x in (about, org, faq)]
    return '\n'.join('<script type="application/ld+json">' + j + '</script>' for j in bloques)


def main(raiz='.'):
    os.chdir(raiz)
    base = capa.quitar_bloques(open('es/crm-madrid.html', encoding='utf-8').read())
    head, body = base.split('</head>', 1)
    # cabecera: título, descripción, canónica, idiomas, tarjetas para compartir y datos estructurados
    head = re.sub(r'<title>[^<]*</title>', f'<title>{TITULO}</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + DESC, head)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{URL}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', head)
    head = head.replace(f'<link rel="canonical" href="{URL}">',
                        f'<link rel="canonical" href="{URL}">\n<link rel="alternate" hreflang="es" href="{URL}">\n'
                        '<link rel="alternate" hreflang="en" href="https://zeniapartners.com/about.html">\n'
                        '<link rel="alternate" hreflang="x-default" href="https://zeniapartners.com/about.html">')
    for prop in ('og:title', 'twitter:title'):
        head = re.sub(r'(<meta (?:property|name)="' + prop + r'" content=")[^"]*', lambda m: m.group(1) + TITULO, head)
    for prop in ('og:description', 'twitter:description'):
        head = re.sub(r'(<meta (?:property|name)="' + prop + r'" content=")[^"]*', lambda m: m.group(1) + DESC, head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + URL, head)
    head = re.sub(r'(<meta (?:property|name)="(?:og|twitter):image" content=")[^"]*',
                  lambda m: m.group(1) + 'https://zeniapartners.com/assets/images/og-home-es.jpg', head)
    head = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="profile">', head)
    head = re.sub(r'<script type="application/ld\+json".*?</script>\s*', '', head, flags=re.S)
    head = head.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', ldjson() + '\n\n<link rel="preconnect" href="https://fonts.googleapis.com">', 1)
    # cuerpo: mismo menú y pie; entre medias, el contenido de esta página
    i = body.find('<section class="hero"'); j = body.find('<footer')
    nav = body[:i].replace('href="#solucion"', 'href="#que-hacemos"').replace('>Solucion<', '>Qué hacemos<').replace('href="#precios"', 'href="#planes"')
    pie = body[j:]
    # el acordeón viejo de la plantilla espera h3+p; aquí las preguntas son <details> nativos
    pie = pie.replace("document.querySelectorAll('.faq-item').forEach", "document.querySelectorAll('.faq-item:not(details)').forEach")
    out = head + '</head>' + nav + cuerpo() + '\n' + pie
    open('es/sobre-zenia.html', 'w', encoding='utf-8').write(out)
    return 'es/sobre-zenia.html'


if __name__ == '__main__':
    print(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
