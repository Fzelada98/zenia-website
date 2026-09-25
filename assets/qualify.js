/* Formulario de cualificación de Zenia (26-ago-2026, rehecho 25-sep-2026).
 *
 * Problema que resuelve: los leads llegaban por WhatsApp sin saber qué negocio
 * tenían ni qué querían automatizar. El mensaje precargado ya dice de qué
 * página vienen; esto añade los datos que de verdad cualifican.
 *
 * Es un único fichero inyectado en todo el sitio (HTML estático en GitHub
 * Pages, sin framework): intercepta el clic de cualquier enlace de WhatsApp,
 * abre un modal, y al enviar registra la cualificación y abre WhatsApp.
 *
 * 25-sep-2026, "primero capturar": con más tráfico, la mayoría abría el modal
 * y se iba, y quien llegaba a WhatsApp a menudo no pulsaba enviar. Ahora:
 *  - El contacto (WhatsApp o email) es OBLIGATORIO y se registra ANTES de
 *    abrir WhatsApp: el lead existe aunque nunca envíe el mensaje.
 *  - Más corto, para que el botón se vea en el móvil: la ciudad sale de la
 *    IP (gaia la geolocaliza) y el tamaño del equipo se pregunta en la llamada.
 *  - En inglés en las páginas en inglés (la home principal y los posts EN).
 *  - En ordenador no se lanza WhatsApp a ciegas (muchos no tienen WhatsApp
 *    Web abierto): se confirma la recepción y WhatsApp queda como opción.
 *  - Se registran también las llamadas reservadas en Calendly.
 *
 * Reglas heredadas de lo que ya funciona en Global Watch Buyers:
 *  - El botón flotante lleva data-directo y sigue abriendo WhatsApp de un
 *    toque: el formulario cualifica, nunca bloquea.
 *  - El botón final es <button>, no un enlace wa.me, para que el beacon de
 *    leads no cuente el mismo lead dos veces.
 *  - Encabezado fijo y scroll interno: en portátil el formulario no cabe
 *    entero y el título se perdía.
 */
(function () {
  "use strict";
  var ENDPOINT = "https://gaia-relojes.onrender.com/gwb/lead";
  var NUM = "34677612799";

  var TXT = {
    es: {
      titulo: "Cuéntanos de tu negocio",
      sub: "30 segundos y te respondemos en menos de 24 h.",
      sector: "¿Qué tipo de negocio tienes?",
      objetivo: "¿Qué te gustaría resolver primero?",
      nombre: "Tu nombre", nombrePh: "¿Cómo te llamamos?",
      contacto: "Tu WhatsApp o email", contactoPh: "+34 600 000 000 o tu@email.com",
      error: "Déjanos un WhatsApp o un email para poder responderte.",
      ctaMovil: "Enviar y abrir WhatsApp", ctaPc: "Enviar",
      confianza: "Sin compromiso · La primera llamada es gratis",
      alt: "Prefiero escribir directamente por WhatsApp",
      priv: "Usamos estos datos solo para responderte y preparar tu propuesta.",
      okTitulo: "¡Recibido{n}!",
      okTexto: "Te escribimos en menos de 24 h a {c}. Si quieres ir más rápido, escríbenos ya:",
      okWa: "Abrir WhatsApp", cerrar: "Cerrar",
      hola: "Hola, vengo de «{p}»", negocio: "Negocio",
      resolver: "Quiero resolver", soy: "Soy", contactoMsg: "Contacto",
      sectores: ["Restaurante", "Clínica", "Gimnasio", "Estética o peluquería",
        "Despacho o asesoría", "Inmobiliaria", "Tienda o ecommerce", "Academia",
        "Hotel", "Otro"],
      objetivos: ["Atender WhatsApp 24/7", "Conseguir más clientes",
        "Automatizar citas o reservas", "Recuperar clientes inactivos",
        "Ordenar el CRM", "Aún no lo sé"]
    },
    en: {
      titulo: "Tell us about your business",
      sub: "30 seconds, and we reply within 24 hours.",
      sector: "What kind of business is it?",
      objetivo: "What would you like to solve first?",
      nombre: "Your name", nombrePh: "What should we call you?",
      contacto: "Your WhatsApp or email", contactoPh: "+1 555 000 0000 or you@email.com",
      error: "Leave us a WhatsApp number or an email so we can reply.",
      ctaMovil: "Send and open WhatsApp", ctaPc: "Send",
      confianza: "No commitment · The first call is free",
      alt: "I'd rather message you directly on WhatsApp",
      priv: "We only use this to reply to you and prepare your proposal.",
      okTitulo: "Got it{n}!",
      okTexto: "We'll get back to you within 24 hours at {c}. Want to go faster? Message us now:",
      okWa: "Open WhatsApp", cerrar: "Close",
      hola: "Hi, I'm coming from «{p}»", negocio: "Business",
      resolver: "I want to solve", soy: "I'm", contactoMsg: "Contact",
      sectores: ["Restaurant", "Clinic", "Gym", "Beauty salon",
        "Law or accounting firm", "Real estate", "Retail or ecommerce", "Academy",
        "Hotel", "Other"],
      objetivos: ["Answer customers 24/7", "Get more clients",
        "Automate bookings", "Win back inactive clients",
        "Organize my CRM", "Not sure yet"]
    }
  };

  /* La home principal traduce en el navegador y cambia <html lang>, así que
   * el idioma se mira al abrir, no al cargar. */
  function idioma() {
    return /^en/i.test(document.documentElement.lang || "") ? "en" : "es";
  }

  /* Contexto de la página: el H1 ya dice vertical y ciudad. */
  function contexto() {
    var h1 = document.querySelector("h1");
    var t = (h1 ? h1.textContent : document.title) || "";
    return t.replace(/\s+/g, " ").split(/\s*[|·]\s*/)[0].trim().slice(0, 90);
  }

  function esMovil() {
    return (window.matchMedia && matchMedia("(pointer:coarse)").matches) ||
      window.innerWidth < 768;
  }

  function registrar(datos) {
    try {
      var base = { site: "zenia", path: location.pathname, ref: document.referrer || "" };
      for (var k in datos) base[k] = datos[k];
      var carga = JSON.stringify(base);
      if (navigator.sendBeacon) navigator.sendBeacon(ENDPOINT, carga);
      else fetch(ENDPOINT, { method: "POST", body: carga, keepalive: true });
    } catch (e) { /* nunca bloquear al usuario por un fallo de registro */ }
  }

  var css = [
    ".zq-fondo{position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,.8);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;padding:12px}",
    ".zq-panel{width:100%;max-width:640px;max-height:92dvh;display:flex;flex-direction:column;background:#0d1117;border:1px solid rgba(255,255,255,.12);border-radius:16px;overflow:hidden;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;box-shadow:0 24px 60px rgba(0,0,0,.6)}",
    ".zq-head{display:flex;gap:14px;align-items:flex-start;padding:20px 22px 16px;border-bottom:1px solid rgba(255,255,255,.1);flex-shrink:0}",
    ".zq-head h2{margin:0;color:#F1F5F9;font-size:1.15rem;line-height:1.35;font-weight:700}",
    ".zq-head p{margin:6px 0 0;color:#94A3B8;font-size:.88rem;line-height:1.45}",
    ".zq-x{flex-shrink:0;width:34px;height:34px;border-radius:50%;border:0;background:rgba(255,255,255,.1);color:#fff;font-size:20px;line-height:1;cursor:pointer}",
    ".zq-x:hover{background:rgba(255,255,255,.2)}",
    ".zq-body{overflow-y:auto;overscroll-behavior:contain;padding:20px 22px 24px}",
    ".zq-lbl{display:block;color:#94A3B8;font-size:.85rem;margin:0 0 10px}",
    ".zq-grp{margin-bottom:20px}",
    ".zq-chips{display:flex;flex-wrap:wrap;gap:8px}",
    ".zq-chip{padding:9px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.16);background:transparent;color:#CBD5E1;font-size:.87rem;cursor:pointer;font-family:inherit}",
    ".zq-chip:hover{border-color:rgba(255,255,255,.4)}",
    ".zq-chip.on{background:#2563EB;border-color:#2563EB;color:#fff;font-weight:600}",
    ".zq-inp{width:100%;box-sizing:border-box;background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.16);border-radius:10px;padding:12px 14px;color:#F1F5F9;font-size:16px;font-family:inherit}",
    ".zq-inp:focus{outline:none;border-color:#2563EB}",
    ".zq-inp.mal{border-color:#F87171}",
    ".zq-inp::placeholder{color:#64748B}",
    ".zq-err{color:#FCA5A5;font-size:.82rem;margin:8px 0 0;display:none}",
    ".zq-cta{width:100%;margin-top:8px;padding:15px;border:0;border-radius:999px;background:#25D366;color:#062e16;font-size:1.02rem;font-weight:700;cursor:pointer;font-family:inherit}",
    ".zq-cta:hover{filter:brightness(1.07)}",
    ".zq-cta:disabled{opacity:.6;cursor:default}",
    ".zq-alt{display:block;text-align:center;margin-top:14px;color:#94A3B8;font-size:.85rem;text-decoration:underline;text-underline-offset:4px}",
    ".zq-priv{color:#64748B;font-size:.76rem;text-align:center;margin:14px 0 0;line-height:1.5}",
    ".zq-conf{color:#94A3B8;font-size:.82rem;text-align:center;margin:12px 0 0}",
    ".zq-ok{text-align:center;padding:12px 4px 4px}",
    ".zq-ok .zq-tick{width:56px;height:56px;margin:0 auto 16px;border-radius:50%;background:rgba(37,211,102,.14);color:#25D366;font-size:28px;line-height:56px}",
    ".zq-ok h2{color:#F1F5F9;font-size:1.3rem;margin:0 0 10px}",
    ".zq-ok p{color:#94A3B8;font-size:.95rem;line-height:1.55;margin:0 0 20px}",
    ".zq-sec{display:block;width:100%;margin-top:10px;padding:13px;border-radius:999px;border:1px solid rgba(255,255,255,.16);background:transparent;color:#CBD5E1;font-size:.95rem;cursor:pointer;font-family:inherit}"
  ].join("");

  var abierto = false;

  function abrir(hrefOriginal) {
    if (abierto) return;
    abierto = true;
    var T = TXT[idioma()];
    var ctx = contexto();
    var estado = { sector: "", objetivo: "", nombre: "", contacto: "" };

    var st = document.createElement("style");
    st.textContent = css;
    document.head.appendChild(st);

    var fondo = document.createElement("div");
    fondo.className = "zq-fondo";
    fondo.setAttribute("role", "dialog");
    fondo.setAttribute("aria-modal", "true");

    function grupo(titulo, opciones, campo) {
      var d = document.createElement("div");
      d.className = "zq-grp";
      var l = document.createElement("span");
      l.className = "zq-lbl";
      l.textContent = titulo;
      d.appendChild(l);
      var c = document.createElement("div");
      c.className = "zq-chips";
      opciones.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "zq-chip";
        b.textContent = o;
        b.onclick = function () {
          var ya = estado[campo] === o;
          estado[campo] = ya ? "" : o;
          Array.prototype.forEach.call(c.children, function (x) {
            x.className = "zq-chip" + (x.textContent === estado[campo] ? " on" : "");
          });
        };
        c.appendChild(b);
      });
      d.appendChild(c);
      return d;
    }

    function texto(titulo, ph, campo, tipo) {
      var d = document.createElement("div");
      d.className = "zq-grp";
      var l = document.createElement("label");
      l.className = "zq-lbl";
      l.textContent = titulo;
      var i = document.createElement("input");
      i.className = "zq-inp";
      i.placeholder = ph;
      if (tipo) i.setAttribute("autocomplete", tipo);
      i.oninput = function () {
        estado[campo] = i.value.slice(0, 80);
        i.classList.remove("mal");
        if (err) err.style.display = "none";
      };
      l.appendChild(i);
      d.appendChild(l);
      return { caja: d, input: i };
    }

    var panel = document.createElement("div");
    panel.className = "zq-panel";

    var head = document.createElement("div");
    head.className = "zq-head";
    var cab = document.createElement("div");
    cab.style.cssText = "min-width:0;flex:1";
    var h2 = document.createElement("h2");
    h2.textContent = T.titulo;
    var sub = document.createElement("p");
    sub.textContent = T.sub;
    cab.appendChild(h2); cab.appendChild(sub);
    head.appendChild(cab);
    var x = document.createElement("button");
    x.className = "zq-x"; x.type = "button"; x.setAttribute("aria-label", T.cerrar);
    x.textContent = "×";
    x.onclick = cerrar;
    head.appendChild(x);

    var body = document.createElement("div");
    body.className = "zq-body";
    body.appendChild(grupo(T.sector, T.sectores, "sector"));
    body.appendChild(grupo(T.objetivo, T.objetivos, "objetivo"));
    body.appendChild(texto(T.nombre, T.nombrePh, "nombre", "name").caja);
    /* Contacto (7-sep-2026, obligatorio desde 25-sep): leads con nombre
     * abrieron WhatsApp y nunca pulsaron enviar; sin su número o email se
     * perdieron. Con esto el aviso lleva cómo contactarles siempre. */
    var campoContacto = texto(T.contacto, T.contactoPh, "contacto", "tel");
    var err = document.createElement("p");
    err.className = "zq-err";
    err.textContent = T.error;
    campoContacto.caja.appendChild(err);
    body.appendChild(campoContacto.caja);

    var movil = esMovil();
    var cta = document.createElement("button");
    cta.type = "button";
    cta.className = "zq-cta";
    cta.textContent = movil ? T.ctaMovil : T.ctaPc;
    cta.onclick = enviar;
    body.appendChild(cta);

    var conf = document.createElement("p");
    conf.className = "zq-conf";
    conf.textContent = T.confianza;
    body.appendChild(conf);

    var alt = document.createElement("a");
    alt.className = "zq-alt";
    alt.href = hrefOriginal;
    alt.target = "_blank";
    alt.rel = "noopener";
    alt.textContent = T.alt;
    alt.onclick = function () { setTimeout(cerrar, 100); };
    body.appendChild(alt);

    var priv = document.createElement("p");
    priv.className = "zq-priv";
    priv.textContent = T.priv;
    body.appendChild(priv);

    panel.appendChild(head); panel.appendChild(body); fondo.appendChild(panel);
    fondo.onclick = function (e) { if (e.target === fondo) cerrar(); };
    document.addEventListener("keydown", onEsc, true);
    var scrollPrevio = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    document.body.appendChild(fondo);

    function onEsc(e) { if (e.key === "Escape") cerrar(); }

    function cerrar() {
      abierto = false;
      document.removeEventListener("keydown", onEsc, true);
      document.body.style.overflow = scrollPrevio;
      if (fondo.parentNode) fondo.parentNode.removeChild(fondo);
      if (st.parentNode) st.parentNode.removeChild(st);
    }

    function contactoValido(v) {
      v = (v || "").trim();
      return /\S+@\S+\.\S+/.test(v) || v.replace(/\D/g, "").length >= 7;
    }

    function enviar() {
      if (cta.disabled) return;
      if (!contactoValido(estado.contacto)) {
        campoContacto.input.classList.add("mal");
        err.style.display = "block";
        campoContacto.input.focus();
        return;
      }
      cta.disabled = true;
      var l = [T.hola.replace("{p}", ctx)];
      if (estado.sector) l.push(T.negocio + ": " + estado.sector);
      if (estado.objetivo) l.push(T.resolver + ": " + estado.objetivo);
      if (estado.nombre) l.push(T.soy + " " + estado.nombre.trim());
      l.push(T.contactoMsg + ": " + estado.contacto.trim());
      var url = "https://wa.me/" + NUM + "?text=" + encodeURIComponent(l.join("\n"));
      // En móvil, abrir ANTES de la petición: si se abre después, Safari e iOS
      // lo bloquean por no venir de un gesto directo del usuario.
      if (movil) {
        // Sin "noopener" en la llamada: con él window.open devuelve SIEMPRE
        // null y el código de respaldo mandaba también esta pestaña a WhatsApp.
        var win = window.open(url, "_blank");
        if (win) { try { win.opener = null; } catch (e) {} }
        else setTimeout(function () { location.href = url; }, 150);
      }
      registrar({
        kind: "qualify", brand: estado.sector, model: estado.objetivo,
        name: estado.nombre.trim(),
        contact: estado.contacto.trim(), locale: idioma(), year: ctx.slice(0, 30)
      });
      if (window.gtag) try { gtag("event", "generate_lead", { method: "qualify" }); } catch (e) {}
      confirmar(url);
    }

    /* Pantalla de confirmación: quien vuelve de WhatsApp sin haber enviado
     * sabe que igualmente le vamos a escribir. */
    function confirmar(url) {
      var nombre = estado.nombre.trim().split(" ")[0];
      head.style.display = "none";
      body.innerHTML = "";
      var ok = document.createElement("div");
      ok.className = "zq-ok";
      var tick = document.createElement("div");
      tick.className = "zq-tick";
      tick.textContent = "✓";
      var t = document.createElement("h2");
      t.textContent = T.okTitulo.replace("{n}", nombre ? ", " + nombre : "");
      var p = document.createElement("p");
      p.textContent = T.okTexto.replace("{c}", estado.contacto.trim());
      var wa = document.createElement("button");
      wa.type = "button";
      wa.className = "zq-cta";
      wa.textContent = T.okWa;
      wa.onclick = function () {
        var w = window.open(url, "_blank");
        if (w) { try { w.opener = null; } catch (e) {} } else location.href = url;
      };
      var c = document.createElement("button");
      c.type = "button";
      c.className = "zq-sec";
      c.textContent = T.cerrar;
      c.onclick = cerrar;
      ok.appendChild(tick); ok.appendChild(t); ok.appendChild(p);
      ok.appendChild(wa); ok.appendChild(c);
      body.appendChild(ok);
    }
  }


  /* El banner de cookies (#cookieBanner, z-index 9999, fijo abajo y a todo lo
   * ancho) quedaba POR ENCIMA del botón flotante de WhatsApp (z-index 9998):
   * mientras el banner estaba visible el botón no se podía pulsar. Aquí se
   * sube el botón por encima del banner mientras haga falta. */
  var origBottom = null, origZ = null;
  function ajustarFlotante() {
    var b = document.querySelector('a[aria-label="Contactar por WhatsApp"], a[data-directo][href*="wa.me"]');
    var banner = document.getElementById("cookieBanner");
    if (!b) return;
    // OJO: el botón trae su posición en estilos EN LÍNEA (bottom:24px;
    // z-index:9998). Hay que guardarlos y restaurar ESOS valores; poner
    // style.bottom="" los borra y el botón se va fuera de la pantalla.
    if (origBottom === null) {
      origBottom = b.style.bottom || "24px";
      origZ = b.style.zIndex || "9998";
    }
    // OJO: no vale offsetParent para saber si se ve — en elementos
    // position:fixed SIEMPRE es null, visibles o no. Se mira el rectángulo.
    var visible = false;
    if (banner) {
      var cb = getComputedStyle(banner);
      visible = cb.display !== "none" && cb.visibility !== "hidden" &&
        cb.opacity !== "0" && banner.getBoundingClientRect().height > 1;
    }
    if (visible) {
      var alto = banner.getBoundingClientRect().height || 65;
      b.style.bottom = Math.round(alto + 16) + "px";
      b.style.zIndex = "10000";
    } else {
      b.style.bottom = origBottom;
      b.style.zIndex = origZ;
    }
  }
  document.addEventListener("DOMContentLoaded", ajustarFlotante);
  ajustarFlotante();
  // El banner se cierra por JS de la propia página: revisar unas cuantas veces
  // en vez de observar, que es más simple y no deja observadores colgando.
  var reintentos = 0;
  var vigilante = setInterval(function () {
    ajustarFlotante();
    if (++reintentos > 20) clearInterval(vigilante);
  }, 700);


  /* Llamadas reservadas en Calendly (25-sep-2026): hasta ahora solo las veía
   * Calendly por correo; el sistema de leads no sabía de qué página venían. */
  window.addEventListener("message", function (e) {
    if (!/calendly\.com$/.test((e.origin || "").split("://")[1] || "")) return;
    var d = e.data;
    if (!d || d.event !== "calendly.event_scheduled") return;
    var inicio = "";
    try { inicio = d.payload.event.start_time || ""; } catch (err) {}
    registrar({ kind: "calendly", model: inicio ? "Llamada " + inicio.slice(0, 16).replace("T", " ") : "Llamada reservada",
      locale: idioma(), year: contexto().slice(0, 30) });
  });


  /* Registrar también los clics en el correo. El beacon original solo miraba
   * `a[href*="wa.me"]`, así que quien escribía a fabrizzio.zelada@zeniapartners.com
   * (publicado en 405 páginas) era INVISIBLE: llegó un lead real el 25-ago
   * (Veterinaria Rondón) y no había forma de saber de qué página venía.
   * Aquí no se abre formulario: se deja pasar el mailto y solo se anota. */
  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var a = t.closest('a[href^="mailto:"]');
    if (!a) return;
    try {
      var h1 = document.querySelector("h1");
      navigator.sendBeacon(ENDPOINT, JSON.stringify({
        site: "zenia", path: location.pathname, ref: document.referrer || "",
        kind: "email",
        year: ((h1 ? h1.textContent : document.title) || "")
          .replace(/\s+/g, " ").split(/\s*[|·:]\s*/)[0].trim().slice(0, 60)
      }));
    } catch (err) { /* nunca estorbar al usuario */ }
  }, true);

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var a = t.closest('a[href*="wa.me"]');
    if (!a) return;
    // El botón flotante es la vía rápida y NO cualifica... salvo en páginas
    // donde es el único enlace de WhatsApp (home, índice del blog): allí sin
    // esto no habría forma de cualificar a nadie. La salida sin fricción sigue
    // existiendo dentro del propio modal.
    if (a.hasAttribute("data-directo") || a.getAttribute("aria-label") === "Contactar por WhatsApp") {
      var otros = document.querySelectorAll(
        'a[href*="wa.me"]:not([data-directo]):not([aria-label="Contactar por WhatsApp"])');
      if (otros.length > 0) return;
    }
    if (a.classList.contains("zq-alt")) return;          // salida directa del modal
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
    e.preventDefault();
    abrir(a.href);
  }, true);
})();
