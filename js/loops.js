// ZENIA, los vídeos de la portada (cada uno dentro de un «.stage-box»).
// Reposo: se reproducen en bucle, sin sonido, solo mientras están en pantalla, recortados a 4:3.
// Con el botón «Ver con sonido» (o pulsando el vídeo): empieza desde el principio con sonido,
// entero (sin recorte) y con los controles del navegador: retroceder, adelantar, volumen,
// pantalla completa. Al terminar vuelve al reposo. Con movimiento reducido no arranca solo y
// muestra los controles desde el principio. Sin script, el vídeo queda quieto con su póster.
(function () {
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.stage-box'));
  if (!boxes.length) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // si el navegador no deja arrancar el bucle, se queda el póster con el botón «Ver con sonido»
  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }

  boxes.forEach(function (box) {
    var v = box.querySelector('video');
    var btn = box.querySelector('.stage-sound');
    if (!v) return;
    v.muted = true; v.defaultMuted = true; v.loop = true;
    v.setAttribute('muted', ''); v.setAttribute('playsinline', ''); v.playsInline = true;
    // el vídeo solo se pinta cuando de verdad está reproduciendo: hasta entonces se ve el póster
    // (Safari en el iPhone pinta el primer fotograma, que es negro, aunque no haya arrancado)
    v.addEventListener('playing', function () { box.classList.add('is-playing'); });
    v.addEventListener('pause', function () { if (!v.dataset.user) box.classList.remove('is-playing'); });
    v.addEventListener('emptied', function () { box.classList.remove('is-playing'); });
    v.controls = reduce; // en reposo sin controles; con movimiento reducido, con ellos
    if (reduce) { v.removeAttribute('autoplay'); }

    function live() {
      if (box.classList.contains('is-live')) return;
      box.classList.add('is-live');
      v.dataset.user = '1';
      v.loop = false; v.muted = false; v.volume = 1; v.controls = true;
      try { v.currentTime = 0; } catch (e) {}
      play(v);
    }
    function rest() {
      box.classList.remove('is-live');
      delete v.dataset.user;
      v.muted = true; v.loop = true; v.controls = reduce;
      try { v.currentTime = 0; } catch (e) {}
      if (!reduce) play(v);
    }
    if (btn) btn.addEventListener('click', function (e) { e.preventDefault(); live(); });
    v.addEventListener('click', function () { if (!v.dataset.user) live(); });
    v.addEventListener('ended', function () { if (v.dataset.user) rest(); });
    // si el visitante quita el silencio desde los controles, también cuenta como «con sonido»
    v.addEventListener('volumechange', function () { if (!v.muted && !v.dataset.user) live(); });
  });

  if (reduce || !('IntersectionObserver' in window)) { return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var v = e.target;
      if (v.dataset.user) { if (!e.isIntersecting && !v.paused) v.pause(); return; } // con sonido: se para al salir y no vuelve solo
      if (e.isIntersecting) { if (v.paused) play(v); }
      else if (!v.paused) {
        v.pause();
        // si apenas empezó (el primer fotograma suele ser negro), vuelve al póster
        if (v.currentTime < 0.6) { try { v.load(); } catch (err) {} }
      }
    });
  }, { threshold: 0.25 });
  boxes.forEach(function (box) { var v = box.querySelector('video'); if (v) io.observe(v); });
  document.addEventListener('visibilitychange', function () {
    boxes.forEach(function (box) { var v = box.querySelector('video'); if (v && document.hidden) v.pause(); });
  });
})();
