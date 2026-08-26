/* Formulario de cualificación de Zenia (26-ago-2026).
 *
 * Problema que resuelve: los leads llegaban por WhatsApp sin saber qué negocio
 * tenían ni qué querían automatizar. El mensaje precargado ya dice de qué
 * página vienen; esto añade los datos que de verdad cualifican.
 *
 * Es un único fichero inyectado en todo el sitio (HTML estático en GitHub
 * Pages, sin framework): intercepta el clic de cualquier enlace de WhatsApp,
 * abre un modal, y al enviar compone el mensaje y registra la cualificación.
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

  var SECTORES = ["Restaurante", "Clínica", "Gimnasio", "Estética o peluquería",
    "Despacho o asesoría", "Inmobiliaria", "Tienda o ecommerce", "Academia",
    "Hotel", "Otro"];
  var OBJETIVOS = ["Atender WhatsApp 24/7", "Conseguir más clientes",
    "Automatizar citas o reservas", "Recuperar clientes inactivos",
    "Ordenar el CRM", "Aún no lo sé"];
  var TAMANOS = ["Solo yo", "2-5 personas", "6-20 personas", "Más de 20"];

  /* Contexto de la página: el H1 ya dice vertical y ciudad. */
  function contexto() {
    var h1 = document.querySelector("h1");
    var t = (h1 ? h1.textContent : document.title) || "";
    return t.replace(/\s+/g, " ").split(/\s*[|·]\s*/)[0].trim().slice(0, 90);
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
    ".zq-inp{width:100%;box-sizing:border-box;background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.16);border-radius:10px;padding:12px 14px;color:#F1F5F9;font-size:.95rem;font-family:inherit}",
    ".zq-inp:focus{outline:none;border-color:#2563EB}",
    ".zq-inp::placeholder{color:#64748B}",
    ".zq-cta{width:100%;margin-top:8px;padding:15px;border:0;border-radius:999px;background:#25D366;color:#062e16;font-size:1.02rem;font-weight:700;cursor:pointer;font-family:inherit}",
    ".zq-cta:hover{filter:brightness(1.07)}",
    ".zq-cta:disabled{opacity:.6;cursor:default}",
    ".zq-alt{display:block;text-align:center;margin-top:14px;color:#94A3B8;font-size:.85rem;text-decoration:underline;text-underline-offset:4px}",
    ".zq-priv{color:#64748B;font-size:.76rem;text-align:center;margin:14px 0 0;line-height:1.5}",
  ].join("");

  var abierto = false;

  function abrir(hrefOriginal) {
    if (abierto) return;
    abierto = true;
    var ctx = contexto();
    var estado = { sector: "", objetivo: "", tamano: "", ciudad: "", nombre: "" };

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

    function texto(titulo, ph, campo) {
      var d = document.createElement("div");
      d.className = "zq-grp";
      var l = document.createElement("span");
      l.className = "zq-lbl";
      l.textContent = titulo;
      var i = document.createElement("input");
      i.className = "zq-inp";
      i.placeholder = ph;
      i.oninput = function () { estado[campo] = i.value.slice(0, 60); };
      d.appendChild(l); d.appendChild(i);
      return d;
    }

    var panel = document.createElement("div");
    panel.className = "zq-panel";

    var head = document.createElement("div");
    head.className = "zq-head";
    head.innerHTML =
      '<div style="min-width:0;flex:1"><h2>Cuéntanos de tu negocio</h2>' +
      '<p>30 segundos. Con esto preparamos la propuesta antes de hablar.</p></div>';
    var x = document.createElement("button");
    x.className = "zq-x"; x.type = "button"; x.setAttribute("aria-label", "Cerrar");
    x.textContent = "×";
    x.onclick = cerrar;
    head.appendChild(x);

    var body = document.createElement("div");
    body.className = "zq-body";
    body.appendChild(grupo("¿Qué tipo de negocio tienes?", SECTORES, "sector"));
    body.appendChild(grupo("¿Qué te gustaría resolver primero?", OBJETIVOS, "objetivo"));
    body.appendChild(grupo("¿Cuántos sois?", TAMANOS, "tamano"));
    body.appendChild(texto("¿En qué ciudad?", "Ej.: Lima, Madrid, Bogotá", "ciudad"));
    body.appendChild(texto("Tu nombre", "¿Cómo te llamamos?", "nombre"));

    var cta = document.createElement("button");
    cta.type = "button";
    cta.className = "zq-cta";
    cta.textContent = "Continuar por WhatsApp";
    cta.onclick = enviar;
    body.appendChild(cta);

    var alt = document.createElement("a");
    alt.className = "zq-alt";
    alt.href = hrefOriginal;
    alt.target = "_blank";
    alt.rel = "noopener";
    
    alt.textContent = "Prefiero escribir directamente";
    alt.onclick = function () { setTimeout(cerrar, 100); };
    body.appendChild(alt);

    var priv = document.createElement("p");
    priv.className = "zq-priv";
    priv.textContent = "Usamos estos datos solo para preparar tu propuesta y responderte por WhatsApp. No los vendemos ni los publicamos.";
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

    function enviar() {
      if (cta.disabled) return;
      cta.disabled = true;
      cta.textContent = "Abriendo WhatsApp…";
      var l = ["Hola, vengo de «" + ctx + "»"];
      if (estado.sector) l.push("Negocio: " + estado.sector);
      if (estado.ciudad) l.push("Ciudad: " + estado.ciudad);
      if (estado.tamano) l.push("Equipo: " + estado.tamano);
      if (estado.objetivo) l.push("Quiero resolver: " + estado.objetivo);
      if (estado.nombre) l.push("Soy " + estado.nombre);
      var url = "https://wa.me/" + NUM + "?text=" + encodeURIComponent(l.join("\n"));
      // Abrir ANTES de la petición: si se abre después, Safari e iOS lo bloquean
      // por no venir de un gesto directo del usuario.
      var win = window.open(url, "_blank", "noopener");
      try {
        var carga = JSON.stringify({
          site: "zenia", path: location.pathname, ref: document.referrer || "",
          kind: "qualify", brand: estado.sector, city: estado.ciudad,
          model: estado.objetivo, condition: estado.tamano, name: estado.nombre,
          year: ctx.slice(0, 30)
        });
        if (navigator.sendBeacon) navigator.sendBeacon(ENDPOINT, carga);
        else fetch(ENDPOINT, { method: "POST", body: carga, keepalive: true });
      } catch (e) { /* nunca bloquear al usuario por un fallo de registro */ }
      if (!win) location.href = url;
      cerrar();
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
