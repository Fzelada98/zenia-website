#!/usr/bin/env python3
"""Genera las variantes «noir» (v2, pulidas) de la portada española para que Fabrizzio elija.

Parte del es/index.html de la rama rediseno-v10 (estructura recompuesta) y:
  - mueve la conversación del agente a la columna derecha de la portada, en una tarjeta de cristal,
    con avatar;
  - añade la línea en versalitas sobre el titular y la banda «Trabajamos sobre» con los símbolos
    reales de cada herramienta (simple-icons, CC0);
  - numera las secciones (clase `numbered`) para las etiquetas «— 01»;
  - pone una imagen real en la tarjeta destacada de servicios;
  - escribe la etapa dentro de cada tramo de la barra del proceso;
  - quita la frase de cifras (se repetía con la rejilla) y la burbuja que tapaba el precio;
  - cambia la primera foto de casos por la de Global Watch Buyers;
  - escribe es/index-a.html (negro y champán), es/index-b.html (navy y champán) y
    es/index-c.html (navy y azul de marca), cada una con su hoja.
"""
import os
import re
import sys

ZV = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.path.join(ZV, "es", "index.html")
STYLES = os.path.join(ZV, "styles")
OVER = os.path.join(HERE, "noir-overrides.css")
ICONS = os.path.join(HERE, "icons")

FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600"
         "&family=Space+Grotesk:wght@700&display=swap")

B_CSS = """/* Variante B: navy y champán */
:root { --paper: #0B1220; --paper-2: #111A2C; --paper-3: #1A2540; --nav-bg: rgba(11, 18, 32, 0.86); }
html, body { background: var(--paper); }
.chat { background: rgba(17, 26, 44, 0.72); }
.footer, body > div:has(> a[href$="cobertura.html"]) { background: #080D18 !important; }
"""

C_CSS = """/* Variante C: navy y azul de marca */
:root { --paper: #0B1220; --paper-2: #111A2C; --paper-3: #1A2540; --nav-bg: rgba(11, 18, 32, 0.86);
  --accent: #5B8CFF; --accent-deep: #2563EB; --accent-light: #8DB3FF; --accent-text: #8DB3FF;
  --accent-pale: rgba(91, 140, 255, 0.18); --accent-on-ink: #8DB3FF; --on-accent: #ffffff;
  --line: rgba(91, 140, 255, 0.2); --line-strong: rgba(91, 140, 255, 0.45);
  --halo: rgba(91, 140, 255, 0.14); --halo-2: rgba(91, 140, 255, 0.04); --ring: rgba(91, 140, 255, 0.16); }
html, body { background: var(--paper); }
svg.zenia-mark path:first-of-type { fill: #3B82F6; }
svg.zenia-mark path:last-of-type { fill: #5B8CFF; }
.chat { background: rgba(17, 26, 44, 0.72); border-color: rgba(91, 140, 255, 0.25); }
.chat-head { background: rgba(91, 140, 255, 0.08); }
.chat-avatar { background: rgba(91, 140, 255, 0.12); }
.msg.out { background: rgba(91, 140, 255, 0.2); }
.btn-primary, .cta-actions .btn-primary, .booking-submit, .demo-switch button[aria-pressed="true"], .stage.s1 { background: var(--accent-deep); color: #fff; }
.btn-primary:hover, .cta-actions .btn-primary:hover, .booking-submit:hover { background: #1D4ED8; }
.stage.s2 { background: #1D4ED8; color: #fff; }
.stage.s3 { background: rgba(91, 140, 255, 0.22); border-color: var(--line); }
.service-card--featured { background: rgba(91, 140, 255, 0.07); }
.service-card--featured:hover { background: rgba(91, 140, 255, 0.1); }
.price-hero { background: rgba(91, 140, 255, 0.06); }
#cookieBanner button:first-child { background: var(--accent-deep) !important; color: #fff !important; }
.footer, body > div:has(> a[href$="cobertura.html"]) { background: #080D18 !important; }
"""

TOOLS = [("whatsapp", "WhatsApp Business API"), ("hubspot", "HubSpot"), ("zoho", "Zoho CRM"),
         ("odoo", "Odoo"), ("googlecalendar", "Google Calendar"), ("calendly", "Calendly")]


def leer(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def escribir(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def uno(patron, s, flags=re.S):
    m = list(re.finditer(patron, s, flags))
    assert len(m) == 1, f"{patron[:50]!r}: {len(m)}"
    return m[0]


def icono(nombre):
    svg = leer(os.path.join(ICONS, nombre + ".svg")).strip()
    svg = re.sub(r"<title>.*?</title>", "", svg)
    svg = svg.replace('<svg role="img"', '<svg aria-hidden="true" focusable="false"', 1)
    return svg


def base_html(s):
    # 1. la conversación y su texto, a la portada
    demo = uno(r'\n<!-- DEMO: la conversación del agente -->\n<section class="demo" id="demo">.*?</section>\n', s)
    sec = demo.group(0)
    h2 = uno(r'<h2[^>]*>(.*?)</h2>', sec).group(1)
    switch = uno(r'<div class="demo-switch".*?</div>', sec).group(0)
    note = uno(r'<p class="demo-note"[^>]*>.*?</p>', sec).group(0)
    chat = uno(r'<div class="chat reveal reveal-delay-2" id="demoChat" data-ui>.*?\n    </div>\n', sec).group(0)
    s = s[: demo.start()] + "\n" + s[demo.end():]
    chat = chat.replace('<div class="chat-head"><div>', '<div class="chat-head"><span class="chat-avatar" aria-hidden="true">L</span><div>', 1)
    assert 'chat-avatar' in chat
    bloque = f'''    <div class="hero-demo reveal reveal-delay-2">
      <p class="demo-caption">{h2}</p>
      {switch}
      {chat.strip()}
      {note}
    </div>
'''
    s = re.sub(r'(<section class="hero[^"]*" id="hero">\s*<div class="container">\s*)',
               lambda m: m.group(1) + '<p class="eyebrow">CRM + WhatsApp + IA para PYMEs en Espa&ntilde;a y Latinoam&eacute;rica</p>\n    ', s, count=1)
    hero = uno(r'<section class="hero[^"]*" id="hero">.*?</section>', s)
    h = hero.group(0)
    cierre = h.rfind("</div>\n</section>")
    assert cierre > 0, "no encuentro el cierre de la portada"
    h = h[:cierre] + bloque + "  " + h[cierre:]
    s = s[: hero.start()] + h + s[hero.end():]
    assert 'class="hero-demo' in s, "no pude colocar la conversación en la portada"

    # 2. la banda de herramientas, con símbolo
    items = "".join(f"<li>{icono(k)}<span>{n}</span></li>" for k, n in TOOLS)
    strip = f'''
<!-- Herramientas sobre las que se trabaja -->
<section class="strip" aria-label="Herramientas">
  <div class="container">
    <p class="strip-label">Trabajamos sobre</p>
    <ul>{items}</ul>
  </div>
</section>
'''
    assert s.count('<section class="opportunities" id="opportunities">') == 1
    s = s.replace('<section class="opportunities" id="opportunities">', strip.strip() + '\n\n<section class="opportunities" id="opportunities">', 1)
    assert 'class="strip"' in s

    # 3. secciones numeradas
    for sel in ('class="opportunities" id="opportunities"', 'class="tailor" id="tailor"', 'class="section" id="services"',
                'class="section process" id="process"', 'class="section" id="impact"', 'class="proof" id="proof"',
                'class="faq-section" id="faq"', 'class="section index" id="verticales"', 'class="section pricing" id="precios"'):
        nuevo = sel.replace('class="', 'class="numbered ')
        assert s.count(f'<section {sel}>') == 1, sel
        s = s.replace(f'<section {sel}>', f'<section {nuevo}>', 1)

    # 4. tipografía
    s = re.sub(r"family=Source\+Serif\+4:[^&\"]+&family=Space\+Grotesk:wght@700", FONTS.split("css2?")[1].split("&display")[0], s)
    assert "Cormorant" in s

    # 5. la tarjeta destacada de servicios, con su imagen a la derecha
    fig = ('\n      <figure class="service-figure"><img src="/cases/img/ts-gaia-lote.webp" alt="Gaia, el agente de Throwin&rsquo; Salt: '
           'el lote del d&iacute;a de relojes revisado y listo para eBay" width="1080" height="1350" loading="lazy">'
           '<figcaption>Gaia, el agente que construimos para Throwin&rsquo; Salt: el lote del d&iacute;a de relojes, revisado y listo para publicar en eBay.</figcaption></figure>')
    m = uno(r'(<div class="service-card service-card--featured reveal">.*?<div class="service-card-body">.*?\n        </div>\n)(      </div>\n    </div>)', s)
    s = s[: m.end(1)] + "  " + fig.strip("\n") + "\n" + s[m.end(1):]
    assert 'service-figure' in s
    tarjeta = uno(r'<div class="service-card service-card--featured reveal">.*?</section>', s).group(0)
    assert tarjeta.index('service-figure') < tarjeta.index('</section>') and tarjeta.count('service-figure') == 1

    # 6. el proceso: la etapa escrita dentro de cada tramo
    etapas = {"s1": "An&aacute;lisis", "s2": "Redise&ntilde;o", "s3": "Implementaci&oacute;n", "s4": "Optimizaci&oacute;n continua"}
    for k, v in etapas.items():
        pat = re.compile(r'(<div class="stage %s" style="--w:[0-9.]+"><span>[^<]*</span>)(</div>)' % k)
        assert len(pat.findall(s)) == 1, k
        s = pat.sub(lambda mm: mm.group(1) + f'<strong>{v}</strong>' + mm.group(2), s, count=1)

    # 7. la frase de cifras (ya está en la rejilla) y la burbuja sobre el precio
    s = re.sub(r'\n\s*<p class="impact-sentence reveal">.*?</p>', '', s, count=1, flags=re.S)
    assert 'impact-sentence' not in s
    s = re.sub(r'\n\s*<div class="price-overlap" data-ui aria-hidden="true">.*?</div></div>', '', s, count=1, flags=re.S)
    assert 'price-overlap' not in s

    # 8. la primera foto de casos: Global Watch Buyers
    old = uno(r'<figure><img src="/cases/img/croian-home\.webp".*?</figure>', s).group(0)
    gwb = ('<figure><img src="/cases/img/gwb-card.webp" alt="Global Watch Buyers: captaci&oacute;n de relojes por WhatsApp en 33 pa&iacute;ses '
           '(conversaci&oacute;n recreada)" width="1600" height="1000" loading="lazy"><figcaption>Global Watch Buyers: captaci&oacute;n de relojes '
           'por WhatsApp en 33 pa&iacute;ses, con GWB Network (conversaci&oacute;n recreada)</figcaption></figure>')
    s = s.replace(old, gwb + "\n      " + old, 1)
    old3 = uno(r'\n      <figure><img src="/cases/img/ts-card\.webp".*?</figure>', s).group(0)
    s = s.replace(old3, "", 1)
    assert s.count("<figure>") == 3 + 0, s.count("<figure>")

    # 9. nota de marcas en el pie
    s = s.replace('</p>\n      </div>\n      <div class="footer-columns">',
                  '</p>\n        <p class="footer-brands">Las marcas y s&iacute;mbolos de terceros pertenecen a sus propietarios; no implican afiliaci&oacute;n.</p>\n      </div>\n      <div class="footer-columns">', 1)
    assert 'footer-brands' in s

    # 10. iconos decorativos ocultos: que no los lea el lector de pantalla
    s = s.replace('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
                  '<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">')
    return s


def main():
    s = base_html(leer(ES))
    main_css = leer(os.path.join(STYLES, "main.css"))
    over = leer(OVER)
    escribir(os.path.join(STYLES, "noir.css"), main_css + "\n\n" + over)
    escribir(os.path.join(STYLES, "noir-b.css"), B_CSS)
    escribir(os.path.join(STYLES, "noir-c.css"), C_CSS)
    for letra, extra, theme in (("a", "", "#0a0a0a"),
                                ("b", '\n<link rel="stylesheet" href="../styles/noir-b.css?v=2">', "#0B1220"),
                                ("c", '\n<link rel="stylesheet" href="../styles/noir-c.css?v=2">', "#0B1220")):
        v = s.replace('<link rel="stylesheet" href="../styles/main.css?v=11">', '<link rel="stylesheet" href="../styles/noir.css?v=2">' + extra)
        v = v.replace('<link rel="stylesheet" href="../styles/main.css?v=10">', '<link rel="stylesheet" href="../styles/noir.css?v=2">' + extra)
        assert "noir.css" in v
        v = v.replace('<meta name="theme-color" content="#F4F4F1">', f'<meta name="theme-color" content="{theme}">')
        v = v.replace('../js/demo-chat.js?v=1', '../js/demo-chat.js?v=2')
        escribir(os.path.join(ZV, "es", f"index-{letra}.html"), v)
        print("es/index-%s.html" % letra, len(v))


if __name__ == "__main__":
    main()
