# Rediseño «noir» de la portada (1-nov-2026)

Tres variantes de la portada española para que Fabrizzio elija: negro y champán (A), navy y champán (B),
navy y azul de marca (C). Parten de `es/index.html` de esta rama (`rediseno-v10`) y de `styles/main.css` v11.

Regenerar las tres (desde la raíz del repo):

    python3 scripts/rediseno-noir/build_noir.py .

Escribe `es/index-a.html`, `es/index-b.html`, `es/index-c.html`, `styles/noir.css` (main.css + `noir-overrides.css`),
`styles/noir-b.css` y `styles/noir-c.css`. Para verlas: `python3 -m http.server 8766` en la raíz y abrir
`http://127.0.0.1:8766/es/index-a.html` (b, c). Capturas: `python3 scripts/rediseno-noir/shot2.py <url> salida.png 1440 12`
(o 390 para el móvil; el 12 son los segundos de espera para que termine la conversación del agente).

Los símbolos de la banda «Trabajamos sobre» son de simple-icons (CC0). `js/demo-chat.js` v2 rellena el avatar del chat.
Pendiente: la portada inglesa (`index.html`) se hace igual cuando Fabrizzio elija variante.
