// ZENIA · página de vídeo por prospecto. Reproduce con sonido al tocar y avisa (una vez por visita) cuando
// empiezan a verlo y cuando lo ven casi entero. No cuenta las pruebas propias (?qa, localhost, navegador automatizado).
(function () {
  var D = {}; try { D = JSON.parse(document.getElementById('v-data').textContent); } catch (e) {}
  var v = document.getElementById('vid'), b = document.getElementById('play');
  var qa = /[?&]qa\b/.test(location.search) || location.hostname === 'localhost' || location.hostname === '127.0.0.1' || navigator.webdriver;
  var URL_ = 'https://zenia-leads.onrender.com/lead', hecho = {};
  function aviso(kind) {
    if (qa || hecho[kind] || !navigator.sendBeacon) return; hecho[kind] = 1;
    try { navigator.sendBeacon(URL_, JSON.stringify({ site: 'zenia-demo', kind: kind, brand: D.nombre, path: location.pathname, ref: document.referrer || '' })); } catch (e) {}
  }
  function empezar() {
    b.hidden = true; v.controls = true; v.muted = false;
    var p = v.play(); if (p && p.catch) p.catch(function () { b.hidden = false; v.controls = false; });
  }
  b.addEventListener('click', empezar);
  v.addEventListener('playing', function () { b.hidden = true; aviso('video'); });
  v.addEventListener('timeupdate', function () { if (v.duration && v.currentTime / v.duration > 0.85) aviso('video-fin'); });
  v.addEventListener('ended', function () { v.controls = false; b.hidden = false; b.querySelector('span').textContent = 'Volver a verlo'; });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="wa.me"],a[href*="calendly.com"],a[href^="mailto:"]');
    if (!a || qa || !navigator.sendBeacon) return;
    navigator.sendBeacon(URL_, JSON.stringify({ site: 'zenia', src: 'video', brand: D.nombre, path: location.pathname, ref: document.referrer || '' }));
  }, true);
})();
