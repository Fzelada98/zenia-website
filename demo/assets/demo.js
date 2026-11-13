// ZENIA · demo privada por negocio. El visitante toca preguntas de cliente y el agente responde con
// la información pública del negocio (datos en #demo-data, generados por scripts/demos/build_demos.py).
// La ficha del CRM se rellena con lo que pasa en la conversación de esta visita: nada inventado.
(function () {
  var D = JSON.parse(document.getElementById('demo-data').textContent);
  var body = document.getElementById('chatBody'), chips = document.getElementById('chips'),
      status = document.getElementById('chatStatus'), rows = document.getElementById('crmRows'),
      busy = false, n = { ok: 0, esc: 0, cita: 0 };
  var MOTIVO = { info: 'Información', precio: 'Precio', horario: 'Horario', sede: 'Sedes', urgencia: 'Urgencia', derivar: 'Consulta especial', cita: 'Cita' };
  var HORAS = { clinica: ['10:30', '17:00', '12:00'], taller: ['9:00', '16:30', '11:00'], autoescuela: ['18:00', '11:00', '19:00'] };
  var DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

  function hora() { var d = new Date(); return d.getHours() + ':' + ('0' + d.getMinutes()).slice(-2); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function scroll() { body.scrollTop = body.scrollHeight; }

  function bubble(dir, text, extra) {
    var m = document.createElement('div');
    m.className = 'msg ' + dir;
    m.innerHTML = '<span>' + esc(text) + '</span>' + (extra || '') + '<time>' + hora() + '</time>';
    body.appendChild(m); scroll(); return m;
  }
  function typing(ms, then) {
    status.textContent = 'escribiendo…'; status.classList.add('typing');
    var t = document.createElement('div'); t.className = 'typing-bubble'; t.innerHTML = '<i></i><i></i><i></i>';
    body.appendChild(t); scroll();
    setTimeout(function () { t.remove(); status.textContent = 'en línea'; status.classList.remove('typing'); then(); }, ms);
  }
  function espera(texto) { return 700 + Math.min(1500, texto.length * 9); }

  function fila(motivo, detalle, estado, clase) {
    var vacio = rows.querySelector('.crm-empty'); if (vacio) vacio.remove();
    var tr = document.createElement('tr'); tr.className = 'new';
    tr.innerHTML = '<td>' + hora() + '</td><td>' + esc(motivo) + '</td><td class="opt">' + esc(detalle) + '</td><td><span class="state ' + clase + '">' + esc(estado) + '</span></td>';
    rows.insertBefore(tr, rows.firstChild);
    document.getElementById('kOk').textContent = n.ok;
    document.getElementById('kCita').textContent = n.cita;
    document.getElementById('kEsc').textContent = n.esc;
  }

  function huecos() {
    var out = [], d = new Date(), h = HORAS[D.vertical] || HORAS.clinica, dias = 0;
    while (out.length < 3) {
      d.setDate(d.getDate() + 1); dias++;
      if (d.getDay() === 0) continue;   // domingo cerrado
      var dia = dias === 1 ? 'mañana' : 'el ' + DIAS[d.getDay()] + ' ' + d.getDate();
      out.push(dia + ' a las ' + h[out.length]);
    }
    return out;
  }

  function pintarChips() {
    chips.innerHTML = '';
    var hay = false;
    if (!D._citaHecha) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'cita'; b.textContent = D.cita_demo.chip || 'Pedir cita';
      b.onclick = cita; chips.appendChild(b); hay = true;
    }
    D.conversacion.forEach(function (q, i) {
      if (q._usada) return;
      var b = document.createElement('button'); b.type = 'button'; b.textContent = q.pregunta;
      b.onclick = function () { pregunta(i); }; chips.appendChild(b); hay = true;
    });
    if (!hay) {
      var r = document.createElement('button'); r.type = 'button'; r.textContent = 'Volver a empezar';
      r.onclick = function () { location.reload(); }; chips.appendChild(r);
    }
    chips.scrollLeft = 0;
    chips.classList.toggle('fin', chips.scrollWidth <= chips.clientWidth + 2);
  }

  function pregunta(i) {
    if (busy) return; busy = true;
    var q = D.conversacion[i]; q._usada = true; pintarChips();
    bubble('in', q.pregunta);
    typing(espera(q.respuesta), function () {
      bubble('out', q.respuesta);
      if (q.tipo === 'derivar' || q.tipo === 'urgencia') { n.esc++; fila(MOTIVO[q.tipo], 'Aviso a tu equipo con el chat', 'Pasado a tu equipo', 'esc'); }
      else { n.ok++; fila(MOTIVO[q.tipo] || 'Información', q.pregunta, 'Respondido', 'ok'); }
      busy = false;
    });
  }

  function cita() {
    if (busy) return; busy = true;
    var c = D.cita_demo; D._citaHecha = true; pintarChips();
    bubble('in', c.pregunta);
    typing(espera(c.respuesta_intro), function () {
      var hs = huecos();
      var m = bubble('out', c.respuesta_intro, '<span class="msg-buttons">' + hs.map(function (h) { return '<button type="button">' + esc(h) + '</button>'; }).join('') + '</span>');
      busy = false;
      [].forEach.call(m.querySelectorAll('.msg-buttons button'), function (b) {
        b.onclick = function () {
          if (busy) return; busy = true;
          [].forEach.call(m.querySelectorAll('.msg-buttons button'), function (x) { x.disabled = true; });
          b.classList.add('tapped');
          var h = b.textContent;
          bubble('in', h);
          typing(900, function () {
            bubble('out', 'Perfecto. ¿A nombre de quién la reservo?');
            setTimeout(function () {
              bubble('in', 'Laura Gómez');
              typing(1200, function () {
                bubble('out', 'Listo, Laura: ' + c.servicio + ' ' + h + ' en ' + c.sede + '. Te mando un recordatorio por aquí el día antes y, si necesitas cambiarla, me escribes.');
                n.cita++; fila('Cita', c.servicio + ' · ' + c.sede, 'Cita reservada', 'cita');
                var card = document.getElementById('crmCard');
                card.hidden = false;
                card.querySelector('[data-k=servicio]').textContent = c.servicio;
                card.querySelector('[data-k=sede]').textContent = c.sede;
                card.querySelector('[data-k=cuando]').textContent = h;
                busy = false;
              });
            }, 900);
          });
        };
      });
    });
  }

  document.getElementById('phoneTime').textContent = hora();
  pintarChips();

  // Quién abre la demo (para avisar a Fabrizzio). No cuenta las pruebas propias.
  try {
    var qa = /[?&]qa\b/.test(location.search) || location.hostname === 'localhost' || location.hostname === '127.0.0.1' || navigator.webdriver;
    if (!qa && navigator.sendBeacon) {
      navigator.sendBeacon('https://gaia-relojes.onrender.com/gwb/lead', JSON.stringify({ site: 'zenia-demo', kind: 'demo', brand: D.nombre, path: location.pathname, ref: document.referrer || '' }));
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href*="wa.me"],a[href*="calendly.com"]');
      if (!a || qa) return;
      navigator.sendBeacon('https://gaia-relojes.onrender.com/gwb/lead', JSON.stringify({ site: 'zenia', src: 'demo', brand: D.nombre, path: location.pathname, ref: document.referrer || '' }));
    }, true);
  } catch (e) {}
})();
