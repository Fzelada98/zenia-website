# Zenia v2 · rebrand «producto» (14-nov-2026)

Pedido de Fabrizzio: «hagamos un rebrand como esta marca: ventia-latam.com» y «ataquemos nichos».
De Ventia se toma el ENFOQUE (producto a la vista, promesa de resultado, nichos, precio a medida,
demo como llamada a la acción), nunca su logo, textos ni clientes.

- `build.py <raíz> [--preview]`: genera la portada ES y las páginas /es/clinicas/, /es/talleres/,
  /es/autoescuelas/. Con --preview escribe en <raíz>/v2/ con noindex (NO commitear v2/).
- `z2.css`, `z2.js`: se copian a /assets/z2/ con ?v=<epoch>.
- `iconos-integraciones.json`: símbolos de la banda «Trabajamos sobre» de la portada anterior.
- Contenido: solo cifras de casos reales (GWB 831/33/10 de 12; Throwin' Salt 54/23/2 M$).
  Teléfono y panel = negocio de EJEMPLO, rotulado. Sin «10x», «-40 %», etc. de la portada anterior.
- Formulario «tu demo en 48 h»: beacon a gaia {site:zenia, kind:qualify, src:demo-form,
  model:"Ver mi demo", city:<web>} → aviso de lead por correo (notifier).
- **EN VIVO desde el 14-nov-2026** (commits 04e76b4 y 7e775c7): portada ES + 3 nichos, imágenes para
  compartir `assets/images/og-z2-*.jpg`, sitemap con los 3 nichos, GA4 sin cookies + Cloudflare.
  Inglés pendiente. El guard (`~/.zenia-seo-guard/inject_ctas.py`) ya no depende del botón flotante
  de esta portada (usa `~/.zenia-seo-guard/float_canon.html`).
