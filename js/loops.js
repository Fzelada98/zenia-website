// ZENIA, los vídeos en bucle de la portada (clase «loop»): se reproducen sin sonido solo mientras
// están en pantalla, se paran al salir y, con movimiento reducido, no arrancan solos y muestran
// los controles. El póster se ve siempre; sin script, el vídeo queda quieto con su póster.
(function () {
  var vids = Array.prototype.slice.call(document.querySelectorAll('video.loop'));
  if (!vids.length) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) {
    vids.forEach(function (v) { v.removeAttribute('autoplay'); v.controls = true; });
    return;
  }
  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () { v.controls = true; }); }
  if (!('IntersectionObserver' in window)) { vids.forEach(play); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var v = e.target;
      if (e.isIntersecting) { if (v.paused) play(v); }
      else if (!v.paused) {
        v.pause();
        // si apenas empezó (el primer fotograma suele ser negro), vuelve al póster
        if (v.currentTime < 0.6) { try { v.load(); } catch (err) {} }
      }
    });
  }, { threshold: 0.25 });
  vids.forEach(function (v) { v.muted = true; io.observe(v); });
  document.addEventListener('visibilitychange', function () {
    vids.forEach(function (v) { if (document.hidden) v.pause(); });
  });
})();
