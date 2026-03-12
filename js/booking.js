// ZENIA — Booking Modal & Calendly Integration

var bookingStep = 1;
var zeniaCallScheduled = null;
var calendlyLoaded = false;

// Lazy-load Calendly widget on first modal open
function loadCalendly() {
  if (calendlyLoaded) return;
  calendlyLoaded = true;
  var s = document.createElement('script');
  s.src = 'https://assets.calendly.com/assets/external/widget.js';
  s.async = true;
  document.body.appendChild(s);
}

function openCalendly(e) {
  e.preventDefault();
  loadCalendly();
  bookingStep = 1;
  showStep(1);
  document.getElementById('bookingModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeBooking() {
  var modal = document.getElementById('bookingModal');
  modal.classList.remove('active');
  document.body.style.overflow = '';
  setTimeout(function() {
    document.getElementById('bookingForm').reset();
    showStep(1);
  }, 350);
}

function showStep(step) {
  bookingStep = step;
  var steps = [
    document.getElementById('bookingStep1'),
    document.getElementById('bookingStep2'),
    document.getElementById('bookingStep3')
  ];
  steps.forEach(function(s, i) {
    if (i + 1 === step) {
      s.classList.remove('hidden');
      s.classList.add('active');
    } else {
      s.classList.add('hidden');
      s.classList.remove('active');
    }
  });
  var progress = step === 1 ? 50 : step === 2 ? 80 : 100;
  document.getElementById('bookingProgress').style.width = progress + '%';

  if (currentLang === 'es') translateForm();
}

function translateForm() {
  var t = {
    formTitle: 'Ayudanos a preparar tu sesion',
    formDesc: 'Unas preguntas rapidas para aprovechar al maximo tu tiempo',
    labelCompany: 'Nombre de la empresa',
    labelSize: 'Tama\u00f1o de la empresa',
    labelArea: '\u00bfQue area te gustaria mejorar mas?',
    labelOnline: 'Tu presencia online principal',
    optSizeDefault: 'Seleccionar...',
    optSize1: '1-10 empleados',
    optSize2: '10-50 empleados',
    optSize3: '50-200 empleados',
    optSize4: '200+ empleados',
    optAreaDefault: 'Seleccionar...',
    optArea1: 'Ventas',
    optArea2: 'Atencion al Cliente',
    optArea3: 'Operaciones',
    optArea4: 'Productividad Interna',
    optArea5: 'No estoy seguro',
    companyUrl: 'Ingresa tu URL',
    formSubmitBtn: 'Confirmar Reserva',
    noticeText: 'Prepararemos un breve analisis de oportunidades AI para tu empresa antes de la llamada.',
    confirmTitle: '\u00a1Todo listo!',
    confirmDesc: 'Analizaremos tu empresa antes de la llamada y llegaremos preparados con oportunidades AI personalizadas para tu negocio.',
    confirmCloseBtn: 'Cerrar'
  };
  Object.keys(t).forEach(function(id) {
    var el = document.getElementById(id);
    if (el) {
      if (el.tagName === 'INPUT') el.placeholder = t[id];
      else if (el.tagName === 'OPTION') el.textContent = t[id];
      else if (id === 'labelOnline') el.innerHTML = t[id] + ' <span style="font-weight:400;color:var(--text-muted)">(web, Instagram, LinkedIn, etc.)</span>';
      else el.textContent = t[id];
    }
  });
}

function submitBookingForm(e) {
  e.preventDefault();
  var data = {
    company: document.getElementById('companyName').value,
    size: document.getElementById('companySize').value,
    area: document.getElementById('companyArea').value,
    onlinePresence: document.getElementById('companyUrl').value || '',
    callScheduled: zeniaCallScheduled,
    timestamp: new Date().toISOString()
  };

  // Store locally as backup
  var bookings = JSON.parse(localStorage.getItem('zenia-bookings') || '[]');
  bookings.push(data);
  localStorage.setItem('zenia-bookings', JSON.stringify(bookings));

  // Send to ZENIA Research Agent backend
  var WEBHOOK_URL = window.ZENIA_WEBHOOK_URL || 'https://zenia-backend-y6hp.onrender.com/webhook/booking';
  fetch(WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(function(r) {
    console.log('Briefing generation triggered for:', data.company);
  }).catch(function(err) {
    console.warn('Webhook not reachable, data saved locally:', err.message);
  });

  showStep(3);
}

// Listen for Calendly events
window.addEventListener('message', function(e) {
  var data = e.data;
  if (typeof data === 'string') {
    try { data = JSON.parse(data); } catch(err) { return; }
  }
  if (!data || !data.event) return;
  if (data.event === 'calendly.event_scheduled') {
    if (data.payload && data.payload.event && data.payload.event.start_time) {
      zeniaCallScheduled = data.payload.event.start_time;
    }
    showStep(2);
  }
});

// Close modal on Escape
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeBooking();
});

// Expose for inline onclick handlers
window.openCalendly = openCalendly;
window.closeBooking = closeBooking;
window.showStep = showStep;
window.submitBookingForm = submitBookingForm;
