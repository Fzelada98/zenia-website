#!/usr/bin/env python3
"""ZENIA, una sola entidad «Zenia Partners» en los datos estructurados de todo el sitio (nov-2026).

Por qué: ChatGPT, Gemini, Claude y Perplexity deciden a quién recomendar leyendo, entre otras
cosas, los datos estructurados (JSON-LD) de las páginas. El sitio declaraba la empresa ~2.000
veces como «ZENIA» (consultoría de IA genérica) y ~60 como «Zenia Partners» (agencia de agentes
de IA y CRM por WhatsApp), con dos @id distintos (#organization y #organizacion). Para un modelo
eran dos empresas, y «Zenia» a secas choca con otras marcas.

Qué hace (idempotente):
  - Las fichas completas de empresa (portadas, about, blog, casos) pasan a ser UNA: @id
    https://zeniapartners.com/#organization, nombre «Zenia Partners», alias «ZENIA», con lo que
    hace hoy (CRM a medida + agente de IA por WhatsApp), precios, países, fundador y contacto.
  - Las menciones dentro de otras fichas (publisher, provider, worksFor, author) apuntan a ese @id.
  - Fuera las fichas viejas de «consultoría integral de IA» (#service) de las portadas.
Uso: python3 scripts/entidad-ia/aplicar.py [RAÍZ]
"""
import glob
import json
import os
import re
import sys

BASE = 'https://zeniapartners.com'
ID = BASE + '/#organization'
NOMBRES = {'ZENIA', 'Zenia', 'Zenia Partners', 'ZENIA AI Consulting', 'ZENIA Consultoría IA'}
VIEJOS_ID = {BASE + '/#organization', BASE + '/#organizacion', BASE + '/#service', BASE + '/es/#service'}

PAISES = ['España', 'Perú', 'México', 'Colombia', 'Chile', 'Argentina', 'Ecuador', 'Uruguay', 'Bolivia', 'Estados Unidos']
PAISES_EN = ['Spain', 'Peru', 'Mexico', 'Colombia', 'Chile', 'Argentina', 'Ecuador', 'Uruguay', 'Bolivia', 'United States']

DESC = {
    'es': ('Zenia Partners es una agencia de inteligencia artificial con sede en Madrid que construye CRM a medida y '
           'agentes de IA que atienden, agendan y venden por WhatsApp para pymes de España y Latinoamérica. Cada '
           'agente se conecta al WhatsApp Business API y a las herramientas que el negocio ya usa. La implantación '
           'lleva unas cinco semanas y los planes empiezan en 297 € al mes.'),
    'en': ('Zenia Partners is a Madrid-based AI agency that builds custom CRMs and AI agents that answer, book and '
           'sell on WhatsApp for small and mid-sized businesses in Spain and Latin America. Each agent connects to '
           'the WhatsApp Business API and to the tools the business already uses. Rollout takes about five weeks '
           'and plans start at €297 per month.'),
}
SERVICIOS = {
    'es': [('CRM a medida', 'CRM diseñado alrededor de cómo vende y atiende cada negocio, con ficha de cliente, historial y seguimiento automático.'),
           ('Agente de IA por WhatsApp', 'Agente propio sobre WhatsApp Business API que responde en segundos las 24 horas, cualifica, agenda, confirma y recupera clientes.'),
           ('Automatización de citas, reservas y campañas', 'Recordatorios, confirmaciones, reactivación de clientes inactivos y campañas por WhatsApp.'),
           ('Desarrollo de plataformas SaaS a medida', 'Productos y paneles propios con IA en el centro, del diseño al despliegue.')],
    'en': [('Custom CRM', 'A CRM designed around how each business sells and serves customers, with client records, history and automated follow-up.'),
           ('WhatsApp AI agent', 'A dedicated agent on the WhatsApp Business API that replies in seconds, 24/7, qualifies, books, confirms and wins back customers.'),
           ('Booking, reminder and campaign automation', 'Reminders, confirmations, reactivation of inactive customers and WhatsApp campaigns.'),
           ('Custom SaaS development', 'Own products and dashboards with AI at the core, from design to deployment.')],
}
PLANES = [('Starter', '297', 'CRM hasta 3 usuarios, WhatsApp Business y 3 automatizaciones', 'CRM for up to 3 users, WhatsApp Business and 3 automations'),
          ('Growth', '497', 'CRM hasta 10 usuarios, agente de IA por WhatsApp y automatizaciones ilimitadas', 'CRM for up to 10 users, WhatsApp AI agent and unlimited automations'),
          ('Enterprise', '897', 'Usuarios ilimitados, agentes de IA personalizados e integraciones a medida (desde)', 'Unlimited users, custom AI agents and custom integrations (from)')]


def org(lang):
    es = lang != 'en'
    return {
        '@type': ['Organization', 'ProfessionalService'],
        '@id': ID,
        'name': 'Zenia Partners',
        'alternateName': ['ZENIA', 'Zenia'],
        'url': BASE + '/',
        'logo': BASE + '/assets/logos/zenia-logo.png',
        'image': BASE + ('/assets/images/og-home-es.jpg' if es else '/assets/images/og-home-en.jpg'),
        'description': DESC['es' if es else 'en'],
        'slogan': 'CRM a medida y agentes de IA por WhatsApp' if es else 'Custom CRM and WhatsApp AI agents',
        'foundingDate': '2025',
        'founder': {'@type': 'Person', 'name': 'Fabrizzio Zelada Uriarte', 'jobTitle': 'Founder' if not es else 'Fundador',
                    'sameAs': ['https://www.linkedin.com/in/fabrizziozelada/']},
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Madrid', 'addressCountry': 'ES'},
        'areaServed': [{'@type': 'Country', 'name': p} for p in (PAISES if es else PAISES_EN)],
        'email': 'fabrizzio.zelada@zeniapartners.com',
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'sales', 'email': 'fabrizzio.zelada@zeniapartners.com',
                          'url': 'https://wa.me/34677612799', 'availableLanguage': ['es', 'en']}],
        'sameAs': ['https://www.linkedin.com/company/zenia-partners/', 'https://www.instagram.com/zeniapartners'],
        'knowsAbout': (['CRM a medida', 'agentes de IA', 'WhatsApp Business API', 'automatización de WhatsApp',
                        'automatización de citas y reservas', 'recuperación de clientes inactivos', 'IA para pymes',
                        'desarrollo de SaaS con IA'] if es else
                       ['custom CRM', 'AI agents', 'WhatsApp Business API', 'WhatsApp automation',
                        'booking automation', 'customer reactivation', 'AI for SMBs', 'AI SaaS development']),
        'priceRange': '297 € - 897 €+ / mes' if es else '€297 - €897+ / month',
        'hasOfferCatalog': {
            '@type': 'OfferCatalog', 'name': 'Servicios de Zenia Partners' if es else 'Zenia Partners services',
            'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'description': d}}
                                for n, d in SERVICIOS['es' if es else 'en']] +
                               [{'@type': 'Offer', 'name': f'Plan {n}', 'price': p, 'priceCurrency': 'EUR',
                                 'description': (des_es if es else des_en) + ('. Setup único de 997 €.' if es else '. One-off setup €997.'),
                                 'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': p, 'priceCurrency': 'EUR',
                                                        'unitText': 'MONTH'}}
                                for n, p, des_es, des_en in PLANES]},
    }


REF = {'@type': 'Organization', '@id': ID, 'name': 'Zenia Partners', 'url': BASE + '/'}


def es_nuestra(x):
    if not isinstance(x, dict):
        return False
    t = x.get('@type'); ts = t if isinstance(t, list) else [t]
    if not ({'Organization', 'ProfessionalService', 'LocalBusiness'} & set(ts)):
        return False
    return x.get('name') in NOMBRES or x.get('@id') in VIEJOS_ID


def arreglar(x, lang, nivel=0):
    """Devuelve (nuevo, cambiado). nivel 0 = objeto raíz o elemento de @graph."""
    if isinstance(x, list):
        out, ch = [], False
        for v in x:
            if nivel == 0 and isinstance(v, dict) and v.get('@id') in (BASE + '/#service', BASE + '/es/#service'):
                ch = True
                continue      # ficha vieja de «consultoría integral»: fuera
            nv, c = arreglar(v, lang, nivel)
            out.append(nv); ch = ch or c
        return out, ch
    if not isinstance(x, dict):
        return x, False
    if es_nuestra(x):
        nuevo = org(lang) if nivel == 0 else dict(REF)
        if nivel == 0 and '@context' in x:
            nuevo = {'@context': x['@context'], **nuevo}
        return nuevo, nuevo != x
    out, ch = {}, False
    for k, v in x.items():
        if k == '@graph':
            nv, c = arreglar(v, lang, 0)
        elif k == 'mainEntity' and es_nuestra(v):
            nv = org(lang); c = nv != v
        else:
            nv, c = arreglar(v, lang, nivel + 1)
        out[k] = nv; ch = ch or c
    return out, ch


def procesar(raiz='.'):
    os.chdir(raiz)
    tocados = []
    archivos = (glob.glob('*.html') + glob.glob('es/*.html') + glob.glob('en/*.html') +
                glob.glob('blog/*.html') + glob.glob('cases/*.html'))
    for f in sorted(archivos):
        h = open(f, encoding='utf-8').read()
        m = re.search(r'<html[^>]*\blang="([a-zA-Z]+)', h)
        lang = (m.group(1).lower()[:2] if m else 'es')
        cambios = [False]

        def rep(mm):
            try:
                d = json.loads(mm.group(2))
            except Exception:
                return mm.group(0)
            nd, ch = arreglar(d, lang)
            if isinstance(d, dict) and es_nuestra(d):
                nd, ch = {'@context': d.get('@context', 'https://schema.org'), **org(lang)}, True
            if not ch or nd == d:
                return mm.group(0)
            cambios[0] = True
            return mm.group(1) + json.dumps(nd, ensure_ascii=False).replace('</', '<\\/') + mm.group(3)

        n = re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', rep, h, flags=re.S)
        # una ficha completa por página como mucho: si ya va dentro de un @graph (portadas), sobran las
        # sueltas; si no, se queda la primera suelta
        marca = '"@id": "' + ID + '", "name": "Zenia Partners", "alternateName"'
        sueltas = list(re.finditer(r'<script type="application/ld\+json"[^>]*>\{"@context": "[^"]*", "@type": \["Organization", "ProfessionalService"\], "@id": "' + re.escape(ID) + r'".*?</script>\n?', n, re.S))
        en_graph = n.count(marca) > len(sueltas)
        sobran = sueltas if en_graph else sueltas[1:]
        for mm in reversed(sobran):
            n = n[:mm.start()] + n[mm.end():]
        if n != h:
            open(f, 'w', encoding='utf-8').write(n)
            tocados.append(f)
    return tocados


if __name__ == '__main__':
    t = procesar(sys.argv[1] if len(sys.argv) > 1 else '.')
    print('archivos con la entidad unificada:', len(t))
