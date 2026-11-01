// ZENIA, la conversación de ejemplo del agente (sección «demo» de la portada).
// Cambia de negocio con los botones y reproduce los mensajes uno a uno, en el idioma
// de la página. Sin script, la página muestra la conversación del restaurante tal cual.
(function () {
  var DATA = {
    es: {
      restaurante: {
        name: 'La Terraza · Restaurante', status: 'en línea',
        sys: 'Reserva guardada en el CRM · Recordatorio programado para mañana a las 18:00',
        msgs: [
          ['in', 'Hola, ¿tienen mesa para 4 mañana a las 21:00?', '23:48'],
          ['out', '¡Hola! Sí, nos queda mesa para 4 a las 21:00, en la terraza o en el salón. ¿Cuál prefieres?', '23:48'],
          ['in', 'Terraza. A nombre de Laura.', '23:49'],
          ['out', 'Listo, Laura: mesa para 4 mañana a las 21:00 en la terraza. Te mando un recordatorio mañana a las 18:00. ¿Alguna alergia que debamos saber?', '23:49'],
          ['in', 'Sin gluten, gracias', '23:50'],
          ['out', 'Anotado, avisamos a cocina. ¡Hasta mañana!', '23:50']
        ]
      },
      clinica: {
        name: 'Clínica Dental Norte', status: 'en línea',
        sys: 'Cita cambiada en el CRM · Recordatorio programado 24 h antes',
        msgs: [
          ['in', 'Buenas noches, ¿puedo cambiar mi cita del jueves? No puedo a las 10.', '22:15'],
          ['out', 'Claro, Marta. El jueves hay hueco a las 12:30 y a las 17:00 con la Dra. Ruiz. ¿Cuál te viene mejor?', '22:15'],
          ['in', 'A las 17:00.', '22:16'],
          ['out', 'Hecho: jueves a las 17:00 con la Dra. Ruiz. Te envío un recordatorio el miércoles. Si necesitas moverla otra vez, escríbeme aquí.', '22:16'],
          ['in', 'Perfecto, gracias', '22:17'],
          ['out', 'A ti. ¡Hasta el jueves!', '22:17']
        ]
      },
      gimnasio: {
        name: 'Gimnasio Forma', status: 'en línea',
        sys: 'Lead calificado en el CRM · Clase de prueba agendada',
        msgs: [
          ['in', 'Hola, ¿cuánto cuesta la mensualidad?', '23:02'],
          ['out', '¡Hola! La cuota es 39 € al mes sin permanencia, con acceso a todas las clases. ¿Quieres probar una clase gratis esta semana?', '23:02'],
          ['in', 'Sí, ¿puede ser el miércoles por la tarde?', '23:03'],
          ['out', 'El miércoles hay funcional a las 18:30 y spinning a las 19:30. ¿Cuál te apunto?', '23:03'],
          ['in', 'Funcional. Soy Diego', '23:04'],
          ['out', 'Listo, Diego: funcional el miércoles a las 18:30. Trae ropa cómoda y llega 10 minutos antes. ¡Te esperamos!', '23:04']
        ]
      }
    },
    en: {
      restaurante: {
        name: 'La Terraza · Restaurant', status: 'online',
        sys: 'Booking saved to the CRM · Reminder scheduled for tomorrow at 18:00',
        msgs: [
          ['in', 'Hi, do you have a table for 4 tomorrow at 21:00?', '23:48'],
          ['out', 'Hi! Yes, we still have a table for 4 at 21:00, on the terrace or in the dining room. Which do you prefer?', '23:48'],
          ['in', 'Terrace. Under Laura.', '23:49'],
          ['out', 'Done, Laura: table for 4 tomorrow at 21:00 on the terrace. I will send you a reminder tomorrow at 18:00. Any allergies we should know about?', '23:49'],
          ['in', 'Gluten free, thanks', '23:50'],
          ['out', 'Noted, we will tell the kitchen. See you tomorrow!', '23:50']
        ]
      },
      clinica: {
        name: 'Clínica Dental Norte', status: 'online',
        sys: 'Appointment moved in the CRM · Reminder scheduled 24 h before',
        msgs: [
          ['in', 'Good evening, can I move my Thursday appointment? I cannot make 10:00.', '22:15'],
          ['out', 'Of course, Marta. On Thursday there is 12:30 or 17:00 with Dr. Ruiz. Which works better?', '22:15'],
          ['in', '17:00.', '22:16'],
          ['out', 'Done: Thursday at 17:00 with Dr. Ruiz. I will send a reminder on Wednesday. If you need to move it again, just write here.', '22:16'],
          ['in', 'Perfect, thank you', '22:17'],
          ['out', 'Thank you. See you Thursday!', '22:17']
        ]
      },
      gimnasio: {
        name: 'Gimnasio Forma', status: 'online',
        sys: 'Lead qualified in the CRM · Trial class booked',
        msgs: [
          ['in', 'Hi, how much is the monthly membership?', '23:02'],
          ['out', 'Hi! It is 39 € a month with no lock-in, all classes included. Want to try a free class this week?', '23:02'],
          ['in', 'Yes, could it be Wednesday afternoon?', '23:03'],
          ['out', 'On Wednesday there is functional at 18:30 and spinning at 19:30. Which one shall I book?', '23:03'],
          ['in', 'Functional. I am Diego', '23:04'],
          ['out', 'Done, Diego: functional on Wednesday at 18:30. Bring comfortable clothes and arrive 10 minutes early. See you!', '23:04']
        ]
      }
    }
  };

  var root = document.getElementById('demoChat');
  if (!root) return;
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.demo-switch button'));
  var body = root.querySelector('.chat-body');
  var head = root.querySelector('.chat-head');
  var sys = root.querySelector('.chat-sys');
  var timers = [];
  var current = 'restaurante';
  var motion = function () {
    return document.documentElement.classList.contains('js') && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  };

  function lang() {
    var l = (document.documentElement.lang || 'es').slice(0, 2).toLowerCase();
    return DATA[l] ? l : 'es';
  }
  function esc(s) {
    return s.replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function later(ms, fn) { timers.push(setTimeout(fn, ms)); }

  function render(key) {
    timers.forEach(clearTimeout); timers = [];
    current = key;
    var d = DATA[lang()][key];
    head.querySelector('strong').textContent = d.name;
    head.querySelector('strong + span').textContent = d.status;
    var av = head.querySelector('.chat-avatar');
    if (av) av.textContent = d.name.charAt(0);
    sys.textContent = d.sys;
    body.innerHTML = '';
    var typing = document.createElement('div');
    typing.className = 'chat-typing'; typing.hidden = true; typing.setAttribute('aria-hidden', 'true');
    typing.innerHTML = '<i></i><i></i><i></i>';
    var t = 250;
    d.msgs.forEach(function (m) {
      var el = document.createElement('div');
      el.className = 'msg ' + m[0];
      el.innerHTML = esc(m[1]) + '<time>' + esc(m[2]) + '</time>';
      body.appendChild(el);
      if (!motion()) { el.classList.add('shown'); return; }
      if (m[0] === 'out') {
        later(t, function () { typing.hidden = false; body.appendChild(typing); });
        t += 900;
        later(t, function () { typing.hidden = true; el.classList.add('shown'); });
      } else {
        later(t, function () { el.classList.add('shown'); });
      }
      t += 700;
    });
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
