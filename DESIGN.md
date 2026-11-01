# DESIGN.md: zeniapartners.com

Sistema de diseño de la web de Zenia Partners desde el 31 de octubre de 2026 (hoja de estilos
`styles/main.css` v10). Cualquier agente o persona que toque la web lee esto antes de escribir
HTML o CSS. Lo que no aparece aquí se decide con las reglas de la casa de Taste Skill (sin
degradados, sin sombras en reposo, sin cristal, sin etiquetas pequeñas en mayúsculas, sin
numeración decorativa, sin tarjetas con icono, titulares de dos líneas como máximo).

## 1. Carácter

Papel y tinta. Una firma de consultoría que construye agentes de IA: sobria, editorial, segura.
La jerarquía la hacen la escala tipográfica, el espacio y tres campos de color planos (un tono
de papel, la tinta y el azul). Nada brilla, nada flota, nada se degrada. El mismo lenguaje que
los documentos formales de Zenia (membrete en Space Grotesk, títulos en serif, filetes finos en
tinta solo en tablas y formularios).

## 2. Color

| Papel | Token | Hex | Uso |
|---|---|---|---|
| Papel | `--paper` | `#F4F4F1` | fondo de toda la página |
| Papel 2 | `--paper-2` | `#E8E8E3` | un tono más: filas alternas, bloque destacado, campo de la cita, menú móvil |
| Papel 3 | `--paper-3` | `#DBDBD4` | estado hover de superficies en papel 2 |
| Tinta | `--ink` | `#0F172A` | texto corrido, títulos, el campo invertido (enfoque, pie) |
| Tinta suave | `--ink-soft` | `#3F4A5F` | texto secundario dentro de tablas y notas |
| Tinta apagada | `--ink-mute` | `#5B6475` | notas, horas, pies de foto (nunca por debajo de 13 px) |
| Azul | `--accent` | `#2563EB` | el único acento: botón principal, enlaces de caso, el campo del cierre |
| Azul profundo | `--accent-deep` | `#1D4ED8` | hover del botón principal y enlaces de texto (`--accent-text`, contraste sobre papel 2) |
| Azul pálido | `--accent-pale` | `#D6E2FF` | burbujas del agente en la conversación, un tramo de la barra de etapas |
| Azul sobre tinta | `--accent-on-ink` | `#8DB3FF` | enlaces grandes sobre el campo de tinta (el correo del pie) |

Reglas: un solo azul por pantalla; el texto corrido siempre en tinta plena; las superficies se
separan por un paso de tono, nunca por una línea ni una sombra; una sección puede cambiar el
campo entero (tinta o azul), nada se funde con nada. Prohibidos el violeta, el índigo y
cualquier degradado.

## 3. Tipografía

- Títulos y cifras: **Source Serif 4** (Google Fonts, ejes `opsz` y `wght`), peso 500,
  interlineado 0,98 a 1,05, tracking de −0,015 a −0,025 em. Nunca una palabra en otro color o
  en cursiva dentro de un titular.
- Texto, menú y botones: pila del sistema, `-apple-system, "Helvetica Neue", Helvetica,
  "Segoe UI", Roboto, Arial` (en la Mac y el iPhone es Helvetica Neue, como en los documentos).
- Logotipo: **Space Grotesk** 700 solo para la palabra ZENIA (menú y pie).
- Escala (cinco pasos más una pequeña): portada `clamp(2.75rem, 7.4vw, 7rem)`, título
  `clamp(2rem, 4.4vw, 3.75rem)`, declaración `clamp(1.5rem, 2.3vw, 2.125rem)`, entrada
  `clamp(1.1875rem, 1.5vw, 1.4375rem)`, texto 17 px, pequeña 15 px. En el teléfono: portada
  32 px, títulos 24 a 28 px.
- Titulares de dos líneas como máximo en escritorio; medida del texto corrido de 40 a 62 ch.
- Detalle: comillas tipográficas, `text-wrap: balance` en títulos, cifras alineadas
  (`tabular-nums`) y espacios duros entre cifra y unidad (`8&nbsp;semanas`).

## 4. Espacio y retícula

- Un contenedor de 1320 px con márgenes iguales de `clamp(20px, 3.2vw, 48px)`.
- Retícula de 12 columnas (`repeat(12, minmax(0, 1fr))`, hueco 24 px) dentro de cada sección.
- Entre secciones, `clamp(96px, 12vw, 176px)`; dentro de una sección nunca más que eso.
- Cada sección tiene una composición distinta de la vecina: portada solo tipográfica,
  conversación a la derecha, lista grande, texto más campo de tinta, dos columnas, barra de
  etapas, frase con cifras, tabla, campo de tono con la cita, preguntas sangradas, índice,
  cifra enorme, tres afirmaciones, campo azul, nombre a todo el ancho.
- Los campos a sangre (azul del cierre, tinta del pie) usan `width: 100vw` y
  `margin-left: calc(50% - 50vw)`, con el contenido alineado al contenedor.

## 5. Componentes

- **Botón**: rectángulo sin radio, 56 px de alto (44 en el menú), un relleno plano. Principal
  azul con texto blanco; secundario en papel 2 con texto tinta; sobre el campo azul, papel con
  tinta. Hover: un paso más de tono; activo: `scale(0.985)`; foco: contorno azul de 2 px.
- **Menú**: barra llana sobre el papel, sin fondo ni filete, logotipo a la izquierda, cinco
  enlaces, una acción. En el teléfono, hamburguesa y hoja de enlaces en papel 2.
- **Conversación de ejemplo** (`.chat`, raíz `data-ui`): cabecera en tinta, burbujas del
  cliente en blanco y del agente en azul pálido, horas en 13 px, línea de sistema al pie.
  Las burbujas aparecen una a una (`js/demo-chat.js`); con movimiento reducido, todas a la vez.
- **Barra de etapas** (`.stage-bar`, `data-ui`): cuatro tramos planos (tinta, azul, azul
  pálido, papel 2) cuyo ancho sigue la duración real de cada fase.
- **Tabla de casos**: `<table>` sin bordes, filas impares en papel 2, cifras en serif.
- **Preguntas**: `<details>` con chevrón de dos trazos; abierta, un tono de papel 2 que sobresale
  24 px a cada lado.
- **Formularios y tablas** son los únicos sitios donde puede haber una línea de 1 px.
- **Pie**: campo de tinta, la palabra ZENIA a todo el ancho (SVG con `textLength`), contacto
  en serif azul sobre tinta, columnas de enlaces a 15 px, línea legal a 13 px.

## 6. Movimiento

- Todo dentro de `@media (prefers-reduced-motion: no-preference)`; la página reducida es la
  página terminada y sin script nada queda oculto (la clase `js` en `<html>` activa las
  entradas).
- Entradas por partes: `.reveal` sube 18 px y aparece en 0,6 s, con retardos de 80 ms
  (`.reveal-delay-1` a `-5`).
- Respuesta en cada control: color en hover, `scale` en activo, contorno en foco.
- La firma: la palabra ZENIA del pie crece del 94 % al 100 % al entrar en pantalla
  (`animation-timeline: view()`, con fallback estático).
- Solo `transform` y `opacity`; nunca `transition: all`.

## 7. Prohibido

Degradados (también en texto), sombras en reposo, `backdrop-filter`, bordes de 1 px fuera de
tablas y formularios, etiquetas pequeñas en mayúsculas espaciadas, numeración 01/02/03,
tarjetas con icono, filas de tarjetas iguales, emojis, pastillas, violeta e índigo, Inter como
tipografía, guiones largos en el texto, la palabra «chatbot».

## 8. Cómo comprobar un cambio

```bash
node ~/.claude/skills/design-taste-frontend/scripts/lint.mjs index.html es/index.html styles/main.css
node ~/.claude/skills/design-taste-frontend/scripts/inspect.mjs https://zeniapartners.com/es/ --out .taste-skill/after
```

Mirar las capturas a 1440, 768 y 390 px antes de dar nada por bueno. Al cambiar `main.css`,
subir `?v=N` en los `<link>` de las dos portadas (GitHub Pages cachea unos diez minutos).
