# DESIGN.md: zeniapartners.com

Sistema de diseño de las DOS portadas de Zenia Partners (`index.html` en inglés y `es/index.html`
en español) desde el 3 de noviembre de 2026. Las portadas cargan `styles/home.css`; las ~560
landings por sector y ciudad siguen con `styles/main.css` y no se tocan desde aquí.

Cualquier agente o persona que toque las portadas lee esto antes de escribir HTML o CSS.

## 1. Carácter

Navy y azul de marca, con la calidad de un banco privado: serif editorial (Cormorant Garamond),
etiquetas en versalitas espaciadas, paneles de cristal con filete fino, atmósfera (una fotografía
de Madrid de noche velada y una red de nodos animada en la portada). Lo que vende es el producto
a la vista: un WhatsApp real dentro de un teléfono y el CRM a medida, navegable, debajo. Las
cifras son reales y los vídeos son de clientes reales.

Lo que Fabrizzio rechazó y no vuelve: fondo claro «papel y tinta», páginas escasas sin imágenes,
titulares a 7vw, vídeos verticales sueltos.

## 2. Color (variante C)

| Papel | Token | Valor | Uso |
|---|---|---|---|
| Navy | `--paper` | `#0B1220` | fondo de la página |
| Navy 2 | `--paper-2` | `#111A2C` | bandas de tono (enfoque, índice), menú abierto, aviso de cookies |
| Navy 3 | `--paper-3` | `#1A2540` | superficies elevadas |
| Texto | `--ink` | `#EEF1F7` | texto corrido y títulos |
| Texto suave | `--ink-soft` | `#C3CAD8` | texto secundario |
| Texto apagado | `--ink-mute` | `#8B95A7` | notas y pies de foto (nunca por debajo de 12 px) |
| Azul claro | `--accent` | `#5B8CFF` | etiquetas, cifras, cursivas del titular, filetes |
| Azul de marca | `--accent-deep` | `#2563EB` | botón principal, la fila nueva del CRM |
| Filete | `--line` / `--line-strong` | azul al 20 % / 45 % | bordes de paneles y tabla |

El WhatsApp del teléfono usa los colores oficiales del tema oscuro de WhatsApp (`#0B141A`,
`#202C33`, `#005C4B`, ticks `#53BDEB`) y no se toca. La ventana del CRM usa `#0E1626` con los
estados verde / ámbar / azul / naranja.

## 3. Tipografía

- Títulos y cifras: **Cormorant Garamond** 500/600, con la segunda parte del titular en cursiva
  azul (`.text-gradient`). Numerales modernos siempre (`font-variant-numeric: lining-nums`).
- Texto, menú, botones y etiquetas: pila del sistema (Helvetica Neue / Segoe UI / Roboto).
- Logotipo: **Space Grotesk** 700 solo para la palabra ZENIA.
- Etiquetas en versalitas: 12 px, tracking 0,18 em, nunca más pequeñas.
- Texto corrido 16 px o más. Titulares a dos líneas en escritorio (en inglés el H1 y los títulos
  tienen más medida: `html[lang="en"]`).

## 4. Composición

1. Menú fijo con fondo velado.
2. Portada: frase centrada sobre la foto de Madrid velada (`.hero-photo`) y la red de nodos
   (`.hero-net`, `js/hero-net.js`); debajo la escena (`.scene`): el CRM a medida a la izquierda
   y el teléfono con WhatsApp a la derecha (en móvil, teléfono y luego CRM).
3. Banda «Trabajamos sobre» con los símbolos reales (simple-icons, CC0).
4. Secciones numeradas «— 01» con filete superior: oportunidades (lista), enfoque (banda de
   tono), servicios (tarjetas de cristal y la destacada con el vídeo de GWB Network), proceso
   (línea de tiempo `.gantt` con regla de semanas), impacto (cifras), casos (dos casos destacados
   con vídeo, fotos y tabla), cita centrada, preguntas, índice, precios (con puntos), cierre con la
   misma foto, pie compacto (símbolo, ZENIA, lema, botón).

## 5. Piezas vivas

- **Conversación y CRM** (`js/demo-chat.js`): tres negocios (restaurante, clínica, gimnasio), la
  hora del visitante, «escribiendo…», ticks azules, botones de respuesta rápida; al terminar, la
  fila entra en el CRM y las cifras suben. El CRM tiene cinco vistas por negocio con sus datos
  (`DATA.<idioma>.<negocio>.views`), interruptores en Ajustes y flechas del teclado. En el
  teléfono, las columnas `optm` se ocultan por vista para que nunca haya desplazamiento lateral.
- **Vídeos** (`js/loops.js`): en reposo bucle mudo recortado a 4:3 (`.stage-box`); con «Ver con
  sonido» (o al pulsar) arrancan desde el principio con sonido, enteros y con los controles del
  navegador; al terminar vuelven al reposo. Los MP4 viven en `cases/video/` (recomprimidos a
  720p con `scripts/rediseno-noir/transcode.swift`); los pósteres en `cases/img/`.
- **Idioma**: la portada inglesa manda a `/es/` a quien navega en español (sin preferencia
  guardada, con `?lang=es` o con preferencia `es`); `?lang=en` fuerza el inglés.

## 6. Cómo reconstruir y comprobar

Las dos portadas se generan desde las de la rama `rediseno-v10` (estructura base) con
`scripts/rediseno-noir/build_launch.py <fuente> <salida>`; los textos por idioma están en el
diccionario `L` del script, los estilos en `noir-overrides.css` y los tokens en `C_CSS`. Cada
construcción cambia el `?v=` de la hoja y de los scripts. `LEEME.md` en esa carpeta cuenta el
historial. Antes de dar nada por bueno: Playwright a 1440, 390 y 360 px (sin desbordes, sin
toques menores de 32 px, sin errores de script, el CRM sin desplazamiento lateral en las cinco
vistas de los tres negocios, los tres vídeos con sonido) y el inspector de Taste Skill
(`~/.claude/skills/design-taste-frontend/scripts/inspect.mjs`), sabiendo que marcará a propósito
las etiquetas en versalitas, los filetes, el cristal y las sombras, que aquí son decisión.

## 7. Prohibido

Fondos claros en las portadas, violeta e índigo, Inter, emojis, tarjetas con icono, titulares a
más de dos líneas en escritorio, vídeos verticales sin marco, cifras inventadas, la palabra
«chatbot», guiones largos en el texto.
