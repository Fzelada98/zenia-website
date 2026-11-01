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
.crm-toast { background: rgba(91, 140, 255, 0.07); }
.btn-primary, .cta-actions .btn-primary, .booking-submit, .demo-switch button[aria-pressed="true"], .gantt-row:nth-child(1) .gantt-bar { background: var(--accent-deep); color: #fff; }
.btn-primary:hover, .cta-actions .btn-primary:hover, .booking-submit:hover { background: #1D4ED8; }
.gantt-row:nth-child(2) .gantt-bar { background: #1D4ED8; color: #fff; }
.gantt-row:nth-child(3) .gantt-bar { background: rgba(91, 140, 255, 0.22); border-color: var(--line-strong); }
.gantt-row--inf .gantt-bar { background: rgba(91, 140, 255, 0.14); border-color: var(--line); }
.service-card--featured { background: rgba(91, 140, 255, 0.07); }
.service-card--featured:hover { background: rgba(91, 140, 255, 0.1); }
.price-hero { background: rgba(91, 140, 255, 0.06); }
#cookieBanner button:first-child { background: var(--accent-deep) !important; color: #fff !important; }
.footer, body > div:has(> a[href$="cobertura.html"]) { background: #080D18 !important; }
"""

TOOLS = [("whatsapp", "WhatsApp Business API"), ("hubspot", "HubSpot"), ("zoho", "Zoho CRM"),
         ("odoo", "Odoo"), ("googlecalendar", "Google Calendar"), ("calendly", "Calendly")]

# El teléfono con el WhatsApp del agente (tema oscuro oficial). Lo que va dentro es la versión
# estática del restaurante: sin script se ve así; con script, demo-chat.js v3 la reproduce.
TELEFONO = '''      __SWITCH__
      <div class="phone" data-ui>
        <div class="phone-status" aria-hidden="true"><span class="phone-time">23:48</span><span class="phone-icons"><svg viewBox="0 0 16 12"><path fill="currentColor" d="M0 9h2v3H0zM4 6h2v6H4zM8 3h2v9H8zM12 0h2v12h-2z"/></svg><svg viewBox="0 0 16 12"><path fill="currentColor" d="M8 2.4c2.6 0 4.9 1 6.6 2.7l-1.3 1.3A7.5 7.5 0 0 0 8 4.3a7.5 7.5 0 0 0-5.3 2.1L1.4 5.1A9.3 9.3 0 0 1 8 2.4zm0 3.6c1.6 0 3 .6 4.1 1.7l-1.3 1.3A4 4 0 0 0 8 7.9a4 4 0 0 0-2.8 1.1L3.9 7.7A5.8 5.8 0 0 1 8 6zm0 3.6c.7 0 1.3.3 1.7.7L8 12l-1.7-1.7c.4-.4 1-.7 1.7-.7z"/></svg><svg viewBox="0 0 24 12"><rect x=".5" y=".5" width="20" height="11" rx="2.5" fill="none" stroke="currentColor"/><rect x="2" y="2" width="16" height="8" rx="1.5" fill="currentColor"/><path fill="currentColor" d="M22 4v4a2 2 0 0 0 0-4z"/></svg></span></div>
        <div class="chat" id="demoChat">
          <div class="chat-head"><span class="chat-back" aria-hidden="true">&lsaquo;</span><span class="chat-avatar" aria-hidden="true">L</span><div class="chat-who"><strong>La Terraza &middot; Restaurante</strong><span class="chat-status">en l&iacute;nea</span></div><span class="chat-tools" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="m16 10 5-3v10l-5-3z"/></svg><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></span></div>
          <div class="chat-body">
            <div class="chat-day">Hoy</div>
            <div class="chat-lock">Los mensajes est&aacute;n cifrados de extremo a extremo.</div>
            <div class="msg in shown"><span class="msg-text">Hola, &iquest;tienen mesa para 4 ma&ntilde;ana a las 21:00?</span><time>23:45</time></div>
            <div class="msg out shown read"><span class="msg-text">&iexcl;Hola! S&iacute;, nos queda mesa para 4 a las 21:00. &iquest;D&oacute;nde prefieres?</span><time>23:45<i class="ticks" aria-hidden="true"></i></time><span class="msg-buttons"><span class="tapped">Terraza</span><span>Sal&oacute;n</span></span></div>
            <div class="msg in reply shown"><span class="msg-text">Terraza</span><time>23:46</time></div>
            <div class="msg in shown"><span class="msg-text">A nombre de Laura.</span><time>23:46</time></div>
            <div class="msg out shown read"><span class="msg-text">Listo, Laura: mesa para 4 ma&ntilde;ana a las 21:00 en la terraza. Te mando un recordatorio ma&ntilde;ana a las 18:00. &iquest;Alguna alergia que debamos saber?</span><time>23:46<i class="ticks" aria-hidden="true"></i></time></div>
            <div class="msg in shown"><span class="msg-text">Sin gluten, gracias</span><time>23:47</time></div>
            <div class="msg out shown read"><span class="msg-text">Anotado, avisamos a cocina. &iexcl;Hasta ma&ntilde;ana!</span><time>23:47<i class="ticks" aria-hidden="true"></i></time></div>
          </div>
          <div class="chat-input" aria-hidden="true"><span class="chat-input-field">Mensaje</span><span class="chat-mic"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 15a4 4 0 0 0 4-4V6a4 4 0 0 0-8 0v5a4 4 0 0 0 4 4zm6-4a6 6 0 0 1-12 0H4a8 8 0 0 0 7 7.9V22h2v-3.1A8 8 0 0 0 20 11z"/></svg></span></div>
        </div>
      </div>
      <div class="crm-toast" id="crmToast" data-ui aria-live="polite"><p class="crm-label">Guardado en el CRM</p><strong>Laura &middot; Mesa para 4</strong><p>Ma&ntilde;ana 21:00 &middot; Terraza &middot; Sin gluten</p><p>Recordatorio autom&aacute;tico: ma&ntilde;ana a las 18:00</p></div>'''


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
    s = s[: demo.start()] + "\n" + s[demo.end():]
    telefono = TELEFONO.replace("__SWITCH__", switch)
    bloque = f'''    <div class="hero-demo reveal reveal-delay-2">
      <p class="demo-caption" id="demoCaption">{h2}</p>
{telefono}
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
    ini = h.index('<p class="eyebrow">')
    fin = h.index('    <div class="hero-demo')
    h = h[:ini] + '<div class="hero-copy">\n    ' + h[ini:fin] + '    </div>\n' + h[fin:]
    s = s[: hero.start()] + h + s[hero.end():]
    assert s.count('hero-copy') == 1
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

    # 6. el proceso: línea de tiempo con regla de semanas (como en un informe)
    pasos = re.findall(r'<li class="process-step" style="--w:[0-9.]+"><h3>(.*?)</h3><p>(.*?)</p></li>', s)
    assert len(pasos) == 4, len(pasos)
    pos = [(0, 2, "1 a 2 semanas", ""), (2, 4, "1 a 2 semanas", ""),
           (4, 9.5, "4 a 6 semanas", '<span class="gantt-mark"><span>Primer resultado</span></span>'),
           (9.5, 12, "Continuo, cada mes", "")]
    filas = []
    for (h3, ptxt), (a, b, dur, extra) in zip(pasos, pos):
        inf = ' gantt-row--inf' if b >= 12 else ''
        corto = "Continuo" if inf else dur
        filas.append(f'      <li class="gantt-row{inf}" style="--s:{a};--e:{b}"><div class="gantt-text"><h3>{h3}</h3><p>{ptxt}</p><span class="gantt-dur">{dur}</span></div>'
                     f'<div class="gantt-track">{extra}<span class="gantt-bar"><i>{corto}</i></span></div></li>')
    regla = "".join(f"<span>{'Sem. 1' if i == 1 else i}</span>" for i in range(1, 11)) + '<span class="gantt-inf">en adelante</span>'
    gantt = ('    <div class="gantt reveal reveal-delay-1" data-ui>\n      <div class="gantt-head"><span class="gantt-corner">Etapa</span>'
             '<div class="gantt-ruler" aria-hidden="true">' + regla + '</div></div>\n      <ol class="gantt-rows">\n' + "\n".join(filas) +
             '\n      </ol>\n      <p class="gantt-note">Semanas desde la primera llamada. El primer resultado medible llega antes de la octava.</p>\n    </div>')
    m = uno(r'    <div class="stage-bar reveal reveal-delay-1" data-ui>.*?</ol>\n', s)
    s = s[: m.start()] + gantt + "\n" + s[m.end():]
    assert 'stage-bar' not in s and 'class="gantt' in s

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
        v = v.replace('../js/demo-chat.js?v=1', '../js/demo-chat.js?v=3')
        escribir(os.path.join(ZV, "es", f"index-{letra}.html"), v)
        print("es/index-%s.html" % letra, len(v))


if __name__ == "__main__":
    main()
