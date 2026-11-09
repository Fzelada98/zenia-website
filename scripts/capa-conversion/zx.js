/* ZENIA, capa de conversión de landings y blog (nov-2026). Se publica en /assets/zx.js.
 *
 * 1. Origen de cada lead: al pulsar un enlace de WhatsApp o Calendly se apunta qué botón
 *    fue (data-zx-src o, si no lo lleva, dónde está: menú, portada, final, burbuja…) y se
 *    añade como «src» a los registros que mandan a gaia el beacon de la página y qualify.js.
 *    No se manda nada nuevo: solo se completa lo que ya se enviaba.
 * 2. Barra fija: en el móvil, una barra abajo; en el ordenador, una tarjeta en la esquina.
 *    Aparece al pasar la portada (landings) o al leer un trozo del artículo (blog), se aparta
 *    cuando ya hay un botón de WhatsApp a la vista o se llega al pie, y se puede cerrar
 *    (no vuelve en esa visita). Abre el mismo WhatsApp de la página, pasando por el
 *    formulario de qualify.js como cualquier otro botón.
 * 3. Tablas del blog: se deslizan dentro de su caja; si no caben, se avisa encima.
 * Sin script la página funciona igual: los bloques nuevos vienen ya en el HTML.
 */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  function meta(n) { var m = doc.querySelector('meta[name="' + n + '"]'); return m ? m.getAttribute('content') || '' : ''; }
  var PAGE = meta('zx-page');               // landing | blog | base
  var NEG = meta('zx-negocio');             // «tu clínica», «your practice»…
  var WA = meta('zx-wa');
  var EN = (root.getAttribute('lang') || '').toLowerCase().indexOf('en') === 0;

  /* ---------- 1. origen del lead ---------- */
  var SRC = '';
  function origen(a) {
    var s = a.getAttribute('data-zx-src');
    if (s) return s;
    if (a.closest('.zx-dock')) return 'dock';
    if (a.hasAttribute('data-directo') || /WhatsApp$/.test(a.getAttribute('aria-label') || '')) return 'float';
    if (a.closest('nav, .nav, .blog-nav')) return 'nav';
    if (a.closest('.hero, .blog-header')) return 'hero';
    if (a.closest('.blog-cta')) return 'blog-end';
    if (a.closest('footer, .footer, .blog-footer')) return 'footer';
    return 'body';
  }
  window.addEventListener('click', function (e) {
    var t = e.target;
    var a = t && t.closest ? t.closest('a[href*="wa.me"], a[href*="calendly.com"]') : null;
    if (a) SRC = origen(a).slice(0, 20);
  }, true);
  if (navigator.sendBeacon) {
    var enviar = navigator.sendBeacon.bind(navigator);
    navigator.sendBeacon = function (url, data) {
      try {
        if (SRC && typeof data === 'string' && String(url).indexOf('/gwb/lead') > -1 && data.indexOf('"zenia"') > -1) {
          var o = JSON.parse(data);
          if (o && o.site === 'zenia' && !o.src) { o.src = SRC; data = JSON.stringify(o); }
        }
      } catch (err) { /* nunca estorbar el registro */ }
      return enviar(url, data);
    };
  }

  /* ---------- 3. tablas ---------- */
  function tablas() {
    var ts = doc.querySelectorAll('.blog-content table, article table');
    for (var i = 0; i < ts.length; i++) {
      var t = ts[i];
      if (t.parentNode && t.parentNode.classList && t.parentNode.classList.contains('zx-table-in')) continue;
      var w = doc.createElement('div'); w.className = 'zx-table';
      var h = doc.createElement('p'); h.className = 'zx-table-hint';
      h.textContent = EN ? 'Swipe to see the full table →' : 'Desliza para ver la tabla completa →';
      var inn = doc.createElement('div'); inn.className = 'zx-table-in';
      t.parentNode.insertBefore(w, t); w.appendChild(h); w.appendChild(inn); inn.appendChild(t);
    }
    var cajas = doc.querySelectorAll('.zx-table');
    for (var j = 0; j < cajas.length; j++) {
      var c = cajas[j].querySelector('.zx-table-in');
      if (c) cajas[j].classList.toggle('zx-scroll', c.scrollWidth > c.clientWidth + 2);
    }
  }
  if (PAGE === 'blog') { tablas(); window.addEventListener('resize', tablas); }

  /* ---------- 2. barra fija ---------- */
  if (!WA) return;
  var OFF = 'zx-dock-off';
  try { if (sessionStorage.getItem(OFF)) return; } catch (e) { /* sin almacenamiento: se muestra */ }

  var T = EN ? {
    s1: 'Want this in ' + (NEG || 'your business') + '?',
    s2: 'We reply within 24 hours',
    l1: 'Want this in ' + (NEG || 'your business') + '?',
    l2: 'We build the CRM and the AI agent that answer, book and follow up on WhatsApp. We reply within 24 hours.',
    btn: '<span class="zx-l">Message us on </span>WhatsApp', x: 'Close'
  } : (PAGE === 'blog' ? {
    s1: '¿Lo aplicamos en ' + (NEG || 'tu negocio') + '?',
    s2: 'Respuesta en menos de 24 h',
    l1: '¿Quieres esto en ' + (NEG || 'tu negocio') + '?',
    l2: 'Montamos el CRM y el agente de IA que atienden, agendan y venden por WhatsApp. Te respondemos en menos de 24 h.',
    btn: '<span class="zx-l">Escríbenos por </span>WhatsApp', x: 'Cerrar'
  } : {
    s1: '¿Lo vemos para ' + (NEG || 'tu negocio') + '?',
    s2: 'Respuesta en menos de 24 h',
    l1: '¿Cómo sería en ' + (NEG || 'tu negocio') + '?',
    l2: 'Cuéntanos cómo trabajas hoy y te enseñamos por WhatsApp cómo respondería tu agente de IA.',
    btn: '<span class="zx-l">Escríbenos por </span>WhatsApp', x: 'Cerrar'
  });
  var ICO = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.83 9.83 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88M20.46 3.49A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.48-8.42"/></svg>';

  var dock = doc.createElement('div');
  dock.className = 'zx-dock';
  dock.setAttribute('role', 'complementary');
  dock.setAttribute('aria-label', EN ? 'Contact Zenia' : 'Contactar con Zenia');
  dock.innerHTML =
    '<div class="zx-dock-txt"><strong class="zx-dock-short">' + T.s1 + '</strong><span class="zx-dock-short">' + T.s2 +
    '</span><strong class="zx-dock-long">' + T.l1 + '</strong><span class="zx-dock-long">' + T.l2 + '</span></div>' +
    '<a class="zx-btn" data-zx-src="dock" target="_blank" rel="noopener">' + ICO + '<span>' + T.btn + '</span></a>' +
    '<button type="button" class="zx-dock-x" aria-label="' + T.x + '">&times;</button>';
  dock.querySelector('a').setAttribute('href', WA);
  doc.body.appendChild(dock);
  root.classList.add('zx-has-dock');

  var cerrado = false, on = false, pend = false;
  dock.querySelector('.zx-dock-x').addEventListener('click', function () {
    cerrado = true; mostrar(false); root.classList.remove('zx-has-dock');
    try { sessionStorage.setItem(OFF, '1'); } catch (e) { /* nada */ }
  });

  function mostrar(v) {
    if (v === on) return;
    on = v;
    dock.classList.toggle('on', v);
    root.classList.toggle('zx-dock-on', v);
    // sin foco ni lector de pantalla mientras está escondida
    if (v) dock.removeAttribute('aria-hidden'); else dock.setAttribute('aria-hidden', 'true');
    var f = dock.querySelectorAll('a, button');
    for (var i = 0; i < f.length; i++) { if (v) f[i].removeAttribute('tabindex'); else f[i].setAttribute('tabindex', '-1'); }
  }
  dock.setAttribute('aria-hidden', 'true');

  var hero = doc.querySelector('.hero');
  var pie = doc.querySelector('footer, .footer, .blog-footer');
  var botones = [];
  function recoger() {
    botones = [];
    var cand = doc.querySelectorAll('a[href*="wa.me"], a[href*="calendly.com"]');
    for (var i = 0; i < cand.length; i++) {
      var a = cand[i];
      if (a.closest('.zx-dock, nav, .nav, .blog-nav')) continue;
      if (a.hasAttribute('data-directo') || /WhatsApp$/.test(a.getAttribute('aria-label') || '')) continue;
      if (a.closest('footer, .footer, .blog-footer')) continue;
      if (!/\b(btn|zx-btn)\b/.test(a.className) && !a.closest('.blog-cta')) continue;
      botones.push(a);
    }
  }
  recoger();

  // En el ordenador la tarjeta solo cabe en el margen libre a la derecha del artículo; si no hay
  // sitio, no sale (el botón de WhatsApp del menú fijo ya está siempre a la vista).
  var columna = doc.querySelector('.blog-content') || doc.querySelector('article');
  function cabe() {
    var w = window.innerWidth || root.clientWidth;
    if (w <= 768) return true;
    if (PAGE !== 'blog' || !columna) return false;
    return w - columna.getBoundingClientRect().right >= 380;
  }

  function calcular() {
    pend = false;
    if (cerrado || !cabe()) return mostrar(false);
    if (doc.querySelector('.zq-fondo')) return mostrar(false);   // formulario de qualify.js abierto
    var cookies = doc.getElementById('cookieBanner');              // aviso de cookies abajo: no se pisan
    if (cookies && getComputedStyle(cookies).display !== 'none') return mostrar(false);
    var vh = window.innerHeight || root.clientHeight;
    var y = window.pageYOffset || root.scrollTop;
    var pasado;
    if (PAGE === 'blog') {
      var alto = Math.max(1, (root.scrollHeight || 0) - vh);
      pasado = y > Math.max(640, alto * 0.14);
    } else if (hero) {
      pasado = hero.getBoundingClientRect().bottom < 40;
    } else {
      pasado = y > vh * 0.9;
    }
    if (!pasado) return mostrar(false);
    if (pie && pie.getBoundingClientRect().top < vh - 40) return mostrar(false);
    for (var i = 0; i < botones.length; i++) {
      var r = botones[i].getBoundingClientRect();
      if (r.width && r.bottom > 56 && r.top < vh - 72) return mostrar(false);
    }
    mostrar(true);
  }
  function pedir() { if (!pend) { pend = true; (window.requestAnimationFrame || setTimeout)(calcular); } }
  window.addEventListener('scroll', pedir, { passive: true });
  window.addEventListener('resize', pedir);
  // el formulario de cualificación se abre y se cierra sin hacer scroll
  doc.addEventListener('click', function () { setTimeout(pedir, 50); setTimeout(pedir, 400); });
  pedir();
})();
