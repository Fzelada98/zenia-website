// ZENIA, la conversación de ejemplo del agente (portada), v3: un WhatsApp real dentro de un teléfono.
// Cambia de negocio con los botones y reproduce la conversación como la vería el cliente:
// la hora es la del visitante, «escribiendo…» en la cabecera mientras responde el agente,
// ticks azules al leer, botones de respuesta rápida (WhatsApp Business API) y, al final,
// la ficha que queda guardada en el CRM. Sin script, la página muestra la conversación del
// restaurante tal cual y la ficha del CRM visible.
(function () {
  var DATA = {
    es: {
      caption: { night: 'Lo que hace el agente a las {t}, cuando ya cerraste', day: 'Lo que hace el agente ahora, a las {t}, mientras tú atiendes' },
      status: { online: 'en línea', typing: 'escribiendo…' },
      day: 'Hoy', lock: 'Los mensajes están cifrados de extremo a extremo.', input: 'Mensaje',
      restaurante: {
        name: 'La Terraza · Restaurante', avatar: 'L',
        crm: { label: 'Guardado en el CRM', title: 'Laura · Mesa para 4', lines: ['Mañana 21:00 · Terraza · Sin gluten', 'Recordatorio automático: mañana a las 18:00'] },
        msgs: [
          { d: 'in', t: 'Hola, ¿tienen mesa para 4 mañana a las 21:00?', m: 0 },
          { d: 'out', t: '¡Hola! Sí, nos queda mesa para 4 a las 21:00. ¿Dónde prefieres?', buttons: ['Terraza', 'Salón'], tap: 0, m: 0 },
          { d: 'in', t: 'Terraza', m: 1, reply: true },
          { d: 'in', t: 'A nombre de Laura.', m: 1 },
          { d: 'out', t: 'Listo, Laura: mesa para 4 mañana a las 21:00 en la terraza. Te mando un recordatorio mañana a las 18:00. ¿Alguna alergia que debamos saber?', m: 1 },
          { d: 'in', t: 'Sin gluten, gracias', m: 2 },
          { d: 'out', t: 'Anotado, avisamos a cocina. ¡Hasta mañana!', m: 2 }
        ]
      },
      clinica: {
        name: 'Clínica Dental Norte', avatar: 'C',
        crm: { label: 'Cita cambiada en el CRM', title: 'Marta · Jueves 17:00', lines: ['Dra. Ruiz · Revisión', 'Recordatorio automático: miércoles a las 17:00'] },
        msgs: [
          { d: 'in', t: 'Buenas noches, ¿puedo cambiar mi cita del jueves? No puedo a las 10.', m: 0 },
          { d: 'out', t: 'Claro, Marta. El jueves hay hueco con la Dra. Ruiz. ¿Cuál te viene mejor?', buttons: ['Jueves 12:30', 'Jueves 17:00'], tap: 1, m: 0 },
          { d: 'in', t: 'Jueves 17:00', m: 1, reply: true },
          { d: 'out', t: 'Hecho: jueves a las 17:00 con la Dra. Ruiz. Te envío un recordatorio el miércoles. Si necesitas moverla otra vez, escríbeme aquí.', m: 1 },
          { d: 'in', t: 'Perfecto, gracias', m: 2 },
          { d: 'out', t: 'A ti. ¡Hasta el jueves!', m: 2 }
        ]
      },
      gimnasio: {
        name: 'Gimnasio Forma', avatar: 'G',
        crm: { label: 'Lead calificado en el CRM', title: 'Diego · Clase de prueba', lines: ['Funcional · Miércoles 18:30', 'Seguimiento automático si no viene: jueves 10:00'] },
        msgs: [
          { d: 'in', t: 'Hola, ¿cuánto cuesta la mensualidad?', m: 0 },
          { d: 'out', t: '¡Hola! La cuota es 39 € al mes sin permanencia, con acceso a todas las clases. ¿Quieres probar una clase gratis esta semana?', buttons: ['Sí, quiero probar', 'Más información'], tap: 0, m: 0 },
          { d: 'in', t: 'Sí, quiero probar', m: 1, reply: true },
          { d: 'in', t: '¿Puede ser el miércoles por la tarde? Soy Diego', m: 1 },
          { d: 'out', t: 'El miércoles hay funcional a las 18:30 y spinning a las 19:30. ¿Cuál te apunto?', buttons: ['Funcional 18:30', 'Spinning 19:30'], tap: 0, m: 1 },
          { d: 'in', t: 'Funcional 18:30', m: 2, reply: true },
          { d: 'out', t: 'Listo, Diego: funcional el miércoles a las 18:30. Trae ropa cómoda y llega 10 minutos antes. ¡Te esperamos!', m: 2 }
        ]
      }
    },
    en: {
      caption: { night: 'What the agent does at {t}, after you have closed', day: 'What the agent is doing right now, at {t}, while you serve customers' },
      status: { online: 'online', typing: 'typing…' },
      day: 'Today', lock: 'Messages are end-to-end encrypted.', input: 'Message',
      restaurante: {
        name: 'La Terraza · Restaurant', avatar: 'L',
        crm: { label: 'Saved to the CRM', title: 'Laura · Table for 4', lines: ['Tomorrow 21:00 · Terrace · Gluten free', 'Automatic reminder: tomorrow at 18:00'] },
        msgs: [
          { d: 'in', t: 'Hi, do you have a table for 4 tomorrow at 21:00?', m: 0 },
          { d: 'out', t: 'Hi! Yes, we still have a table for 4 at 21:00. Where would you like to sit?', buttons: ['Terrace', 'Dining room'], tap: 0, m: 0 },
          { d: 'in', t: 'Terrace', m: 1, reply: true },
          { d: 'in', t: 'Under Laura.', m: 1 },
          { d: 'out', t: 'Done, Laura: table for 4 tomorrow at 21:00 on the terrace. I will send you a reminder tomorrow at 18:00. Any allergies we should know about?', m: 1 },
          { d: 'in', t: 'Gluten free, thanks', m: 2 },
          { d: 'out', t: 'Noted, we will tell the kitchen. See you tomorrow!', m: 2 }
        ]
      },
      clinica: {
        name: 'Clínica Dental Norte', avatar: 'C',
        crm: { label: 'Appointment moved in the CRM', title: 'Marta · Thursday 17:00', lines: ['Dr. Ruiz · Check-up', 'Automatic reminder: Wednesday at 17:00'] },
        msgs: [
          { d: 'in', t: 'Good evening, can I move my Thursday appointment? I cannot make 10:00.', m: 0 },
          { d: 'out', t: 'Of course, Marta. Thursday has openings with Dr. Ruiz. Which works better?', buttons: ['Thursday 12:30', 'Thursday 17:00'], tap: 1, m: 0 },
          { d: 'in', t: 'Thursday 17:00', m: 1, reply: true },
          { d: 'out', t: 'Done: Thursday at 17:00 with Dr. Ruiz. I will send a reminder on Wednesday. If you need to move it again, just write here.', m: 1 },
          { d: 'in', t: 'Perfect, thank you', m: 2 },
          { d: 'out', t: 'Thank you. See you Thursday!', m: 2 }
        ]
      },
      gimnasio: {
        name: 'Gimnasio Forma', avatar: 'G',
        crm: { label: 'Lead qualified in the CRM', title: 'Diego · Trial class', lines: ['Functional · Wednesday 18:30', 'Automatic follow-up if he does not show: Thursday 10:00'] },
        msgs: [
          { d: 'in', t: 'Hi, how much is the monthly membership?', m: 0 },
          { d: 'out', t: 'Hi! It is 39 € a month with no lock-in, all classes included. Want to try a free class this week?', buttons: ['Yes, I want to try', 'More information'], tap: 0, m: 0 },
          { d: 'in', t: 'Yes, I want to try', m: 1, reply: true },
          { d: 'in', t: 'Could it be Wednesday afternoon? I am Diego', m: 1 },
          { d: 'out', t: 'On Wednesday there is functional at 18:30 and spinning at 19:30. Which one shall I book?', buttons: ['Functional 18:30', 'Spinning 19:30'], tap: 0, m: 1 },
          { d: 'in', t: 'Functional 18:30', m: 2, reply: true },
          { d: 'out', t: 'Done, Diego: functional on Wednesday at 18:30. Bring comfortable clothes and arrive 10 minutes early. See you!', m: 2 }
        ]
      }
    }
  };

  var root = document.getElementById('demoChat');
  if (!root) return;
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.demo-switch button'));
  var body = root.querySelector('.chat-body');
  var head = root.querySelector('.chat-head');
  var avatar = head.querySelector('.chat-avatar');
  var who = head.querySelector('.chat-who strong');
  var status = head.querySelector('.chat-status');
  var input = root.querySelector('.chat-input-field');
  var caption = document.getElementById('demoCaption');
  var clock = document.querySelector('.phone-time');
  var toast = document.getElementById('crmToast');
  var timers = [];
  var current = 'restaurante';
  var motion = function () {
    return document.documentElement.classList.contains('js') && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  };

  function lang() {
    var l = (document.documentElement.lang || 'es').slice(0, 2).toLowerCase();
    return DATA[l] ? l : 'es';
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function hhmm(d) { return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function esc(s) {
    return s.replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function later(ms, fn) { timers.push(setTimeout(fn, ms)); }

  function tick() {
    var now = new Date();
    if (clock) clock.textContent = hhmm(now);
    if (caption) {
      var L = DATA[lang()];
      var h = now.getHours();
      caption.textContent = (h >= 20 || h < 8 ? L.caption.night : L.caption.day).replace('{t}', hhmm(now));
    }
  }

  function bubble(m, when) {
    var el = document.createElement('div');
    el.className = 'msg ' + m.d + (m.reply ? ' reply' : '');
    var html = '<span class="msg-text">' + esc(m.t) + '</span><time>' + esc(when) + (m.d === 'out' ? '<i class="ticks" aria-hidden="true"></i>' : '') + '</time>';
    if (m.buttons) {
      html += '<span class="msg-buttons">' + m.buttons.map(function (b) { return '<span>' + esc(b) + '</span>'; }).join('') + '</span>';
    }
    el.innerHTML = html;
    return el;
  }

  function render(key) {
    timers.forEach(clearTimeout); timers = [];
    current = key;
    var L = DATA[lang()];
    var d = L[key];
    var now = new Date();
    var base = new Date(now.getTime() - 3 * 60000);
    who.textContent = d.name;
    status.textContent = L.status.online;
    if (avatar) avatar.textContent = d.avatar;
    if (input) input.textContent = L.input;
    tick();
    body.innerHTML = '<div class="chat-day">' + esc(L.day) + '</div><div class="chat-lock">' + esc(L.lock) + '</div>';
    if (toast) {
      toast.classList.remove('show');
      toast.querySelector('.crm-label').textContent = d.crm.label;
      toast.querySelector('strong').textContent = d.crm.title;
      var ps = toast.querySelectorAll('p:not(.crm-label)');
      d.crm.lines.forEach(function (line, i) { if (ps[i]) ps[i].textContent = line; });
    }
    var t = 300;
    var last = null;
    d.msgs.forEach(function (m) {
      var when = hhmm(new Date(base.getTime() + m.m * 60000));
      var el = bubble(m, when);
      if (!motion()) {
        body.appendChild(el); el.classList.add('shown');
        if (m.d === 'out') el.classList.add('read');
        if (m.buttons && typeof m.tap === 'number') el.querySelectorAll('.msg-buttons span')[m.tap].classList.add('tapped');
        return;
      }
      if (m.d === 'out') {
        later(t, function () { status.textContent = L.status.typing; });
        t += 1100;
        later(t, function () { status.textContent = L.status.online; body.appendChild(el); requestAnimationFrame(function () { el.classList.add('shown'); }); });
        t += 650;
        later(t, function () { el.classList.add('read'); });
        if (m.buttons && typeof m.tap === 'number') {
          var idx = m.tap;
          t += 900;
          later(t, function () { el.querySelectorAll('.msg-buttons span')[idx].classList.add('tapped'); });
          t += 250;
        } else {
          t += 500;
        }
      } else {
        later(t, function () { body.appendChild(el); requestAnimationFrame(function () { el.classList.add('shown'); }); });
        t += m.reply ? 500 : 900;
      }
      last = el;
    });
    if (toast) {
      if (!motion()) { toast.classList.add('show'); }
      else { later(t + 400, function () { toast.classList.add('show'); }); }
    }
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-sector') === key)); });
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () { render(b.getAttribute('data-sector')); });
  });

  // Si la página cambia de idioma (la portada en inglés se traduce en el navegador),
  // la conversación se vuelve a pintar en ese idioma.
  if (window.MutationObserver) {
    new MutationObserver(function () { render(current); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  }

  // La hora del teléfono sigue la del visitante.
  tick();
  setInterval(tick, 30000);

  // Arranca cuando la sección entra en pantalla, para que la secuencia se vea.
  var started = false;
  function start() { if (started) return; started = true; render(current); }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { start(); io.disconnect(); }
    }, { threshold: 0.25 });
    io.observe(root);
  } else {
    start();
  }
})();
