#!/usr/bin/env python3
"""Construye las DOS portadas de Zenia (inglés `index.html` y español `es/index.html`) con el diseño
«noir C» (navy y azul de marca) para publicarlas, a partir de las portadas de la rama `rediseno-v10`.

    python3 build_launch.py <carpeta con las portadas de la rama (fuente)> <carpeta de salida (clon de main)>

Escribe en la salida: index.html, es/index.html y styles/home.css (= main.css v11 de la rama +
noir-overrides.css + los tokens de la variante C). Las landings siguen con su styles/main.css de main.
La hoja lleva ?v=<epoch>: cada construcción cambia la versión y el navegador no reutiliza la vieja.
"""
import os
import re
import sys
import time

SRC = sys.argv[1]
OUT = sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
OVER = os.path.join(HERE, "noir-overrides.css")
ICONS = os.path.join(HERE, "icons")

FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600"
         "&family=Space+Grotesk:wght@700&display=swap")

C_CSS = """/* Variante C: navy y azul de marca */
:root { --paper: #0B1220; --paper-2: #111A2C; --paper-3: #1A2540; --nav-bg: rgba(11, 18, 32, 0.86); --paper-rgb: 11, 18, 32; --net-rgb: 91, 140, 255;
  --accent: #5B8CFF; --accent-deep: #2563EB; --accent-light: #8DB3FF; --accent-text: #8DB3FF;
  --accent-pale: rgba(91, 140, 255, 0.18); --accent-on-ink: #8DB3FF; --on-accent: #ffffff;
  --line: rgba(91, 140, 255, 0.2); --line-strong: rgba(91, 140, 255, 0.45);
  --halo: rgba(91, 140, 255, 0.14); --halo-2: rgba(91, 140, 255, 0.04); --ring: rgba(91, 140, 255, 0.16);
  --ink: #EEF1F7; --ink-2: #F7F9FC; --ink-soft: #C3CAD8; --ink-mute: #8B95A7; --on-ink: #EEF1F7; --on-ink-soft: #C3CAD8; }
html, body { background: var(--paper); }
.skip-to-content, .btn-primary, .cta-actions .btn-primary, .booking-submit { color: #fff; }
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

# Textos por idioma. Lo que no está aquí viene del HTML de la rama.
L = {
    "es": {
        "pre": "../", "home": "/es/", "lang": "es",
        "eyebrow": "CRM a medida + agente de IA por WhatsApp",
        "subtitle": "Un CRM hecho a la medida de tu negocio y un agente de IA que atiende, agenda y vende por WhatsApp. Resultados medibles en 4 semanas.",
        "strip_aria": "Herramientas", "strip_label": "Trabajamos sobre",
        "chat_name": "La Terraza &middot; Restaurante", "online": "en l&iacute;nea", "today": "Hoy",
        "lock": "Los mensajes est&aacute;n cifrados de extremo a extremo.", "input": "Mensaje",
        "msgs": [("in", "Hola, &iquest;tienen mesa para 4 ma&ntilde;ana a las 21:00?", "23:45", None),
                 ("out", "&iexcl;Hola! S&iacute;, nos queda mesa para 4 a las 21:00. &iquest;D&oacute;nde prefieres?", "23:45", ("Terraza", "Sal&oacute;n")),
                 ("in reply", "Terraza", "23:46", None), ("in", "A nombre de Laura.", "23:46", None),
                 ("out", "Listo, Laura: mesa para 4 ma&ntilde;ana a las 21:00 en la terraza. Te mando un recordatorio ma&ntilde;ana a las 18:00. &iquest;Alguna alergia que debamos saber?", "23:46", None),
                 ("in", "Sin gluten, gracias", "23:47", None), ("out", "Anotado, avisamos a cocina. &iexcl;Hasta ma&ntilde;ana!", "23:47", None)],
        "crm_tag": "CRM a medida", "crm_aria": "CRM a medida &middot; La Terraza", "tabs": ["Reservas", "Clientes", "Campa&ntilde;as", "Agente", "Ajustes"],
        "who": "Madrid &middot; 2 salas", "live": "Actualizado ahora",
        "kpis": [("Reservas para ma&ntilde;ana", "24", "+1"), ("Ocupaci&oacute;n a las 21:00", "92&nbsp;%", ""), ("Atendidas por el agente", "16", "+1")],
        "crm_title": "Reservas de ma&ntilde;ana", "crm_when": "Martes",
        "cols": ["Hora", "Nombre", "Pax", "Zona", "Notas", "Estado"],
        "rows": [("20:00", "Familia Ortega", "6", "Sal&oacute;n", "Cumplea&ntilde;os", "ok", "Confirmada", False),
                 ("20:30", "Marc Vidal", "2", "Terraza", "&mdash;", "ok", "Confirmada", False),
                 ("21:00", "Laura", "4", "Terraza", "Sin gluten", "agent", "Por el agente", True),
                 ("21:00", "Ana Ruiz", "3", "Sal&oacute;n", "Silla beb&eacute;", "wait", "Pendiente", False),
                 ("21:30", "Pedro Lima", "2", "Terraza", "&mdash;", "ok", "Confirmada", False),
                 ("22:00", "Grupo Sato", "8", "Sal&oacute;n", "Men&uacute; degustaci&oacute;n", "ok", "Confirmada", False)],
        "sound": "Ver con sonido",
        "saas_aria": "V&iacute;deo de lanzamiento de GWB Network, la red privada de transporte en mano construida por Zenia",
        "saas_cap": 'GWB Network, la plataforma que construimos para Global Watch Buyers. <a href="/es/caso-global-watch-buyers.html">Ver el caso</a>.',
        "saas_points": ["Red privada de transporte en mano, con miembros por aval e identidad verificada", "Un c&oacute;digo de entrega en cada viaje y panel para el equipo", "Dise&ntilde;o, desarrollo, lanzamiento y v&iacute;deo: todo desde Zenia"],
        "durs": ["1 a 2 semanas", "1 a 2 semanas", "4 a 6 semanas", "Continuo, cada mes"], "shorts": ["1 a 2 sem.", "1 a 2 sem.", "4 a 6 sem.", "Continuo"],
        "wk1": "Sem. 1", "onwards": "en adelante", "stage": "Etapa", "first": "Primer resultado",
        "gantt_note": "Semanas desde la primera llamada.",
        "copilots": ("<h3>Copilotos de Conocimiento Interno</h3>", "<h3>Copilotos de Conocimiento</h3>"),
        "gwb_aria": "Recreaci&oacute;n: un vendedor de relojes escribe a las 2:47 de la madrugada y sale con la llamada agendada",
        "gwb_cap": "Las 2:47 de la madrugada: un vendedor escribe y sale con la llamada agendada. Recreaci&oacute;n.",
        "gwb_eyebrow": "Caso destacado &middot; Global Watch Buyers",
        "gwb_h3": "Vendedores de relojes de lujo de 33 pa&iacute;ses, captados por WhatsApp",
        "gwb_p": "P&aacute;ginas de venta en 13 idiomas, WhatsApp con cualificaci&oacute;n, panel de leads y anuncios que solo traen vendedores. Encima, el agente de IA que contesta, cualifica y agenda.",
        "gwb_stats": [("831", "conversaciones de WhatsApp"), ("33", "pa&iacute;ses"), ("10 de 12", "contactos de anuncios con reloj premium")],
        "gwb_link": "/es/caso-global-watch-buyers.html", "gwb_btn": "Ver el caso",
        "ts_aria": "The Unmakeable, pel&iacute;cula de marca de Throwin&rsquo; Salt Co. hecha por Zenia con relojes reales del stock",
        "ts_cap": "The Unmakeable, la pel&iacute;cula de marca de Throwin&rsquo; Salt Co., hecha por Zenia.",
        "ts_eyebrow": "Caso destacado &middot; Throwin&rsquo; Salt Co.",
        "ts_h3": "Relojes de alta gama: el lote del d&iacute;a, publicado en eBay desde WhatsApp",
        "ts_p": "Gaia, el agente que construimos, prepara cada anuncio con t&iacute;tulo, fotos y precio y lo publica en eBay cuando el equipo dice &laquo;publica&raquo;.",
        "ts_stats": [("54", "relojes publicados en 4 semanas"), ("23", "en un solo d&iacute;a"), ("2&nbsp;M$", "de inventario en eBay")],
        "ts_link": "/es/caso-throwin-salt-gaia.html", "ts_btn": "Ver el caso",
        "footer_tag": "CRM a medida y agentes de IA por WhatsApp para PYMEs en Espa&ntilde;a y Latinoam&eacute;rica.",
        "footer_cta": "Agenda una llamada",
        "brands": "Las marcas y s&iacute;mbolos de terceros pertenecen a sus propietarios; no implican afiliaci&oacute;n.",
        "credit": 'Fotograf&iacute;a de Madrid: <a href="https://commons.wikimedia.org/wiki/File:Skyline_view_of_Madrid,_Spain_at_night_-_50317258357.jpg" target="_blank" rel="noopener">Tim Adams</a>, CC BY 2.0, v&iacute;a Wikimedia Commons.',
    },
    "en": {
        "pre": "", "home": "/", "lang": "en",
        "eyebrow": "Tailor-made CRM + AI agent on WhatsApp",
        "subtitle": "A CRM built around your business and an AI agent that answers, books and sells on WhatsApp. Measurable results in 4 weeks.",
        "strip_aria": "Tools", "strip_label": "We work on",
        "chat_name": "La Terraza &middot; Restaurant", "online": "online", "today": "Today",
        "lock": "Messages are end-to-end encrypted.", "input": "Message",
        "msgs": [("in", "Hi, do you have a table for 4 tomorrow at 21:00?", "23:45", None),
                 ("out", "Hi! Yes, we still have a table for 4 at 21:00. Where would you like to sit?", "23:45", ("Terrace", "Dining room")),
                 ("in reply", "Terrace", "23:46", None), ("in", "Under Laura.", "23:46", None),
                 ("out", "Done, Laura: table for 4 tomorrow at 21:00 on the terrace. I will send you a reminder tomorrow at 18:00. Any allergies we should know about?", "23:46", None),
                 ("in", "Gluten free, thanks", "23:47", None), ("out", "Noted, we will tell the kitchen. See you tomorrow!", "23:47", None)],
        "crm_tag": "Tailor-made CRM", "crm_aria": "Tailor-made CRM &middot; La Terraza", "tabs": ["Bookings", "Guests", "Campaigns", "Agent", "Settings"],
        "who": "Madrid &middot; 2 rooms", "live": "Updated just now",
        "kpis": [("Bookings for tomorrow", "24", "+1"), ("Occupancy at 21:00", "92&nbsp;%", ""), ("Handled by the agent", "16", "+1")],
        "crm_title": "Tomorrow&rsquo;s bookings", "crm_when": "Tuesday",
        "cols": ["Time", "Name", "Guests", "Area", "Notes", "Status"],
        "rows": [("20:00", "Ortega family", "6", "Dining room", "Birthday", "ok", "Confirmed", False),
                 ("20:30", "Marc Vidal", "2", "Terrace", "&mdash;", "ok", "Confirmed", False),
                 ("21:00", "Laura", "4", "Terrace", "Gluten free", "agent", "By the agent", True),
                 ("21:00", "Ana Ruiz", "3", "Dining room", "High chair", "wait", "Pending", False),
                 ("21:30", "Pedro Lima", "2", "Terrace", "&mdash;", "ok", "Confirmed", False),
                 ("22:00", "Sato party", "8", "Dining room", "Tasting menu", "ok", "Confirmed", False)],
        "sound": "Play with sound",
        "saas_aria": "Launch film of GWB Network, the private hand-carry network built by Zenia",
        "saas_cap": 'GWB Network, the platform we built for Global Watch Buyers. <a href="/cases/global-watch-buyers-ai-acquisition.html">Read the case</a>.',
        "saas_points": ["A private hand-carry network, with vouched members and verified identity", "A handover code on every trip and a panel for the team", "Design, build, launch and film: all from Zenia"],
        "durs": ["1 to 2 weeks", "1 to 2 weeks", "4 to 6 weeks", "Ongoing, every month"], "shorts": ["1 to 2 wks", "1 to 2 wks", "4 to 6 wks", "Ongoing"],
        "wk1": "Wk 1", "onwards": "onwards", "stage": "Stage", "first": "First result",
        "gantt_note": "Weeks from the first call.",
        "copilots": None,
        "gwb_aria": "Re-enactment: a watch seller writes at 2:47 in the morning and leaves with a call booked",
        "gwb_cap": "2:47 in the morning: a seller writes and leaves with a call booked. A re-enactment.",
        "gwb_eyebrow": "Featured case &middot; Global Watch Buyers",
        "gwb_h3": "Luxury watch sellers from 33 countries, acquired on WhatsApp",
        "gwb_p": "Selling pages in 13 languages, WhatsApp with qualification, a lead panel and ads that only bring sellers. On top, the AI agent that answers, qualifies and books.",
        "gwb_stats": [("831", "WhatsApp conversations"), ("33", "countries"), ("10 of 12", "ad contacts with a premium watch")],
        "gwb_link": "/cases/global-watch-buyers-ai-acquisition.html", "gwb_btn": "See the case",
        "ts_aria": "The Unmakeable, the brand film of Throwin&rsquo; Salt Co., made by Zenia with real watches from stock",
        "ts_cap": "The Unmakeable, the brand film of Throwin&rsquo; Salt Co., made by Zenia.",
        "ts_eyebrow": "Featured case &middot; Throwin&rsquo; Salt Co.",
        "ts_h3": "High-end watches: the day&rsquo;s lot, listed on eBay from WhatsApp",
        "ts_p": "Gaia, the agent we built, prepares every listing with title, photos and price and publishes it on eBay when the team says &ldquo;publish&rdquo;.",
        "ts_stats": [("54", "watches listed in 4 weeks"), ("23", "in a single day"), ("$2&nbsp;M", "of inventory on eBay")],
        "ts_link": "/cases/throwin-salt-gaia-ebay-whatsapp.html", "ts_btn": "See the case",
        "footer_tag": "Tailor-made CRM and AI agents on WhatsApp for SMBs in Spain and Latin America.",
        "footer_cta": "Book a call",
        "brands": "Third-party marks and logos belong to their owners; no affiliation is implied.",
        "credit": 'Madrid photograph: <a href="https://commons.wikimedia.org/wiki/File:Skyline_view_of_Madrid,_Spain_at_night_-_50317258357.jpg" target="_blank" rel="noopener">Tim Adams</a>, CC BY 2.0, via Wikimedia Commons.',
    },
}

PHONE_STATUS = ('<div class="phone-status" aria-hidden="true"><span class="phone-time">23:48</span><span class="phone-icons"><svg viewBox="0 0 16 12"><path fill="currentColor" d="M0 9h2v3H0zM4 6h2v6H4zM8 3h2v9H8zM12 0h2v12h-2z"/></svg>'
                '<svg viewBox="0 0 16 12"><path fill="currentColor" d="M8 2.4c2.6 0 4.9 1 6.6 2.7l-1.3 1.3A7.5 7.5 0 0 0 8 4.3a7.5 7.5 0 0 0-5.3 2.1L1.4 5.1A9.3 9.3 0 0 1 8 2.4zm0 3.6c1.6 0 3 .6 4.1 1.7l-1.3 1.3A4 4 0 0 0 8 7.9a4 4 0 0 0-2.8 1.1L3.9 7.7A5.8 5.8 0 0 1 8 6zm0 3.6c.7 0 1.3.3 1.7.7L8 12l-1.7-1.7c.4-.4 1-.7 1.7-.7z"/></svg>'
                '<svg viewBox="0 0 24 12"><rect x=".5" y=".5" width="20" height="11" rx="2.5" fill="none" stroke="currentColor"/><rect x="2" y="2" width="16" height="8" rx="1.5" fill="currentColor"/><path fill="currentColor" d="M22 4v4a2 2 0 0 0 0-4z"/></svg></span></div>')
CHAT_TOOLS = ('<span class="chat-tools" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="m16 10 5-3v10l-5-3z"/></svg>'
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></span>')
MIC = '<span class="chat-mic"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 15a4 4 0 0 0 4-4V6a4 4 0 0 0-8 0v5a4 4 0 0 0 4 4zm6-4a6 6 0 0 1-12 0H4a8 8 0 0 0 7 7.9V22h2v-3.1A8 8 0 0 0 20 11z"/></svg></span>'


def leer(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def escribir(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def uno(patron, s, flags=re.S):
    m = list(re.finditer(patron, s, flags))
    assert len(m) == 1, f"{patron[:60]!r}: {len(m)}"
    return m[0]


def icono(nombre):
    svg = leer(os.path.join(ICONS, nombre + ".svg")).strip()
    svg = re.sub(r"<title>.*?</title>", "", svg)
    return svg.replace('<svg role="img"', '<svg aria-hidden="true" focusable="false"', 1)


def telefono(T, crm):
    msgs = []
    for d, txt, when, btns in T["msgs"]:
        out = "out" in d
        cls = "msg " + d + " shown" + (" read" if out else "")
        line = f'<div class="{cls}"><span class="msg-text">{txt}</span><time>{when}' + ('<i class="ticks" aria-hidden="true"></i>' if out else "") + '</time>'
        if btns:
            line += '<span class="msg-buttons">' + "".join(('<span class="tapped">' if i == 0 else '<span>') + b + '</span>' for i, b in enumerate(btns)) + '</span>'
        msgs.append("            " + line + "</div>")
    return f'''      __SWITCH__
      <div class="scene">
{crm}
      <div class="phone" data-ui>
        {PHONE_STATUS}
        <div class="chat" id="demoChat">
          <div class="chat-head"><span class="chat-back" aria-hidden="true">&lsaquo;</span><span class="chat-avatar" aria-hidden="true">L</span><div class="chat-who"><strong>{T["chat_name"]}</strong><span class="chat-status">{T["online"]}</span></div>{CHAT_TOOLS}</div>
          <div class="chat-body">
            <div class="chat-day">{T["today"]}</div>
            <div class="chat-lock">{T["lock"]}</div>
{chr(10).join(msgs)}
          </div>
          <div class="chat-input" aria-hidden="true"><span class="chat-input-field">{T["input"]}</span>{MIC}</div>
        </div>
      </div>
      </div>'''


def crm_html(T, marca):
    tabs = "".join(('<span class="on">' if i == 0 else '<span>') + t + '</span>' for i, t in enumerate(T["tabs"]))
    kpis = "".join(f'<div class="crm-kpi"><small>{k}</small><strong>{v}{("<i>" + d + "</i>") if d else ""}</strong></div>' for k, v, d in T["kpis"])
    ths = "".join(('<th class="opt">' if i in (3, 4) else '<th>') + c + '</th>' for i, c in enumerate(T["cols"]))
    rows = []
    for t, n, pax, zona, nota, st, lab, new in T["rows"]:
        tr = '<tr class="crm-row new show">' if new else '<tr>'
        rows.append(f'          {tr}<td>{t}</td><td>{n}</td><td>{pax}</td><td class="opt">{zona}</td><td class="opt dim">{nota}</td><td><span class="crm-state {st}">{lab}</span></td></tr>')
    mark = f'<span class="crm-mark" aria-hidden="true">{marca}</span>'
    return f'''    <div class="crm-window" id="crmWindow" data-ui aria-label="{T["crm_aria"]}">
      <aside class="crm-side">{mark}<nav>{tabs}</nav><div class="crm-who"><b>La Terraza</b>{T["who"]}</div></aside>
      <div class="crm-main">
        <div class="crm-top">{mark}<span class="crm-brand">La Terraza <span>&middot; {T["crm_tag"]}</span></span><span class="crm-live">{T["live"]}</span><div class="crm-tabs">{tabs}</div></div>
        <div class="crm-kpis">{kpis}</div>
        <div class="crm-title"><b>{T["crm_title"]}</b><em>{T["crm_when"]}</em></div>
        <table class="crm"><thead><tr>{ths}</tr></thead><tbody>
{chr(10).join(rows)}
        </tbody></table>
      </div>
    </div>'''


def stage(poster, src, aria, sound):
    return (f'<div class="stage-box" style="--poster:url({poster})"><video class="loop" controls muted loop playsinline preload="metadata" poster="{poster}" width="720" height="1280" aria-label="{aria}">'
            f'<source src="{src}" type="video/mp4"></video><button type="button" class="stage-sound">{sound}</button></div>')


def feature(T, flip, poster, src, aria, cap, eyebrow, h3, p, stats, link, btn):
    st = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in stats)
    return f'''    <div class="case-feature{" case-feature--flip" if flip else ""} reveal reveal-delay-1">
      <figure class="reel-frame">{stage(poster, src, aria, T["sound"])}
        <figcaption>{cap}</figcaption></figure>
      <div class="case-feature-text">
        <p class="eyebrow">{eyebrow}</p>
        <h3>{h3}</h3>
        <p>{p}</p>
        <div class="case-feature-stats">{st}</div>
        <a href="{link}" class="btn btn-secondary btn-arrow">{btn}</a>
      </div>
    </div>
'''


def build(lang, s, ver):
    T = L[lang]
    pre = T["pre"]
    marca = uno(r'<svg class="zenia-mark".*?</svg>', s).group(0)

    # 1. la conversación y el CRM, a la portada; la frase centrada sobre la foto
    demo = uno(r'\n<!-- DEMO: la conversación del agente -->\n<section class="demo" id="demo">.*?</section>\n', s)
    sec = demo.group(0)
    h2 = uno(r'<h2[^>]*>(.*?)</h2>', sec).group(1)
    switch = uno(r'<div class="demo-switch".*?</div>', sec).group(0)
    note = uno(r'<p class="demo-note"[^>]*>(.*?)</p>', sec).group(1)
    s = s[: demo.start()] + "\n" + s[demo.end():]
    tel = telefono(T, crm_html(T, marca)).replace("__SWITCH__", switch)
    bloque = f'''    <div class="hero-demo reveal reveal-delay-2">
      <p class="demo-caption" id="demoCaption">{h2}</p>
{tel}
      <p class="demo-note reveal reveal-delay-3">{note}</p>
    </div>
'''
    assert s.count('<section class="hero hero-portada" id="hero">') == 1
    s = s.replace('<section class="hero hero-portada" id="hero">', '<section class="hero hero-portada" id="hero">\n  <div class="hero-net" aria-hidden="true"></div>\n  <div class="hero-photo" aria-hidden="true"><picture><source media="(max-width: 768px)" srcset="/assets/images/hero-madrid-m.webp"><img src="/assets/images/hero-madrid.webp" width="2400" height="1109" alt="" decoding="async" fetchpriority="high"></picture></div>', 1)
    s = re.sub(r'(<section class="hero[^"]*" id="hero">\s*(?:<div class="hero-net"[^\n]*\n)?\s*(?:<div class="hero-photo"[^\n]*\n)?\s*<div class="container">\s*)',
               lambda m: m.group(1) + f'<p class="eyebrow">{T["eyebrow"]}</p>\n    ', s, count=1)
    hero = uno(r'<section class="hero[^"]*" id="hero">.*?</section>', s)
    h = hero.group(0)
    cierre = h.rfind("</div>\n</section>")
    assert cierre > 0
    h = h[:cierre] + bloque + "  " + h[cierre:]
    ini = h.index('<p class="eyebrow">')
    fin = h.index('    <div class="hero-demo')
    h = h[:ini] + '<div class="hero-copy">\n    ' + h[ini:fin] + '    </div>\n' + h[fin:]
    s = s[: hero.start()] + h + s[hero.end():]
    assert s.count('hero-copy') == 1
    old_sub = uno(r'<p class="hero-subtitle reveal reveal-delay-2"[^>]*>.*?</p>', s).group(0)
    s = s.replace(old_sub, f'<p class="hero-subtitle reveal reveal-delay-2">{T["subtitle"]}</p>', 1)

    # 2. la banda de herramientas
    items = "".join(f"<li>{icono(k)}<span>{n}</span></li>" for k, n in TOOLS)
    strip = f'<section class="strip" aria-label="{T["strip_aria"]}">\n  <div class="container">\n    <p class="strip-label">{T["strip_label"]}</p>\n    <ul>{items}</ul>\n  </div>\n</section>'
    assert s.count('<section class="opportunities" id="opportunities">') == 1
    s = s.replace('<section class="opportunities" id="opportunities">', strip + '\n\n<section class="opportunities" id="opportunities">', 1)

    # 3. secciones numeradas (las que existan en este idioma)
    for sel in ('class="opportunities" id="opportunities"', 'class="tailor" id="tailor"', 'class="section" id="services"',
                'class="section process" id="process"', 'class="section" id="impact"', 'class="proof" id="proof"',
                'class="faq-section" id="faq"', 'class="section index" id="verticales"', 'class="section pricing" id="precios"'):
        if s.count(f'<section {sel}>') == 1:
            s = s.replace(f'<section {sel}>', '<section ' + sel.replace('class="', 'class="numbered ', 1) + '>', 1)
    assert s.count('class="numbered ') >= 7

    # 4. tipografía
    s = re.sub(r"family=Source\+Serif\+4:[^&\"]+&family=Space\+Grotesk:wght@700", FONTS.split("css2?")[1].split("&display")[0], s)
    assert "Cormorant" in s

    # 5. la tarjeta de SaaS: el vídeo de GWB Network y lo que lleva la plataforma
    fig = (f'<figure class="service-figure is-video reel-frame">{stage("/cases/img/gwb-network-poster.webp", "/cases/video/gwb-network.mp4", T["saas_aria"], T["sound"])}'
           f'<figcaption>{T["saas_cap"]}</figcaption></figure>')
    m = uno(r'(<div class="service-card service-card--featured reveal">.*?<div class="service-card-body">.*?\n        </div>\n)(      </div>\n    </div>)', s)
    s = s[: m.end(1)] + "        " + fig + "\n" + s[m.end(1):]
    puntos = '\n          <ul class="service-points">' + "".join(f"<li>{x}</li>" for x in T["saas_points"]) + "</ul>"
    m2 = uno(r'(<div class="service-card-body">.*?<p[^>]*>[^<]*</p>)', s)
    s = s[: m2.end(1)] + puntos + s[m2.end(1):]
    assert s.count('service-figure') == 1 and 'service-points' in s

    # 6. el proceso: la línea de tiempo
    pasos = re.findall(r'<li class="process-step" style="--w:[0-9.]+"><h3[^>]*>(.*?)</h3><p[^>]*>(.*?)</p></li>', s)
    assert len(pasos) == 4, len(pasos)
    pos = [(0, 2), (2, 4), (4, 9.5), (9.5, 12)]
    filas = []
    for i, ((h3, ptxt), (a, b)) in enumerate(zip(pasos, pos)):
        inf = ' gantt-row--inf' if b >= 12 else ''
        filas.append(f'      <li class="gantt-row{inf}" style="--s:{a};--e:{b};--r:{i + 2}"><div class="gantt-text"><h3>{h3}</h3><p>{ptxt}</p><span class="gantt-dur">{T["durs"][i]}</span></div>'
                     f'<div class="gantt-track"><span class="gantt-bar"><i>{T["shorts"][i]}</i></span></div></li>')
    regla = "".join(f"<span>{T['wk1'] if i == 1 else i}</span>" for i in range(1, 11)) + f'<span class="gantt-inf">{T["onwards"]}</span>'
    gantt = (f'    <div class="gantt reveal reveal-delay-1" data-ui>\n      <div class="gantt-chart">\n        <div class="gantt-corner">{T["stage"]}</div>\n'
             f'        <div class="gantt-ruler" aria-hidden="true">{regla}<b class="gantt-ms" style="--x:8">{T["first"]}</b></div>\n'
             '        <div class="gantt-grid" aria-hidden="true"><span class="gantt-mark" style="--x:8"></span></div>\n'
             '        <ol class="gantt-rows">\n' + "\n".join(filas) + '\n        </ol>\n      </div>\n    </div>\n'
             f'    <p class="gantt-note reveal reveal-delay-2">{T["gantt_note"]}</p>')
    m = uno(r'    <div class="stage-bar reveal reveal-delay-1" data-ui>.*?</ol>\n', s)
    s = s[: m.start()] + gantt + "\n" + s[m.end():]
    assert 'stage-bar' not in s
    if T["copilots"] and s.count(T["copilots"][0]) == 1:
        s = s.replace(T["copilots"][0], T["copilots"][1], 1)

    # 7. fuera la frase de cifras (ya está en la rejilla) y la burbuja sobre el precio
    s = re.sub(r'\n\s*<p class="impact-sentence reveal"[^>]*>.*?</p>', '', s, count=1, flags=re.S)
    assert 'impact-sentence' not in s
    s = re.sub(r'\n\s*<div class="price-overlap" data-ui aria-hidden="true">.*?</div></div>', '', s, count=1, flags=re.S)
    assert 'price-overlap' not in s

    # 8. los dos casos destacados con vídeo, antes de las fotos
    f1 = feature(T, False, "/cases/img/gwb-agente-poster.webp", "/cases/video/gwb-agente-247am.mp4", T["gwb_aria"], T["gwb_cap"], T["gwb_eyebrow"], T["gwb_h3"], T["gwb_p"], T["gwb_stats"], T["gwb_link"], T["gwb_btn"])
    f2 = feature(T, True, "/cases/img/ts-unmakeable-poster.webp", "/cases/video/ts-unmakeable.mp4", T["ts_aria"], T["ts_cap"], T["ts_eyebrow"], T["ts_h3"], T["ts_p"], T["ts_stats"], T["ts_link"], T["ts_btn"])
    assert s.count('    <div class="work-strip reveal reveal-delay-1">') == 1
    s = s.replace('    <div class="work-strip reveal reveal-delay-1">', f1 + f2 + '    <div class="work-strip reveal reveal-delay-1">', 1)

    # 8b. el cierre, con la fotografía velada
    assert s.count('<div class="cta-box reveal">') == 1
    s = s.replace('<div class="cta-box reveal">', '<div class="cta-box reveal">\n      <div class="cta-bg" aria-hidden="true"><img src="/assets/images/hero-madrid.webp" width="2400" height="1109" alt="" loading="lazy" decoding="async"></div>', 1)

    # 8c. el pie: símbolo, nombre, lema y acción en vez del nombre gigante
    wm = uno(r'    <svg class="footer-wordmark".*?</svg>\n', s).group(0)
    cabecera = (f'    <div class="footer-head">\n      <a href="{T["home"]}" class="footer-brand">{marca}<span>ZENIA</span></a>\n'
                f'      <p class="footer-tag">{T["footer_tag"]}</p>\n'
                f'      <a href="#" onclick="openCalendly(event)" class="btn btn-primary btn-arrow">{T["footer_cta"]}</a>\n    </div>\n')
    s = s.replace(wm, cabecera, 1)
    assert 'footer-head' in s and 'footer-wordmark' not in s
    assert s.count('<a href="#" class="footer-top"') == 1
    s = s.replace('<a href="#" class="footer-top"', '<a href="#hero" class="footer-top"', 1)

    # 9. nota de marcas y crédito de la foto en el pie
    anchor = '</p>\n      </div>\n      <div class="footer-columns">'
    assert s.count(anchor) == 1
    s = s.replace(anchor, f'</p>\n        <p class="footer-brands">{T["brands"]}</p>\n        <p class="footer-credit">{T["credit"]}</p>\n      </div>\n      <div class="footer-columns">', 1)

    # 10. iconos decorativos fuera del lector de pantalla
    s = s.replace('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
                  '<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">')

    # 11a. títulos que abren con h3 y cierran con h4 (error antiguo de la portada inglesa)
    s = re.sub(r'(<h3\b[^>]*>[^<]*)</h4>', r'\1</h3>', s)

    # 11b. al punto: una sola frase en las descripciones y fuera lo redundante
    def primera(frase):
        m = re.match(r'(.*?[.!?])(\s+\S.*)$', frase.strip(), re.S)
        return m.group(1) if m else frase
    def corta(m):
        return m.group(1) + primera(m.group(2)) + m.group(3)
    for pat in (r'(<div class="opp-card[^"]*">.*?<p>)(.*?)(</p>)',
                r'(<div class="service-card[^>]*>.*?<p[^>]*>)(.*?)(</p>)',
                r'(<p class="section-desc"[^>]*>)(.*?)(</p>)',
                r'(<div class="tailor-text[^"]*">.*?<h2[^>]*>.*?</h2>\s*<p[^>]*>)(.*?)(</p>)',
                r'(<div class="tailor-point">.*?<p[^>]*>)(.*?)(</p>)',
                r'(<div class="vision-pillar[^"]*">.*?<p[^>]*>)(.*?)(</p>)',
                r'(<div class="cta-box reveal">.*?<p[^>]*>)(.*?)(</p>)',
                r'(<td>)([^<]{140,})(</td>)'):
        s = re.sub(pat, corta, s, flags=re.S)
    # las cifras de impacto: número y etiqueta, sin párrafo
    s = re.sub(r'(<div class="impact-card[^"]*">.*?</h3>)\s*<p[^>]*>.*?</p>', r'\1', s, flags=re.S)
    # el enfoque: las tres tarjetas sin párrafo (ya lo dicen los tres puntos)
    s = re.sub(r'(<div class="tailor-card[^"]*">.*?</h3>)\s*<p[^>]*>.*?</p>', r'\1', s, flags=re.S)
    # la tarjeta de SaaS: fuera el párrafo, se quedan los tres puntos
    s = re.sub(r'(<div class="service-card-body">.*?</h3>)\s*<p[^>]*>.*?</p>', r'\1', s, count=1, flags=re.S)
    # pies de las fotos de casos: solo el nombre del trabajo
    s = re.sub(r'(<figure><img[^>]*>\s*<figcaption>)([^<:]*):[^<]*(</figcaption>)', r'\1\2\3', s)
    # la nota de la conversación
    s = re.sub(r'(<p class="demo-note[^"]*">)(.*?)(</p>)', lambda m: m.group(1) + ("Conversaci&oacute;n de ejemplo. El flujo es el real." if lang == "es" else "Example conversation. The flow is the real one.") + m.group(3), s, count=1, flags=re.S)

    # 11c. botones del cierre, cortos
    for a, b in (("Agenda tu Sesi&oacute;n Estrat&eacute;gica de IA", "Agenda tu sesi&oacute;n estrat&eacute;gica"), ("Ver Proceso de Transformaci&oacute;n", "Ver el proceso"),
                 ("Book Your AI Strategy Session", "Book your strategy session"), ("See Transformation Process", "See the process"), ("View Transformation Process", "See the process")):
        s = s.replace(a, b)

    # 11. hoja, scripts y color del tema
    n = 0
    for old in (f'<link rel="stylesheet" href="{pre}styles/main.css?v=11">', f'<link rel="stylesheet" href="{pre}styles/main.css?v=10">'):
        if old in s:
            s = s.replace(old, f'<link rel="stylesheet" href="{pre}styles/home.css?v={ver}">', 1); n += 1
    assert n == 1, "no encuentro el <link> de main.css"
    old_js = f'<script defer src="{pre}js/demo-chat.js?v=1"></script>'
    assert s.count(old_js) == 1
    s = s.replace(old_js, f'<script defer src="{pre}js/demo-chat.js?v={ver}"></script>\n<script defer src="{pre}js/hero-net.js?v={ver}"></script>\n<script defer src="{pre}js/loops.js?v={ver}"></script>', 1)
    s = s.replace('<meta name="theme-color" content="#F4F4F1">', '<meta name="theme-color" content="#0B1220">')
    # el contador de Cloudflare con el token de envío (la fuente de la rama trae el identificador de consulta)
    s = s.replace('"token": "67e4803d7cd443a49b12c7d8a99365bf"', '"token": "eceeed460f6d465bba3b970417d5f6b0"')
    # la tarjeta de vista previa (WhatsApp, LinkedIn, X) propia de cada portada
    og = f"https://zeniapartners.com/assets/images/og-home-{lang}.jpg"
    n_og = s.count('<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">')
    assert n_og == 1, n_og
    s = s.replace('<meta property="og:image" content="https://zeniapartners.com/assets/images/og-image.png">',
                  f'<meta property="og:image" content="{og}">\n<meta property="og:image:secure_url" content="{og}">\n<meta property="og:image:type" content="image/jpeg">', 1)
    s = s.replace('<meta name="twitter:image" content="https://zeniapartners.com/assets/images/og-image.png">', f'<meta name="twitter:image" content="{og}">', 1)
    assert s.count(og) == 3, s.count(og)
    if lang == "en":
        # la portada inglesa es monolingüe: sin marcas data-i18n, el script de traducción no vuelve a
        # escribir en vivo los textos recortados (i18n.js sigue cargado para el formulario de reserva)
        s = re.sub(r'\s+data-i18n(?:-html)?="[^"]*"', '', s)
        assert 'data-i18n' not in s
        # el aviso de cookies, en inglés
        s = s.replace('Usamos cookies para analítica (Google Analytics) y mejorar tu experiencia. No compartimos datos con terceros. <a href="/privacy/" style="color:#1D4ED8;text-decoration:underline;">Política de privacidad</a>',
                      'We use cookies for analytics (Google Analytics) and to improve your experience. We do not share data with third parties. <a href="/privacy/" style="color:#1D4ED8;text-decoration:underline;">Privacy policy</a>', 1)
        s = s.replace('cursor:pointer;">Aceptar</button>', 'cursor:pointer;">Accept</button>', 1).replace('cursor:pointer;">Rechazar</button>', 'cursor:pointer;">Reject</button>', 1)
        assert 'Privacy policy' in s and '>Accept<' in s, "aviso de cookies no traducido"
        # quien navega en español va a la portada en español completa (antes se traducía a medias en el navegador)
        red = ('<script>(function(){try{var q=new URLSearchParams(location.search).get("lang");if(q==="en")return;var s=localStorage.getItem("zenia-lang-v2");'
               'var n=(navigator.languages&&navigator.languages[0])||navigator.language||"";if(q==="es"||s==="es"||(!s&&/^es/i.test(n))){location.replace("/es/"+location.hash);}}catch(e){}})();</script>\n')
        assert s.count('<script src="js/i18n.js?v=7"></script>') == 1
        s = s.replace('<script src="js/i18n.js?v=7"></script>', red + '<script src="js/i18n.js?v=8"></script>', 1)
    return s


def main():
    ver = str(int(time.time()))
    css = leer(os.path.join(SRC, "styles", "main.css")) + "\n\n" + leer(OVER) + "\n\n" + C_CSS
    escribir(os.path.join(OUT, "styles", "home.css"), css)
    for lang, rel in (("es", os.path.join("es", "index.html")), ("en", "index.html")):
        out = build(lang, leer(os.path.join(SRC, rel)), ver)
        escribir(os.path.join(OUT, rel), out)
        print(rel, len(out), "v=" + ver)


if __name__ == "__main__":
    main()
