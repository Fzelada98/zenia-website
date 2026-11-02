// ZENIA, la escena de la portada, v4: un WhatsApp real dentro de un teléfono y, detrás, el CRM
// hecho a la medida de cada negocio. Cambia de negocio con los botones y reproduce la
// conversación como la vería el cliente: la hora es la del visitante, «escribiendo…» en la
// cabecera mientras responde el agente, ticks azules al leer, botones de respuesta rápida
// (WhatsApp Business API) y, al terminar, la fila nueva aparece en el CRM y sus cifras suben.
// Sin script, la página muestra el restaurante tal cual, con la fila ya en el CRM.
(function () {
  var DATA = {
    es: {
      caption: { night: 'Lo que hace el agente a las {t}, cuando ya cerraste', day: 'Lo que hace el agente ahora, a las {t}, mientras tú atiendes' },
      status: { online: 'en línea', typing: 'escribiendo…' },
      day: 'Hoy', lock: 'Los mensajes están cifrados de extremo a extremo.', input: 'Mensaje',
      crmTag: 'CRM a medida', updated: 'Actualizado ahora', agentState: 'Por el agente', settings: 'Ajustes',
      restaurante: {
        name: 'La Terraza · Restaurante', avatar: 'L', brand: 'La Terraza', where: 'Madrid · 2 salas',
        crm: {
          tabs: ['Reservas', 'Clientes', 'Campañas', 'Agente'],
          kpis: [['Reservas para mañana', '23', '+1'], ['Ocupación a las 21:00', '92 %', ''], ['Atendidas por el agente', '15', '+1']],
          title: 'Reservas de mañana', when: 'Martes', cols: ['Hora', 'Nombre', 'Pax', 'Zona', 'Notas', 'Estado'], opt: [3, 4],
          rows: [
            ['20:00', 'Familia Ortega', '6', 'Salón', 'Cumpleaños', 'ok', 'Confirmada'],
            ['20:30', 'Marc Vidal', '2', 'Terraza', '—', 'ok', 'Confirmada'],
            ['21:00', 'Laura', '4', 'Terraza', 'Sin gluten', 'agent', '', true],
            ['21:00', 'Ana Ruiz', '3', 'Salón', 'Silla bebé', 'wait', 'Pendiente'],
            ['21:30', 'Pedro Lima', '2', 'Terraza', '—', 'ok', 'Confirmada'],
            ['22:00', 'Grupo Sato', '8', 'Salón', 'Menú degustación', 'ok', 'Confirmada']
          ]
        },
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
        name: 'Clínica Dental Norte', avatar: 'C', brand: 'Clínica Dental Norte', where: 'Valencia · 3 gabinetes',
        crm: {
          tabs: ['Agenda', 'Pacientes', 'Recordatorios', 'Agente'],
          kpis: [['Citas el jueves', '18', ''], ['Huecos libres', '3', '+1'], ['Cambios hechos por el agente', '6', '+1']],
          title: 'Agenda del jueves · Dra. Ruiz', when: 'Jueves', cols: ['Hora', 'Paciente', 'Tratamiento', 'Recordatorio', 'Estado'], opt: [2, 3],
          rows: [
            ['10:00', 'Libre', '—', '—', 'off', 'Hueco liberado'],
            ['10:30', 'Jorge Peña', 'Limpieza', 'Enviado', 'ok', 'Confirmada'],
            ['12:30', 'Libre', '—', '—', 'off', 'Disponible'],
            ['16:00', 'Elena Soto', 'Revisión', 'Enviado', 'ok', 'Confirmada'],
            ['17:00', 'Marta Gil', 'Revisión', 'Miércoles 17:00', 'agent', '', true],
            ['17:30', 'Luis Mora', 'Empaste', 'Enviado', 'ok', 'Confirmada']
          ]
        },
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
        name: 'Gimnasio Forma', avatar: 'G', brand: 'Gimnasio Forma', where: 'Sevilla · 420 socios',
        crm: {
          tabs: ['Leads', 'Socios', 'Clases', 'Agente'],
          kpis: [['Leads esta semana', '31', '+1'], ['Pruebas agendadas', '12', '+1'], ['Altas este mes', '7', '']],
          title: 'Leads de esta semana', when: 'Semana 45', cols: ['Nombre', 'Origen', 'Interés', 'Prueba', 'Estado'], opt: [1, 2],
          rows: [
            ['Diego', 'WhatsApp', 'Funcional', 'Mié 18:30', 'agent', '', true],
            ['Carla Ríos', 'Instagram', 'Spinning', 'Jue 19:30', 'ok', 'Prueba agendada'],
            ['Tomás Vega', 'Web', 'Pesas', '—', 'wait', 'Sin respuesta'],
            ['Nuria Bel', 'WhatsApp', 'Yoga', 'Vie 10:00', 'ok', 'Alta'],
            ['Iván Soto', 'Google', 'Funcional', 'Mar 18:30', 'ok', 'Prueba hecha'],
            ['Sara Núñez', 'Instagram', 'Pilates', '—', 'wait', 'Seguimiento jueves']
          ]
        },
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
      crmTag: 'Tailor-made CRM', updated: 'Updated just now', agentState: 'By the agent', settings: 'Settings',
      restaurante: {
        name: 'La Terraza · Restaurant', avatar: 'L', brand: 'La Terraza', where: 'Madrid · 2 rooms',
        crm: {
          tabs: ['Bookings', 'Guests', 'Campaigns', 'Agent'],
          kpis: [['Bookings for tomorrow', '23', '+1'], ['Occupancy at 21:00', '92 %', ''], ['Handled by the agent', '15', '+1']],
          title: 'Tomorrow’s bookings', when: 'Tuesday', cols: ['Time', 'Name', 'Guests', 'Area', 'Notes', 'Status'], opt: [3, 4],
          rows: [
            ['20:00', 'Ortega family', '6', 'Dining room', 'Birthday', 'ok', 'Confirmed'],
            ['20:30', 'Marc Vidal', '2', 'Terrace', '—', 'ok', 'Confirmed'],
            ['21:00', 'Laura', '4', 'Terrace', 'Gluten free', 'agent', '', true],
            ['21:00', 'Ana Ruiz', '3', 'Dining room', 'High chair', 'wait', 'Pending'],
            ['21:30', 'Pedro Lima', '2', 'Terrace', '—', 'ok', 'Confirmed'],
            ['22:00', 'Sato party', '8', 'Dining room', 'Tasting menu', 'ok', 'Confirmed']
          ]
        },
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
        name: 'Clínica Dental Norte', avatar: 'C', brand: 'Clínica Dental Norte', where: 'Valencia · 3 surgeries',
        crm: {
          tabs: ['Schedule', 'Patients', 'Reminders', 'Agent'],
          kpis: [['Appointments Thursday', '18', ''], ['Open slots', '3', '+1'], ['Changes made by the agent', '6', '+1']],
          title: 'Thursday schedule · Dr. Ruiz', when: 'Thursday', cols: ['Time', 'Patient', 'Treatment', 'Reminder', 'Status'], opt: [2, 3],
          rows: [
            ['10:00', 'Open', '—', '—', 'off', 'Slot freed'],
            ['10:30', 'Jorge Peña', 'Cleaning', 'Sent', 'ok', 'Confirmed'],
            ['12:30', 'Open', '—', '—', 'off', 'Available'],
            ['16:00', 'Elena Soto', 'Check-up', 'Sent', 'ok', 'Confirmed'],
            ['17:00', 'Marta Gil', 'Check-up', 'Wednesday 17:00', 'agent', '', true],
            ['17:30', 'Luis Mora', 'Filling', 'Sent', 'ok', 'Confirmed']
          ]
        },
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
        name: 'Gimnasio Forma', avatar: 'G', brand: 'Gimnasio Forma', where: 'Seville · 420 members',
        crm: {
          tabs: ['Leads', 'Members', 'Classes', 'Agent'],
          kpis: [['Leads this week', '31', '+1'], ['Trials booked', '12', '+1'], ['Sign-ups this month', '7', '']],
          title: 'This week’s leads', when: 'Week 45', cols: ['Name', 'Source', 'Interest', 'Trial', 'Status'], opt: [1, 2],
          rows: [
            ['Diego', 'WhatsApp', 'Functional', 'Wed 18:30', 'agent', '', true],
            ['Carla Ríos', 'Instagram', 'Spinning', 'Thu 19:30', 'ok', 'Trial booked'],
            ['Tomás Vega', 'Web', 'Weights', '—', 'wait', 'No reply yet'],
            ['Nuria Bel', 'WhatsApp', 'Yoga', 'Fri 10:00', 'ok', 'Signed up'],
            ['Iván Soto', 'Google', 'Functional', 'Tue 18:30', 'ok', 'Trial done'],
            ['Sara Núñez', 'Instagram', 'Pilates', '—', 'wait', 'Follow-up Thursday']
          ]
        },
        msgs: [
          { d: 'in', t: 'Hi, how much is the monthly membership?', m: 0 },
          { d: 'out', t: 'It is 39 € a month with no lock-in, all classes included. Want to try a free class this week?', buttons: ['Yes, I want to try', 'More information'], tap: 0, m: 0 },
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
  var win = document.getElementById('crmWindow');
  var markHTML = (win && win.querySelector('.crm-mark')) ? win.querySelector('.crm-mark').innerHTML : 'Z';
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
    return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
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

  // La pantalla del CRM, hecha para el negocio elegido.
  function renderCRM(L, d) {
    if (!win) return;
    var c = d.crm;
    win.classList.remove('updated');
    win.setAttribute('aria-label', L.crmTag + ' · ' + d.brand);
    var tabs = c.tabs.map(function (t, i) { return '<span' + (i === 0 ? ' class="on"' : '') + '>' + esc(t) + '</span>'; }).join('');
    var html = '<aside class="crm-side"><span class="crm-mark" aria-hidden="true">' + markHTML + '</span>' + tabs + '<span>' + esc(L.settings) + '</span><div class="crm-who"><b>' + esc(d.brand) + '</b>' + esc(d.where) + '</div></aside><div class="crm-main">';
    html += '<div class="crm-top"><span class="crm-mark" aria-hidden="true">' + markHTML + '</span><span class="crm-brand">' + esc(d.brand) + ' <span>· ' + esc(L.crmTag) + '</span></span><span class="crm-live">' + esc(L.updated) + '</span><div class="crm-tabs">' + tabs + '</div></div>';
    html += '<div class="crm-kpis">' + c.kpis.map(function (k) {
      return '<div class="crm-kpi"><small>' + esc(k[0]) + '</small><strong>' + esc(k[1]) + (k[2] ? '<i>' + esc(k[2]) + '</i>' : '') + '</strong></div>';
    }).join('') + '</div>';
    html += '<div class="crm-title"><b>' + esc(c.title) + '</b><em>' + esc(c.when) + '</em></div>';
    html += '<table class="crm"><thead><tr>' + c.cols.map(function (col, i) { return '<th' + (c.opt.indexOf(i) >= 0 ? ' class="opt"' : '') + '>' + esc(col) + '</th>'; }).join('') + '</tr></thead><tbody>';
    c.rows.forEach(function (r) {
      var n = c.cols.length - 1;
      var isNew = r[n + 2] === true;
      html += '<tr' + (isNew ? ' class="crm-row new"' : '') + '>';
      for (var i = 0; i < n; i++) {
        var cls = [];
        if (c.opt.indexOf(i) >= 0) cls.push('opt');
        if (i > 0 && c.opt.indexOf(i) >= 0 && i === n - 1) cls.push('dim');
        if (c.opt.indexOf(i) >= 0 && i === c.opt[c.opt.length - 1]) cls.push('dim');
        html += '<td' + (cls.length ? ' class="' + cls.join(' ') + '"' : '') + '>' + esc(r[i]) + '</td>';
      }
      var state = r[n], label = r[n + 1] || L.agentState;
      html += '<td><span class="crm-state ' + esc(state) + '">' + esc(label) + '</span></td></tr>';
    });
    html += '</tbody></table></div>';
    win.innerHTML = html;
  }

  function showNewRow() {
    if (!win) return;
    var row = win.querySelector('.crm-row.new');
    if (row) row.classList.add('show');
    win.classList.add('updated');
    // las cifras suben con la fila nueva
    win.querySelectorAll('.crm-kpi strong').forEach(function (k) {
      var inc = k.querySelector('i');
      if (!inc) return;
      var m = /^(\d+)/.exec(k.firstChild.nodeValue || '');
      if (m) k.firstChild.nodeValue = String(parseInt(m[1], 10) + 1) + (k.firstChild.nodeValue.slice(m[1].length));
    });
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
    renderCRM(L, d);
    body.innerHTML = '<div class="chat-day">' + esc(L.day) + '</div><div class="chat-lock">' + esc(L.lock) + '</div>';
    var t = 300;
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
    });
    if (!motion()) { showNewRow(); }
    else { later(t + 400, showNewRow); }
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-sector') === key)); });
  }

  buttons.forEach(function (b) {
    b.addEventListener('click', function () { render(b.getAttribute('data-sector')); });
  });

  // Si la página cambia de idioma (la portada en inglés se traduce en el navegador),
  // la escena se vuelve a pintar en ese idioma.
  if (window.MutationObserver) {
    new MutationObserver(function () { render(current); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  }

  // La hora del teléfono sigue la del visitante.
  tick();
  setInterval(tick, 30000);

  // Arranca cuando la escena entra en pantalla, para que la secuencia se vea.
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
