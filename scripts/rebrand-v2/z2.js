/* ZENIA v2 (nov-2026). Piezas vivas: el WhatsApp de la portada (el visitante toca preguntas de cliente),
   «Así funciona» (una cita completa que se reproduce sola al llegar), las pestañas del panel y el
   formulario «tu demo en 48 h». Sin dependencias. Datos en <script type="application/json" id="z2-data">. */
(function () {
  'use strict';
  var doc = document;
  var DATA = {};
  try { DATA = JSON.parse(doc.getElementById('z2-data').textContent); } catch (e) {}
  var DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
  var HORAS = { clinica: ['10:30', '17:00', '12:00'], taller: ['9:00', '16:30', '11:00'], autoescuela: ['18:00', '11:00', '19:00'] };
  function hora() { var d = new Date(); return d.getHours() + ':' + ('0' + d.getMinutes()).slice(-2); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function huecos(v) {
    var out = [], d = new Date(), h = HORAS[v] || HORAS.clinica, n = 0;
    while (out.length < 3) {
      d.setDate(d.getDate() + 1); n++;
      if (d.getDay() === 0) continue;
      out.push((n === 1 ? 'mañana' : 'el ' + DIAS[d.getDay()] + ' ' + d.getDate()) + ' a las ' + h[out.length]);
    }
    return out;
  }

  /* ---------- un WhatsApp que se puede tocar ---------- */
  function Chat(root) {
    this.root = root;
    this.body = root.querySelector('.chat-body');
    this.chips = root.querySelector('.chips');
    this.status = root.querySelector('.chat-status');
    this.name = root.querySelector('.chat-who strong');
    this.avatar = root.querySelector('.chat-avatar');
    this.busy = false;
  }
  Chat.prototype.scroll = function () { this.body.scrollTop = this.body.scrollHeight; };
  Chat.prototype.bubble = function (dir, text, extra) {
    var m = doc.createElement('div'); m.className = 'msg ' + dir;
    m.innerHTML = '<span>' + esc(text) + '</span>' + (extra || '') + '<time>' + hora() + '</time>';
    this.body.appendChild(m); this.scroll(); return m;
  };
  Chat.prototype.typing = function (ms, then) {
    var self = this;
    this.status.textContent = 'escribiendo…'; this.status.classList.add('typing');
    var t = doc.createElement('div'); t.className = 'typing-bubble'; t.innerHTML = '<i></i><i></i><i></i>';
    this.body.appendChild(t); this.scroll();
    this.timer = setTimeout(function () { t.remove(); self.status.textContent = 'en línea'; self.status.classList.remove('typing'); then(); }, ms);
  };
  Chat.prototype.load = function (d) {
    clearTimeout(this.timer); this.busy = false;
    this.d = JSON.parse(JSON.stringify(d));
    this.name.textContent = d.nombre; this.avatar.textContent = d.inicial || d.nombre.charAt(0);
    this.body.innerHTML = '<div class="chat-day">Hoy</div>';
    if (d.saludo) this.bubble('out', d.saludo);
    this.chipsPaint();
  };
  Chat.prototype.chipsPaint = function () {
    var self = this, d = this.d, hay = false;
    this.chips.innerHTML = '';
    if (!d._cita) {
      var b = doc.createElement('button'); b.type = 'button'; b.className = 'cita'; b.textContent = d.cita.chip;
      b.onclick = function () { self.cita(); }; this.chips.appendChild(b); hay = true;
    }
    d.preguntas.forEach(function (q, i) {
      if (q._u) return;
      var b = doc.createElement('button'); b.type = 'button'; b.textContent = q.p;
      b.onclick = function () { self.pregunta(i); }; self.chips.appendChild(b); hay = true;
    });
    if (!hay) {
      var r = doc.createElement('button'); r.type = 'button'; r.textContent = 'Volver a empezar';
      r.onclick = function () { self.load(self.orig); }; this.chips.appendChild(r);
    }
    this.chips.scrollLeft = 0;
    this.chips.classList.toggle('fin', this.chips.scrollWidth <= this.chips.clientWidth + 2);
  };
  Chat.prototype.pregunta = function (i) {
    if (this.busy) return; this.busy = true;
    var self = this, q = this.d.preguntas[i]; q._u = true; this.chipsPaint();
    this.bubble('in', q.p);
    this.typing(700 + Math.min(1500, q.r.length * 9), function () { self.bubble('out', q.r); self.busy = false; });
  };
  Chat.prototype.cita = function () {
    if (this.busy) return; this.busy = true;
    var self = this, c = this.d.cita; this.d._cita = true; this.chipsPaint();
    this.bubble('in', c.p);
    this.typing(1100, function () {
      var hs = huecos(self.d.vertical);
      var m = self.bubble('out', c.intro, '<span class="msg-buttons">' + hs.map(function (h) { return '<button type="button">' + esc(h) + '</button>'; }).join('') + '</span>');
      self.busy = false;
      [].forEach.call(m.querySelectorAll('.msg-buttons button'), function (b) {
        b.onclick = function () {
          if (self.busy) return; self.busy = true;
          [].forEach.call(m.querySelectorAll('.msg-buttons button'), function (x) { x.disabled = true; });
          b.classList.add('tapped');
          var h = b.textContent; self.bubble('in', h);
          self.typing(900, function () {
            self.bubble('out', '¿A nombre de quién lo reservo?');
            self.timer = setTimeout(function () {
              self.bubble('in', 'Laura Gómez');
              self.typing(1200, function () {
                self.bubble('out', 'Listo, Laura: ' + c.servicio + ' ' + h + '. Te mando un recordatorio por aquí el día antes.');
                self.busy = false;
              });
            }, 800);
          });
        };
      });
    });
  };

  var live = doc.querySelector('[data-chat="live"]');
  if (live && DATA.negocios) {
    var chat = new Chat(live);
    var claves = Object.keys(DATA.negocios);
    var abrir = function (k) {
      chat.orig = DATA.negocios[k]; chat.load(DATA.negocios[k]);
      [].forEach.call(doc.querySelectorAll('.seg button'), function (b) { b.setAttribute('aria-pressed', b.dataset.k === k ? 'true' : 'false'); });
    };
    [].forEach.call(doc.querySelectorAll('.seg button'), function (b) { b.addEventListener('click', function () { abrir(b.dataset.k); }); });
    abrir(claves[0]);
    var t = live.querySelector('.phone-status span'); if (t) t.textContent = hora();
  }

  /* ---------- «Así funciona»: una cita completa que se reproduce sola ---------- */
  var how = doc.querySelector('[data-chat="auto"]');
  if (how && DATA.guion) {
    var steps = doc.querySelectorAll('.steps li');
    var body = how.querySelector('.chat-body'), status = how.querySelector('.chat-status');
    var tm = [], corriendo = false;
    how.querySelector('.chat-who strong').textContent = DATA.guion.nombre;
    how.querySelector('.chat-avatar').textContent = DATA.guion.nombre.charAt(0);
    var paso = function (n) {
      [].forEach.call(steps, function (li, i) { li.classList.toggle('on', i === n); li.classList.toggle('done', i < n); });
    };
    var pon = function (dir, txt, extra) {
      var m = doc.createElement('div');
      if (dir === 'tag') { m.className = 'chat-day'; m.textContent = txt; }
      else { m.className = 'msg ' + dir; m.innerHTML = '<span>' + esc(txt) + '</span>' + (extra || '') + '<time>' + hora() + '</time>'; }
      body.appendChild(m); body.scrollTop = body.scrollHeight;
    };
    var correr = function () {
      tm.forEach(clearTimeout); tm = []; corriendo = true;
      body.innerHTML = '<div class="chat-day">Hoy</div>';
      var t = 400;
      DATA.guion.mensajes.forEach(function (m) {
        if (m.dir === 'out') {
          tm.push(setTimeout(function () { status.textContent = 'escribiendo…'; status.classList.add('typing'); }, t));
          t += 900;
        }
        tm.push(setTimeout(function () {
          status.textContent = 'en línea'; status.classList.remove('typing');
          paso(m.paso);
          var extra = m.botones ? '<span class="msg-buttons">' + m.botones.map(function (b, i) { return '<button type="button" disabled class="' + (i === m.elegido ? 'tapped' : '') + '">' + esc(b) + '</button>'; }).join('') + '</span>' : '';
          pon(m.dir, m.t, extra);
        }, t));
        t += m.dir === 'tag' ? 1400 : 1500 + Math.min(1600, m.t.length * 12);
      });
      tm.push(setTimeout(function () { corriendo = false; }, t));
    };
    var visto = false;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es, o) {
        es.forEach(function (e) { if (e.isIntersecting && !visto) { visto = true; correr(); o.disconnect(); } });
      }, { threshold: 0.35 }).observe(how);
    } else { correr(); }
    var rp = doc.querySelector('.replay'); if (rp) rp.addEventListener('click', correr);
    paso(0);
  }

  /* ---------- pestañas del panel ---------- */
  [].forEach.call(doc.querySelectorAll('.tabs'), function (tabs) {
    var bs = tabs.querySelectorAll('button');
    [].forEach.call(bs, function (b) {
      b.addEventListener('click', function () {
        [].forEach.call(bs, function (x) {
          var on = x === b; x.setAttribute('aria-selected', on ? 'true' : 'false');
          var p = doc.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = !on;
        });
        var side = doc.querySelectorAll('.app-side span[data-tab]');
        [].forEach.call(side, function (s) { s.classList.toggle('on', s.dataset.tab === b.getAttribute('aria-controls')); });
      });
    });
  });

  /* ---------- formulario «tu demo en 48 h» ---------- */
  [].forEach.call(doc.querySelectorAll('form.form'), function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = function (n) { var el = f.elements[n]; return el ? String(el.value || '').trim() : ''; };
      if (!v('contacto') || !v('web')) { f.reportValidity && f.reportValidity(); return; }
      var qa = /[?&]qa\b/.test(location.search) || location.hostname === 'localhost' || navigator.webdriver;
      var carga = JSON.stringify({
        site: 'zenia', kind: 'qualify', src: 'demo-form', brand: v('sector') || 'Otro', model: 'Ver mi demo',
        name: v('nombre').slice(0, 80), contact: v('contacto').slice(0, 120), city: v('web').slice(0, 120),
        year: doc.title.slice(0, 30), locale: 'es', path: location.pathname, ref: doc.referrer || ''
      });
      try { if (!qa) { if (navigator.sendBeacon) navigator.sendBeacon('https://gaia-relojes.onrender.com/gwb/lead', carga); else fetch('https://gaia-relojes.onrender.com/gwb/lead', { method: 'POST', body: carga, keepalive: true }); } } catch (err) {}
      f.classList.add('sent');
    });
  });

  /* ---------- menú del móvil: se cierra al elegir ---------- */
  var menu = doc.querySelector('.menu');
  if (menu) [].forEach.call(menu.querySelectorAll('a'), function (a) { a.addEventListener('click', function () { menu.open = false; }); });
})();
