// ZENIA, la red de la portada: nodos que derivan despacio y se unen cuando están cerca,
// dibujados en un canvas detrás del texto. Toma el color del acento de la hoja de estilos,
// se detiene cuando la portada sale de pantalla y, con movimiento reducido, pinta un solo
// fotograma quieto. Sin script no hay red: la fotografía velada queda igual.
(function () {
  var host = document.querySelector('.hero-net');
  if (!host || !window.requestAnimationFrame) return;
  var canvas = document.createElement('canvas');
  canvas.setAttribute('aria-hidden', 'true');
  host.appendChild(canvas);
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var accent = (getComputedStyle(document.documentElement).getPropertyValue('--net-rgb') || '91, 140, 255').trim();
  var W = 0, H = 0, dpr = 1, nodes = [], running = false, raf = 0, last = 0;
  var LINK = 150, SPEED = 0.028;

  function size() {
    var r = host.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(1, Math.round(r.width)); H = Math.max(1, Math.round(r.height));
    canvas.width = W * dpr; canvas.height = H * dpr;
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var want = Math.round(Math.min(110, Math.max(36, (W * H) / 14000)));
    while (nodes.length < want) nodes.push(make(true));
    nodes.length = want;
  }
  function make(anywhere) {
    var a = Math.random() * Math.PI * 2;
    return { x: Math.random() * W, y: anywhere ? Math.random() * H : H + 10, vx: Math.cos(a) * SPEED, vy: Math.sin(a) * SPEED,
             r: 1 + Math.random() * 1.6, big: Math.random() < 0.12 };
  }
  function step(dt) {
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      n.x += n.vx * dt; n.y += n.vy * dt;
      if (n.x < -20) n.x = W + 20; else if (n.x > W + 20) n.x = -20;
      if (n.y < -20) n.y = H + 20; else if (n.y > H + 20) n.y = -20;
    }
  }
  function draw() {
    ctx.clearRect(0, 0, W, H);
    // enlaces
    ctx.lineWidth = 1;
    for (var i = 0; i < nodes.length; i++) {
      var a = nodes[i];
      for (var j = i + 1; j < nodes.length; j++) {
        var b = nodes[j];
        var dx = a.x - b.x, dy = a.y - b.y;
        var d2 = dx * dx + dy * dy;
        if (d2 > LINK * LINK) continue;
        var t = 1 - Math.sqrt(d2) / LINK;
        ctx.strokeStyle = 'rgba(' + accent + ',' + (0.28 * t * t).toFixed(3) + ')';
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
    }
    // nodos
    for (var k = 0; k < nodes.length; k++) {
      var n = nodes[k];
      if (n.big) {
        var g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 7);
        g.addColorStop(0, 'rgba(' + accent + ',0.55)'); g.addColorStop(1, 'rgba(' + accent + ',0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(n.x, n.y, n.r * 7, 0, Math.PI * 2); ctx.fill();
      }
      ctx.fillStyle = 'rgba(' + accent + ',' + (n.big ? 0.95 : 0.6) + ')';
      ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2); ctx.fill();
    }
  }
  function frame(ts) {
    if (!running) return;
    var dt = last ? Math.min(50, ts - last) : 16; last = ts;
    step(dt); draw();
    raf = requestAnimationFrame(frame);
  }
  function start() { if (running || reduce) return; running = true; last = 0; raf = requestAnimationFrame(frame); }
  function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }

  size(); draw();
  var ro = window.ResizeObserver ? new ResizeObserver(function () { size(); draw(); }) : null;
  if (ro) ro.observe(host); else window.addEventListener('resize', function () { size(); draw(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) start(); else stop(); });
    }, { threshold: 0.05 }).observe(host);
  } else {
    start();
  }
  document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else start(); });
})();
