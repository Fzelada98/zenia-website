#!/usr/bin/env python3
"""ZENIA · páginas de vídeo por prospecto (nov-2026): /v/<negocio>-<código>/.

Para la prospección con vídeo en vez de correo genérico: cada negocio recibe un enlace a SU página, con el vídeo de
su nicho (v/media/zenia-<nicho>.mp4, el mismo para todos los de ese nicho) y su nombre. La página avisa cuando le dan
a reproducir y cuando lo ven entero (registro en gaia, site «zenia-demo», kind «video» / «video-fin»), igual que las demos.
La lista de prospectos vive fuera del repo.

Uso: python3 scripts/videos/build_videos.py <prospectos-video.json> [RAÍZ_DEL_SITIO]
Cada elemento: {nicho: clinicas|talleres|autoescuelas, slug, codigo, nombre}. Escribe v/<slug>-<codigo>/index.html. Idempotente."""
import html
import json
import os
import sys
import urllib.parse

VERSION = '1'
WA = '34677612799'
CALENDLY = 'https://calendly.com/zeladauriartef/30min'
N = {
    'clinicas': dict(tu='vuestra clínica', un='una clínica', cerrada='cuando la clínica está cerrada'),
    'talleres': dict(tu='vuestro taller', un='un taller', cerrada='cuando el taller está cerrado'),
    'autoescuelas': dict(tu='vuestra autoescuela', un='una autoescuela', cerrada='cuando la autoescuela está cerrada'),
}
MARK = ('<svg viewBox="0 0 140 140" aria-hidden="true"><defs><linearGradient id="zb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2563EB"/>'
        '<stop offset="1" stop-color="#3B82F6"/></linearGradient><linearGradient id="zv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366F1"/>'
        '<stop offset="1" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="30" fill="#111A2E"/>'
        '<path d="M70 18Q18 18 18 38v19q0 6 6 6h64Z" fill="url(#zb)"/><path d="M70 122q52 0 52-20V83q0-6-6-6H52Z" fill="url(#zv)"/></svg>')
WA_ICO = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88M20.46 3.49A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.42"/></svg>')


def pagina(p):
    e = lambda s: html.escape(str(s or ''), quote=True)
    n = N[p['nicho']]; nombre = p['nombre']
    wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(f'Hola, Fabrizzio. Soy de {nombre}. He visto el vídeo y quiero ver la demo con nuestro negocio.')
    mail = ('mailto:fabrizzio.zelada@zeniapartners.com?subject=' + urllib.parse.quote(f'Demo para {nombre}')
            + '&body=' + urllib.parse.quote(f'Hola, Fabrizzio:\n\nHe visto el vídeo. Me interesa ver la demo con {nombre}.\n\n'))
    datos = json.dumps({'nombre': nombre, 'nicho': p['nicho']}, ensure_ascii=False).replace('</', '<\\/')
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(nombre)}: 78 segundos sobre vuestro WhatsApp | Zenia</title>
<meta name="description" content="Un vídeo de 78 segundos: qué pasa con los mensajes que llegan {e(n['cerrada'])} y cómo los contesta un agente de IA.">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<meta name="theme-color" content="#070B13">
<meta property="og:type" content="video.other">
<meta property="og:title" content="{e(nombre)}: 78 segundos sobre vuestro WhatsApp">
<meta property="og:description" content="Qué pasa con los mensajes que llegan {e(n['cerrada'])}, y cómo los contesta un agente de IA.">
<meta property="og:image" content="https://zeniapartners.com/v/media/zenia-{p['nicho']}.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/v/assets/v.css?v={VERSION}">
</head>
<body>
<header class="top"><a class="brand" href="https://zeniapartners.com/es/{p['nicho']}/">{MARK}<span>Zenia</span></a><small>Vídeo para <b>{e(nombre)}</b></small></header>
<main class="wrap">
  <div class="txt">
    <p class="label">Preparado para {e(nombre)}</p>
    <h1>78 segundos sobre el WhatsApp de <span>{e(n['tu'])}</span></h1>
    <p class="lead">Qué pasa con los mensajes que llegan {e(n['cerrada'])}, y cómo los contesta un agente de IA en vuestro propio WhatsApp.</p>
    <div class="cta desk">
      <p class="q">¿Lo vemos con {e(nombre)}?</p>
      <p class="s">En 48 horas te preparo una demo con la información de vuestra web. Sin compromiso.</p>
      <div class="btns"><a class="btn wa" href="{e(wa)}" target="_blank" rel="noopener">{WA_ICO}Quiero mi demo</a><a class="btn ghost" href="{e(mail)}">Responder por correo</a><a class="btn ghost" href="{CALENDLY}" target="_blank" rel="noopener">Reservar 30 minutos</a></div>
    </div>
  </div>
  <div class="player" id="player">
    <video id="vid" playsinline preload="metadata" poster="/v/media/zenia-{p['nicho']}.jpg" src="/v/media/zenia-{p['nicho']}.mp4"></video>
    <button class="play" id="play" type="button" aria-label="Reproducir el vídeo con sonido"><i></i><span>Ver el vídeo · 78 s</span></button>
  </div>
  <div class="cta mob">
    <p class="q">¿Lo vemos con {e(nombre)}?</p>
    <p class="s">En 48 horas te preparo una demo con la información de vuestra web. Sin compromiso.</p>
    <div class="btns"><a class="btn wa" href="{e(wa)}" target="_blank" rel="noopener">{WA_ICO}Quiero mi demo</a><a class="btn ghost" href="{e(mail)}">Responder por correo</a><a class="btn ghost" href="{CALENDLY}" target="_blank" rel="noopener">Reservar 30 minutos</a></div>
  </div>
</main>
<footer><span>Fabrizzio Zelada · Zenia Partners · Madrid</span><span>Las pantallas del vídeo son de ejemplo. <a href="https://zeniapartners.com/es/{p['nicho']}/">zeniapartners.com</a></span></footer>
<script type="application/json" id="v-data">{datos}</script>
<script src="/v/assets/v.js?v={VERSION}" defer></script>
</body>
</html>
'''


def main():
    lista = json.load(open(sys.argv[1], encoding='utf-8'))
    raiz = sys.argv[2] if len(sys.argv) > 2 else '.'
    for p in lista:
        d = os.path.join(raiz, 'v', f"{p['slug']}-{p['codigo']}")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(pagina(p))
    print(len(lista), 'páginas en', os.path.join(raiz, 'v'))


if __name__ == '__main__':
    main()
