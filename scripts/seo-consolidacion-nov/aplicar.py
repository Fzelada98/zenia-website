#!/usr/bin/env python3
"""ZENIA, SEO de noviembre de 2026: títulos cortados y canibalización de búsquedas de dinero.

Search Console (11-oct a 7-nov, solo búsquedas humanas: se descartan las de robots con
operadores tipo «-site:» o «intitle:») mostró:

  1. Cinco títulos cortados a mitad de palabra («Guía Compl», «Clinicas y Denti», «en Espa»),
     dos de ellos en landings nacionales.
  2. Cuatro páginas peleando por «crm precios» / «cuánto cuesta un CRM» (posiciones 25 a 63)
     y tres por «crm para asesorías» (16 a 32). Dos de las de precios y una de asesorías son
     el mismo artículo con otro nombre.

Qué hace (idempotente, se puede volver a correr):
  - Títulos completos y alineados con la búsqueda real (también og:title y twitter:title).
  - Los duplicados exactos declaran como canónica a su página principal, pierden sus
    etiquetas hreflang propias, salen del sitemap y llevan arriba un aviso con enlace a la
    principal. No se borra ni se redirige nada: quien llega sigue leyendo la página.
  - Las páginas con ángulo propio (implantación, gestorías) se quedan y enlazan a la principal.
Uso: python3 scripts/seo-consolidacion-nov/aplicar.py [RAÍZ]
"""
import datetime
import os
import re
import sys

BASE = 'https://zeniapartners.com'

TITULOS = {
    'blog/ai-agents-business-operations.html': 'What Are AI Agents? How They Transform Business Operations',
    'blog/chatbot-whatsapp-restaurantes.html': 'Chatbot para restaurantes por WhatsApp: guía 2026 | ZENIA',
    'cases/ecommerce-usa.html': 'Case Study: AI Customer Agent for US Luxury Ecommerce',
    'es/crm-clinicas.html': 'CRM para clínicas y dentistas con IA y WhatsApp | ZENIA',
    'es/crm-whatsapp.html': 'CRM con WhatsApp e IA para negocios en España | ZENIA',
}

# duplicado -> (principal, ancla, frase del aviso)
CANONICAS = {
    'blog/cuanto-cuesta-un-crm.html': (
        'blog/cuanto-cuesta-un-crm-para-pymes.html', 'cuánto cuesta un CRM para pymes en 2026',
        'Tenemos una versión más completa y actualizada de esta guía: {enlace}, con la comparativa de precios por modelo y el cálculo de ROI.'),
    'blog/coste-crm.html': (
        'blog/cuanto-cuesta-un-crm-para-pymes.html', 'precios de CRM para pymes en 2026',
        'La guía principal sobre el coste de un CRM, con precios por modelo, costes ocultos y ROI, está en {enlace}.'),
    'blog/mejor-crm-para-asesorias.html': (
        'blog/crm-para-asesorias.html', 'CRM para asesorías: comparativa y precios 2026',
        'La comparativa completa y actualizada está en {enlace}.'),
}

# página con ángulo propio -> (principal, ancla, frase)
PUENTES = {
    'blog/cuanto-cuesta-implementar-un-crm.html': (
        'blog/cuanto-cuesta-un-crm-para-pymes.html', 'cuánto cuesta un CRM para pymes',
        'Esta guía trata el coste de implantación. Si lo que buscas son los precios de las licencias, mira {enlace}.'),
    'blog/crm-para-gestorias.html': (
        'blog/crm-para-asesorias.html', 'CRM para asesorías',
        'Si lo tuyo es una asesoría fiscal, laboral o contable, la comparativa de herramientas y precios está en {enlace}.'),
}


def cambiar_titulo(s, t):
    s = re.sub(r'<title>[^<]*</title>', f'<title>{t}</title>', s, count=1)
    s = re.sub(r'(property="og:title" content=")[^"]*(")', lambda m: m.group(1) + t + m.group(2), s)
    s = re.sub(r'(name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + t + m.group(2), s)
    return s


def aviso(s, destino, ancla, frase):
    """Una sola vez, justo después del primer párrafo bajo el H1 (la primera mención pesa más)."""
    if 'data-zenia-consolidacion' in s:
        return s
    enlace = f'<a href="/{destino}">{ancla}</a>'
    p = (f'\n<p data-zenia-consolidacion="1" style="background:rgba(59,130,246,.08);border-left:3px solid #3B82F6;'
         f'padding:12px 16px;border-radius:6px;margin:22px 0">' + frase.format(enlace=enlace) + '</p>\n')
    m = re.search(r'</h1>', s)
    if not m:
        return s
    corte = s.find('</p>', m.end())
    corte = (corte + 4) if corte != -1 else m.end()
    return s[:corte] + p + s[corte:]


def canonica(s, ruta, principal):
    url = f'{BASE}/{principal}'
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    # las hreflang apuntaban a sí misma: con canónica ajena se contradicen
    s = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="' + re.escape(f'{BASE}/{ruta}') + r'">', '', s)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), s, count=1)
    return s


def main(raiz='.'):
    os.chdir(raiz)
    tocados = []

    def guardar(f, s, o):
        if s != o:
            open(f, 'w', encoding='utf-8').write(s)
            tocados.append(f)

    for f, t in TITULOS.items():
        if os.path.exists(f):
            o = open(f, encoding='utf-8').read()
            guardar(f, cambiar_titulo(o, t), o)
    for f, (pr, ancla, frase) in CANONICAS.items():
        if os.path.exists(f) and os.path.exists(pr):
            o = open(f, encoding='utf-8').read()
            guardar(f, aviso(canonica(o, f, pr), pr, ancla, frase), o)
    for f, (pr, ancla, frase) in PUENTES.items():
        if os.path.exists(f) and os.path.exists(pr):
            o = open(f, encoding='utf-8').read()
            guardar(f, aviso(o, pr, ancla, frase), o)

    # sitemap: fuera los duplicados; lastmod de hoy en lo que cambió
    sm = 'sitemap.xml'
    if os.path.exists(sm):
        o = open(sm, encoding='utf-8').read()
        s = o
        for f in CANONICAS:
            s = re.sub(r'\s*<url>\s*<loc>' + re.escape(f'{BASE}/{f}') + r'</loc>.*?</url>', '', s, flags=re.S)
        hoy = datetime.date.today().isoformat()
        cambiadas = set(TITULOS) | {p for p, *_ in CANONICAS.values()} | set(PUENTES)
        for f in cambiadas:
            s = re.sub(r'(<loc>' + re.escape(f'{BASE}/{f}') + r'</loc>\s*<lastmod>)[^<]*(</lastmod>)',
                       lambda m: m.group(1) + hoy + m.group(2), s)
        guardar(sm, s, o)
    return tocados


if __name__ == '__main__':
    t = main(sys.argv[1] if len(sys.argv) > 1 else '.')
    print('archivos cambiados:', len(t))
    for x in t:
        print(' ', x)
