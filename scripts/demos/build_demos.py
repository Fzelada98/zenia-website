#!/usr/bin/env python3
"""ZENIA, demos privadas por negocio (nov-2026): /demo/<negocio>-<código>/.

Para el seguimiento de prospectos que no contestaron al correo: en vez de otro correo genérico, una
página con SU nombre donde prueban cómo contestaría su WhatsApp un agente de IA (preguntas que se
tocan, cita con huecos de ejemplo) y ven la ficha del CRM rellenarse. Los datos salen solo de su web
pública (fichas JSON hechas fuera del repo: no se publica la lista de prospectos). Sin IA ni servidor.

Uso: python3 scripts/demos/build_demos.py <carpeta_con_json> [RAÍZ_DEL_SITIO]
Escribe demo/<slug>-<código>/index.html y lista las URLs. Idempotente.
"""
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse

VERSION = '1'
BASE = 'https://zeniapartners.com'
CALENDLY = 'https://calendly.com/zeladauriartef/30min'
WA = '34677612799'

PERSONA = {'clinica': ('paciente', 'pacientes'), 'taller': ('cliente', 'clientes'), 'autoescuela': ('alumno', 'alumnos')}
CHIP_CITA = {'clinica': 'Pedir cita', 'taller': 'Pedir cita en el taller', 'autoescuela': 'Quiero apuntarme'}


def codigo(slug):
    return hashlib.sha1((slug + '|zx-demo-2026').encode()).hexdigest()[:4]


def color_ok(c):
    """Color de marca para el avatar si es lo bastante oscuro para letra blanca; si no, azul Zenia."""
    if not c or not re.fullmatch(r'#[0-9a-fA-F]{6}', c):
        return '#2563EB'
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return c if lum < 0.55 else '#2563EB'


def minus(s):
    s = (s or '').strip()
    return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s


def pagina(d):
    e = lambda s: html.escape(str(s or ''), quote=True)
    nombre = d['nombre']
    vert = d.get('vertical') if d.get('vertical') in PERSONA else 'clinica'
    uno, varios = PERSONA[vert]
    sedes = [s for s in (d.get('sedes') or []) if s.get('nombre')]
    host = urllib.parse.urlparse(d.get('web') or '').netloc.replace('www.', '') or 'su web'
    datos = {
        'nombre': nombre, 'vertical': vert,
        'conversacion': [{'pregunta': q['pregunta'], 'respuesta': q['respuesta'], 'tipo': q.get('tipo', 'info')}
                         for q in d['conversacion']],
        'cita_demo': {'pregunta': d['cita_demo']['pregunta'], 'servicio': minus(d['cita_demo']['servicio']),
                      'sede': d['cita_demo']['sede'], 'respuesta_intro': d['cita_demo']['respuesta_intro'],
                      'chip': CHIP_CITA[vert]},
    }
    wa_txt = urllib.parse.quote(f'Hola Fabrizzio, he visto la demo de {nombre} y me gustaría verlo con más calma.')
    n_sedes = len(sedes)
    sedes_html = ''.join(f'<span>{e(s["nombre"])}</span>' for s in sedes)
    lead = {
        'clinica': 'Un agente de IA que responde a tus pacientes en segundos, también de noche y en fin de semana, con la información de tu web, y les reserva la cita.',
        'taller': 'Un agente de IA que responde a tus clientes en segundos, también fuera de horario, con la información de tu web, y les reserva el hueco en el taller.',
        'autoescuela': 'Un agente de IA que responde a tus futuros alumnos en segundos, también de noche y en fin de semana, con la información de tu web, y los apunta.',
    }[vert]
    con_agente = (f'Contesta en segundos a cualquier hora, reparte cada consulta a su sede y reserva sin que nadie tenga que coger el teléfono.'
                  if n_sedes > 1 else 'Contesta en segundos a cualquier hora y reserva sin que nadie tenga que coger el teléfono.')
    data_json = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Demo para {e(nombre)} · Zenia Partners</title>
<meta name="description" content="Demo privada: así contestaría el WhatsApp de {e(nombre)} un agente de IA.">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/demo/assets/demo.css?v={VERSION}">
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "eceeed460f6d465bba3b970417d5f6b0"}}'></script>
</head>
<body>
<header class="wrap top"><a class="wordmark" href="{BASE}/es/">ZENIA</a><small>Demo privada<span class="largo"> para {e(nombre)}</span></small></header>
<main>
<section class="wrap hero">
  <p class="eyebrow">Preparada para {e(nombre)}</p>
  <h1>Así contestaría el WhatsApp de <em>{e(nombre)}</em></h1>
  <p class="lead">{lead}</p>
  <p class="hint"><span class="dot"></span><span><b>Pruébalo:</b> toca una pregunta debajo del chat, como haría un {uno} desde el móvil.</span></p>
</section>
<div class="wrap scene">
  <div class="crm" aria-label="CRM a medida de {e(nombre)}">
    <div class="crm-top"><span class="crm-brand">{e(nombre)} <span>· CRM a medida</span></span><span class="crm-live">En directo</span></div>
    <div class="crm-kpis">
      <div class="crm-kpi"><small>Respondidas por el agente</small><strong id="kOk">0</strong></div>
      <div class="crm-kpi"><small>Citas reservadas</small><strong id="kCita">0</strong></div>
      <div class="crm-kpi"><small>Pasadas a tu equipo</small><strong id="kEsc">0</strong></div>
    </div>
    <div class="crm-section">
      <p class="crm-title"><b>Conversaciones de esta visita</b><em>{f"{n_sedes} sedes" if n_sedes > 1 else e(host)}</em></p>
      <table class="crm-table"><thead><tr><th>Hora</th><th>Motivo</th><th class="opt">Detalle</th><th>Estado</th></tr></thead>
      <tbody id="crmRows"><tr class="crm-empty"><td colspan="4">Aún no hay conversaciones: toca una pregunta en el WhatsApp.</td></tr></tbody></table>
    </div>
    <div class="crm-card" id="crmCard" hidden>
      <div><small>Contacto</small>Laura Gómez (ejemplo)</div>
      <div><small>Origen</small>WhatsApp · atendido por el agente</div>
      <div><small>Servicio</small><span data-k="servicio"></span></div>
      <div><small>Sede</small><span data-k="sede"></span></div>
      <div><small>Cuándo</small><span data-k="cuando"></span></div>
      <div><small>Recordatorio</small>El día antes, por WhatsApp</div>
    </div>
  </div>
  <div class="phone" style="--brand:{color_ok(d.get('color'))}">
    <div class="phone-status" aria-hidden="true"><span id="phoneTime">9:41</span><span><svg viewBox="0 0 16 12"><path fill="currentColor" d="M0 9h2v3H0zM4 6h2v6H4zM8 3h2v9H8zM12 0h2v12h-2z"/></svg><svg viewBox="0 0 24 12"><rect x=".5" y=".5" width="20" height="11" rx="2.5" fill="none" stroke="currentColor"/><rect x="2" y="2" width="16" height="8" rx="1.5" fill="currentColor"/></svg></span></div>
    <div class="chat">
      <div class="chat-head"><span class="chat-avatar" aria-hidden="true">{e(nombre[:1].upper())}</span><div class="chat-who"><strong>{e(nombre)}</strong><span class="chat-status" id="chatStatus">en línea</span></div></div>
      <div class="chat-body" id="chatBody" aria-live="polite">
        <div class="chat-day">Hoy</div>
        <div class="chat-lock">Los mensajes están cifrados de extremo a extremo.</div>
        <div class="chat-day">Toca una pregunta de abajo para empezar</div>
      </div>
      <div class="chips" id="chips" role="group" aria-label="Preguntas de ejemplo"></div>
      <div class="chat-input" aria-hidden="true"><span>Mensaje</span><i></i></div>
    </div>
    <noscript><p style="color:#fff;padding:12px">Activa JavaScript para probar la demo.</p></noscript>
  </div>
</div>
<section class="band"><div class="wrap">
  <p class="eyebrow">Qué cambia</p>
  <h2>Lo que cambia en <em>{e(nombre)}</em></h2>
  <div class="grid3">
    <div class="glass"><h3>Hoy</h3><p>{e(d.get('dolor'))}</p></div>
    <div class="glass"><h3>Con el agente</h3><p>{con_agente}</p></div>
    <div class="glass"><h3>Tu equipo</h3><p>Ve cada conversación en el CRM, con su sede y su motivo, y solo entra en lo que necesita una persona.</p></div>
  </div>
  {f'<div class="sedes" aria-label="Sedes">{sedes_html}</div>' if n_sedes > 1 else ''}
</div></section>
<section class="band cta"><div class="wrap">
  <h2>¿Lo vemos con <em>tus preguntas</em>?</h2>
  <p class="lead">En 30 minutos te enseño cómo quedaría conectado a tu agenda y a tu WhatsApp, con las preguntas que de verdad os hacen tus {varios}. Sin compromiso.</p>
  <div class="btns"><a class="btn btn-primary" href="{CALENDLY}" target="_blank" rel="noopener">Reservar 30 minutos</a><a class="btn btn-ghost" href="https://wa.me/{WA}?text={wa_txt}" target="_blank" rel="noopener">Escribir por WhatsApp</a></div>
  <p class="note">Demo preparada por Zenia Partners con la información pública de {e(host)}, consultada en noviembre de 2026. No está conectada a la agenda de {e(nombre)}: los huecos y el nombre del {uno} son de ejemplo. En el agente real, lo que no sabe lo pasa a una persona de tu equipo.</p>
</div></section>
</main>
<footer><div class="wrap"><span>Zenia Partners · Madrid</span><a href="{BASE}/es/">zeniapartners.com</a></div></footer>
<script type="application/json" id="demo-data">{data_json}</script>
<script src="/demo/assets/demo.js?v={VERSION}"></script>
</body>
</html>
'''


def main(datos, raiz='.'):
    urls = []
    for f in sorted(os.listdir(datos)):
        if not f.endswith('.json'):
            continue
        d = json.load(open(os.path.join(datos, f), encoding='utf-8'))
        ruta = f"demo/{d['slug']}-{codigo(d['slug'])}"
        os.makedirs(os.path.join(raiz, ruta), exist_ok=True)
        open(os.path.join(raiz, ruta, 'index.html'), 'w', encoding='utf-8').write(pagina(d))
        urls.append((d['nombre'], f'{BASE}/{ruta}/'))
    return urls


if __name__ == '__main__':
    for nombre, url in main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else '.'):
        print(f'{nombre}: {url}')
