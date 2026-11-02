# Rediseño «noir» de la portada (1-nov-2026)

Tres variantes de la portada española para que Fabrizzio elija: negro y champán (A), navy y champán (B),
navy y azul de marca (C). Parten de `es/index.html` de esta rama (`rediseno-v10`) y de `styles/main.css` v11.

Regenerar las tres (desde la raíz del repo):

    python3 scripts/rediseno-noir/build_noir.py .

Escribe `es/index-a.html`, `es/index-b.html`, `es/index-c.html`, `styles/noir.css` (main.css + `noir-overrides.css`),
`styles/noir-b.css` y `styles/noir-c.css`. Para verlas: `python3 -m http.server 8766` en la raíz y abrir
`http://127.0.0.1:8766/es/index-a.html` (b, c). Capturas: `python3 scripts/rediseno-noir/shot3.py <url> salida.png 1440 18`
(o 390 para el móvil; el 12 son los segundos de espera para que termine la conversación del agente).

Los símbolos de la banda «Trabajamos sobre» son de simple-icons (CC0). `js/demo-chat.js` v4 reproduce el WhatsApp del agente dentro del teléfono (hora del visitante, «escribiendo…», ticks azules, botones de respuesta rápida) y, debajo, la pantalla del CRM a medida de cada negocio (`.crm-window`), donde la fila de la conversación aparece al terminar; la sección 04 es una línea de tiempo con regla de semanas (`.gantt`). Fabrizzio eligió la variante C (2-nov-2026).
Pendiente: la portada inglesa (`index.html`) se hace igual cuando Fabrizzio elija variante.

2-nov-2026: la portada lleva la frase centrada sobre la foto de Madrid de noche (`assets/images/hero-madrid.webp`, Tim Adams, CC BY 2.0, crédito en el pie; fuente y licencia en `assets/images/hero-src/credits.json`), el teléfono y el CRM a medida como captura de producto, la cita del fundador centrada y el cierre con la misma foto. La hoja cambia de versión (`?v=<epoch>`) en cada construcción para que el navegador no reutilice la vieja.

2-nov-2026 (noche): la portada lleva además una red de nodos animada en canvas (`js/hero-net.js`, color de `--net-rgb`, se para fuera de pantalla y con movimiento reducido pinta un fotograma) y una veladura radial más fuerte detrás del texto; la sección 04 es un cuadro de una pieza (`.gantt-chart`, filas con `display: contents`, rejilla continua, hito «Primer resultado» con rombo); el pie cambia el nombre gigante por una cabecera (símbolo, ZENIA, lema y botón).
