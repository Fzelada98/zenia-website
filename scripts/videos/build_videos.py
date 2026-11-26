#!/usr/bin/env python3
"""ZENIA · páginas de vídeo por prospecto (nov-2026): /v/<negocio>-<código>/.

Para la prospección con vídeo en vez de correo genérico: cada negocio recibe un enlace a SU página, con el vídeo de
su nicho (v/media/zenia-<nicho>.mp4, el mismo para todos los de ese nicho) y su nombre. La página avisa cuando le dan
a reproducir y cuando lo ven entero (registro en gaia, site «zenia-demo», kind «video» / «video-fin»), igual que las demos.
La lista de prospectos vive fuera del repo.

Uso: python3 scripts/videos/build_videos.py <prospectos-video.json> [RAÍZ_DEL_SITIO]
Cada elemento: {nicho: clinicas|talleres|autoescuelas|inmobiliarias|veterinarias|academias|estetica|laser|gimnasios|estudios|coches, slug, codigo, nombre} y, si hace falta,
«tu» (p. ej. «vuestro hospital») o «cerrada» para afinar el texto de ese negocio. Escribe v/<slug>-<codigo>/index.html. Idempotente.
Cada nicho lleva la duración de su vídeo («seg») y la página a la que enlaza el logo («enlace»).

19-nov-2026, prueba A/B: una ficha con "variante": "B" lleva SU vídeo (v/media/p/<slug>-<codigo>.mp4 y .jpg, medio minuto,
el WhatsApp con el nombre del negocio; lo hace «Vídeos por nicho/v2/hacer.py») y otro texto. Las demás no cambian.
Las páginas generadas desde ese día llevan además el contador de Cloudflare (respaldo si gaia no guarda las reproducciones)."""
import html
import json
import os
import sys
import urllib.parse

VERSION = '1'
WA = '34677612799'
CALENDLY = 'https://calendly.com/zeladauriartef/30min'
N = {
    'clinicas': dict(tu='vuestra clínica', un='una clínica', cerrada='cuando la clínica está cerrada', seg=78, enlace='/es/clinicas/'),
    'talleres': dict(tu='vuestro taller', un='un taller', cerrada='cuando el taller está cerrado', seg=78, enlace='/es/talleres/'),
    'autoescuelas': dict(tu='vuestra autoescuela', un='una autoescuela', cerrada='cuando la autoescuela está cerrada', seg=78, enlace='/es/autoescuelas/'),
    # 18-nov-2026: dos nichos más (todavía sin página propia de nicho: el logo lleva a la portada)
    'inmobiliarias': dict(tu='vuestra inmobiliaria', un='una inmobiliaria', cerrada='cuando la oficina está cerrada', seg=80, enlace='/es/'),
    'veterinarias': dict(tu='vuestra clínica', un='una clínica veterinaria', cerrada='fuera del horario de consulta', seg=80, enlace='/es/'),
    # 24-nov-2026: nichos nuevos, solo con vídeo propio (variante B) y la demo gratis como gancho ("oferta": "demo-gratis")
    'academias': dict(tu='vuestra academia', un='una academia', cerrada='cuando la academia está cerrada', seg=33, enlace='/es/'),
    'estetica': dict(tu='vuestro centro', un='un centro de estética', cerrada='cuando el centro está cerrado', seg=33, enlace='/es/'),
    'laser': dict(tu='vuestro centro', un='un centro de depilación láser', cerrada='cuando el centro está cerrado', seg=33, enlace='/es/'),
    'gimnasios': dict(tu='vuestro centro', un='un gimnasio', cerrada='cuando no hay nadie en recepción', seg=33, enlace='/es/'),
    'estudios': dict(tu='vuestro estudio', un='un estudio', cerrada='cuando el estudio está cerrado', seg=33, enlace='/es/'),
    'coches': dict(tu='vuestra exposición', un='una compraventa', cerrada='cuando la exposición está cerrada', seg=33, enlace='/es/'),
}
NOCHE = {'clinicas': '21:45', 'talleres': '21:00', 'autoescuelas': '23:00', 'inmobiliarias': '22:30', 'veterinarias': '22:00',   # hora del mensaje en el vídeo B
         'academias': '22:30', 'estetica': '22:15', 'laser': '22:15', 'gimnasios': '22:45', 'estudios': '22:20', 'coches': '22:40'}
CF = '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "eceeed460f6d465bba3b970417d5f6b0"}\'></script>'
MARK = ('<svg viewBox="0 0 140 140" aria-hidden="true"><defs><linearGradient id="zb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2563EB"/>'
        '<stop offset="1" stop-color="#3B82F6"/></linearGradient><linearGradient id="zv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366F1"/>'
        '<stop offset="1" stop-color="#7C3AED"/></linearGradient></defs><rect width="140" height="140" rx="30" fill="#111A2E"/>'
        '<path d="M70 18Q18 18 18 38v19q0 6 6 6h64Z" fill="url(#zb)"/><path d="M70 122q52 0 52-20V83q0-6-6-6H52Z" fill="url(#zv)"/></svg>')
WA_ICO = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88M20.46 3.49A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.42"/></svg>')


def pagina(p):
    e = lambda s: html.escape(str(s or ''), quote=True)
    n = dict(N[p['nicho']], **{k: p[k] for k in ('tu', 'cerrada') if p.get(k)}); nombre = p['nombre']
    wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(f'Hola, Fabrizzio. Soy de {nombre}. He visto el vídeo y quiero ver la demo con nuestro negocio.')
    mail = ('mailto:fabrizzio.zelada@zeniapartners.com?subject=' + urllib.parse.quote(f'Demo para {nombre}')
            + '&body=' + urllib.parse.quote(f'Hola, Fabrizzio:\n\nHe visto el vídeo. Me interesa ver la demo con {nombre}.\n\n'))
    datos = json.dumps({'nombre': nombre, 'nicho': p['nicho']}, ensure_ascii=False).replace('</', '<\\/')
    if p.get('variante') == 'B':
        return pagina_b(p, n, wa, mail, datos)
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(nombre)}: {n['seg']} segundos sobre vuestro WhatsApp | Zenia</title>
<meta name="description" content="Un vídeo de {n['seg']} segundos: qué pasa con los mensajes que llegan {e(n['cerrada'])} y cómo los contesta un agente de IA.">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<meta name="theme-color" content="#070B13">
<meta property="og:type" content="video.other">
<meta property="og:title" content="{e(nombre)}: {n['seg']} segundos sobre vuestro WhatsApp">
<meta property="og:description" content="Qué pasa con los mensajes que llegan {e(n['cerrada'])}, y cómo los contesta un agente de IA.">
<meta property="og:image" content="https://zeniapartners.com/v/media/zenia-{p['nicho']}.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/v/assets/v.css?v={VERSION}">
{CF if p.get('tanda', '') >= '2026-11-19' else ''}</head>
<body>
<header class="top"><a class="brand" href="https://zeniapartners.com{n['enlace']}">{MARK}<span>Zenia</span></a><small>Vídeo para <b>{e(nombre)}</b></small></header>
<main class="wrap">
  <div class="txt">
    <p class="label">Preparado para {e(nombre)}</p>
    <h1>{n['seg']} segundos sobre el WhatsApp de <span>{e(n['tu'])}</span></h1>
    <p class="lead">Qué pasa con los mensajes que llegan {e(n['cerrada'])}, y cómo los contesta un agente de IA en vuestro propio WhatsApp.</p>
    <div class="cta desk">
      <p class="q">¿Lo vemos con {e(nombre)}?</p>
      <p class="s">En 48 horas te preparo una demo con la información de vuestra web. Sin compromiso.</p>
      <div class="btns"><a class="btn wa" href="{e(wa)}" target="_blank" rel="noopener">{WA_ICO}Quiero mi demo</a><a class="btn ghost" href="{e(mail)}">Responder por correo</a><a class="btn ghost" href="{CALENDLY}" target="_blank" rel="noopener">Reservar 30 minutos</a></div>
    </div>
  </div>
  <div class="player" id="player">
    <video id="vid" playsinline preload="metadata" poster="/v/media/zenia-{p['nicho']}.jpg" src="/v/media/zenia-{p['nicho']}.mp4"></video>
    <button class="play" id="play" type="button" aria-label="Reproducir el vídeo con sonido"><i></i><span>Ver el vídeo · {n['seg']} s</span></button>
  </div>
  <div class="cta mob">
    <p class="q">¿Lo vemos con {e(nombre)}?</p>
    <p class="s">En 48 horas te preparo una demo con la información de vuestra web. Sin compromiso.</p>
    <div class="btns"><a class="btn wa" href="{e(wa)}" target="_blank" rel="noopener">{WA_ICO}Quiero mi demo</a><a class="btn ghost" href="{e(mail)}">Responder por correo</a><a class="btn ghost" href="{CALENDLY}" target="_blank" rel="noopener">Reservar 30 minutos</a></div>
  </div>
</main>
<footer><span>Fabrizzio Zelada · Zenia Partners · Madrid</span><span>Las pantallas del vídeo son de ejemplo. <a href="https://zeniapartners.com{n['enlace']}">zeniapartners.com</a></span></footer>
<script type="application/json" id="v-data">{datos}</script>
<script src="/v/assets/v.js?v={VERSION}" defer></script>
</body>
</html>
'''


def pagina_b(p, n, wa, mail, datos):
    """Variante B: el vídeo es del propio negocio (su nombre en la cabecera del WhatsApp)."""
    e = lambda s: html.escape(str(s or ''), quote=True)
    nombre = p['nombre']; noche = NOCHE[p['nicho']]; seg = int(p.get('seg') or 33); med = f"/v/media/p/{p['slug']}-{p['codigo']}"
    if p.get('media'):                                            # 24-nov-2026: vídeos fuera del repo de la web (p. ej. https://fzelada98.github.io/zenia-videos/p)
        med = f"{p['media'].rstrip('/')}/{p['slug']}-{p['codigo']}"
    og = med if med.startswith('http') else 'https://zeniapartners.com' + med
    if p.get('oferta') == 'demo-gratis':
        return pagina_gratis(p, n, datos, noche, seg, med, og)
    cta = (f'''<p class="q">¿Lo vemos con {e(nombre)}?</p>
      <p class="s">En 48 horas te preparo una demo con la información de la web de {e(nombre)}. Sin compromiso.</p>
      <div class="btns"><a class="btn wa" href="{e(wa)}" target="_blank" rel="noopener">{WA_ICO}Quiero mi demo</a><a class="btn ghost" href="{e(mail)}">Responder por correo</a><a class="btn ghost" href="{CALENDLY}" target="_blank" rel="noopener">Reservar 30 minutos</a></div>''')
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(nombre)}: el WhatsApp de las {noche} | Zenia</title>
<meta name="description" content="Medio minuto con el WhatsApp de {e(nombre)}: el mismo mensaje dos veces, primero sin nadie al otro lado y después con un agente de IA.">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<meta name="theme-color" content="#070B13">
<meta property="og:type" content="video.other">
<meta property="og:title" content="{e(nombre)}: el WhatsApp de las {noche}">
<meta property="og:description" content="El mismo mensaje, dos veces: sin nadie al otro lado y con un agente de IA contestando.">
<meta property="og:image" content="{og}.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/v/assets/v.css?v={VERSION}">
{CF}</head>
<body>
<header class="top"><a class="brand" href="https://zeniapartners.com{n['enlace']}">{MARK}<span>Zenia</span></a><small>Vídeo para <b>{e(nombre)}</b></small></header>
<main class="wrap">
  <div class="txt">
    <p class="label">Preparado para {e(nombre)}</p>
    <h1>Son las {noche} y alguien escribe a <span>{e(nombre)}</span></h1>
    <p class="lead">El mismo mensaje, dos veces: primero sin nadie al otro lado y después con un agente de IA contestando. Dura medio minuto.</p>
    <div class="cta desk">
      {cta}
    </div>
  </div>
  <div class="player" id="player">
    <video id="vid" playsinline preload="metadata" poster="{med}.jpg" src="{med}.mp4"></video>
    <button class="play" id="play" type="button" aria-label="Reproducir el vídeo con sonido"><i></i><span>Ver el vídeo · {seg} s</span></button>
  </div>
  <div class="cta mob">
    {cta}
  </div>
</main>
<footer><span>Fabrizzio Zelada · Zenia Partners · Madrid</span><span>La conversación del vídeo es de ejemplo. <a href="https://zeniapartners.com{n['enlace']}">zeniapartners.com</a></span></footer>
<script type="application/json" id="v-data">{datos}</script>
<script src="/v/assets/v.js?v={VERSION}" defer></script>
</body>
</html>
'''


def pagina_gratis(p, n, datos, noche, seg, med, og):
    """24-nov-2026: mismo vídeo propio, pero el gancho es la DEMO GRATIS (se pide con un toque) y no hay botón de Calendly
    (las llamadas las propone Fabrizzio a partir de las 19:00)."""
    e = lambda s: html.escape(str(s or ''), quote=True)
    nombre = p['nombre']
    wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(f'Hola, Fabrizzio. Soy de {nombre}. He visto el vídeo y quiero la demo gratis con nuestro negocio.')
    mail = ('mailto:fabrizzio.zelada@zeniapartners.com?subject=' + urllib.parse.quote(f'Demo gratis para {nombre}')
            + '&body=' + urllib.parse.quote(f'Hola, Fabrizzio:\n\nHe visto el vídeo. Quiero la demo gratis con {nombre}.\n\n'))
    cta = (f'''<p class="q">Pruébalo gratis con {e(nombre)}</p>
      <p class="s">En 48 horas te preparo una demo con la información de la web de {e(nombre)}, para que la pruebes en el móvil. Gratis y sin compromiso.</p>
      <div class="btns"><a class="btn wa" href="{e(wa)}" target="_blank" rel="noopener">{WA_ICO}Quiero mi demo gratis</a><a class="btn ghost" href="{e(mail)}">Pedirla por correo</a></div>''')
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(nombre)}: el WhatsApp de las {noche} | Zenia</title>
<meta name="description" content="Medio minuto con el WhatsApp de {e(nombre)}: el mismo mensaje dos veces, primero sin nadie al otro lado y después con un agente de IA.">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" type="image/svg+xml" href="/assets/icons/favicon.svg">
<meta name="theme-color" content="#070B13">
<meta property="og:type" content="video.other">
<meta property="og:title" content="{e(nombre)}: el WhatsApp de las {noche}">
<meta property="og:description" content="El mismo mensaje, dos veces: sin nadie al otro lado y con un agente de IA contestando.">
<meta property="og:image" content="{og}.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/v/assets/v.css?v={VERSION}">
{CF}</head>
<body>
<header class="top"><a class="brand" href="https://zeniapartners.com{n['enlace']}">{MARK}<span>Zenia</span></a><small>Vídeo para <b>{e(nombre)}</b></small></header>
<main class="wrap">
  <div class="txt">
    <p class="label">Preparado para {e(nombre)}</p>
    <h1>Son las {noche} y alguien escribe a <span>{e(nombre)}</span></h1>
    <p class="lead">El mismo mensaje, dos veces: primero sin nadie al otro lado y después con un agente de IA contestando. Dura medio minuto.</p>
    <div class="cta desk">
      {cta}
    </div>
  </div>
  <div class="player" id="player">
    <video id="vid" playsinline preload="metadata" poster="{med}.jpg" src="{med}.mp4"></video>
    <button class="play" id="play" type="button" aria-label="Reproducir el vídeo con sonido"><i></i><span>Ver el vídeo · {seg} s</span></button>
  </div>
  <div class="cta mob">
    {cta}
  </div>
</main>
<footer><span>Fabrizzio Zelada · Zenia Partners · Madrid</span><span>La conversación del vídeo es de ejemplo. <a href="https://zeniapartners.com{n['enlace']}">zeniapartners.com</a></span></footer>
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
