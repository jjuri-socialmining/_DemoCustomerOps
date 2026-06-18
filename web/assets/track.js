/* ─────────────────────────────────────────────────────────────────────────────
   SIGMA · Tracker universal de visitas
   Incrústalo en CUALQUIER página con:  <script src="assets/track.js"></script>
   (ajusta la ruta según la carpeta de la página).

   Registra automáticamente:
     • "pageview" → cada vez que alguien ENTRA a una página (qué link usan).
     • "click"    → cada click en un <a> o [data-track] (qué les llama la atención).

   Guarda cada evento en una colección de JSONBin. Una sola configuración aquí.
   Seguridad: CREATE_KEY es una Access Key con permiso SOLO "Bin Create".
   Guía: tools/visit-tracker/SETUP.md
   ───────────────────────────────────────────────────────────────────────────── */
(function () {
  "use strict";

  /* ════════════════════ CONFIG — EDITA ESTO (una sola vez) ═══════════════════ */
  var CONFIG = {
    COLLECTION_ID: "6a32d727da38895dfed1c6c9",
    CREATE_KEY:    "$2a$10$GZXDddQfBmo1UmmKj/Tmwe.agDHu7gfjGGbSIbTJg4iAceXFiXxYm",
    GEO_TIMEOUT_MS: 4000,
    TRACK_CLICKS: true            // false = solo cuenta visitas, no clicks
  };
  /* ═══════════════════════════════════════════════════════════════════════════ */

  var API = "https://api.jsonbin.io/v3/b";

  /* ---------- visitor id persistente (detecta retornos) ---------- */
  function getVisitor() {
    var k = "__sigma_vid";
    try {
      var id = localStorage.getItem(k);
      var n = parseInt(localStorage.getItem(k + "_n") || "0", 10) + 1;
      if (!id) id = "v_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 8);
      localStorage.setItem(k, id);
      localStorage.setItem(k + "_n", String(n));
      return { id: id, visit_count: n, returning: n > 1 };
    } catch (e) {
      return { id: "v_anon_" + Math.random().toString(36).slice(2, 8), visit_count: 1, returning: false };
    }
  }

  /* ---------- dispositivo / SO / navegador ---------- */
  function parseUA() {
    var ua = navigator.userAgent || "", plat = navigator.platform || "", maxTouch = navigator.maxTouchPoints || 0;
    var os = "Desconocido";
    if (/windows phone/i.test(ua)) os = "Windows Phone";
    else if (/win/i.test(plat) || /windows/i.test(ua)) os = "Windows";
    else if (/android/i.test(ua)) os = "Android";
    else if (/iphone|ipod/i.test(ua)) os = "iOS";
    else if (/ipad|macintosh/i.test(ua) && maxTouch > 1) os = "iPadOS";
    else if (/iphone|ipad/i.test(ua)) os = "iOS";
    else if (/mac/i.test(plat) || /mac os x/i.test(ua)) os = "macOS";
    else if (/cros/i.test(ua)) os = "ChromeOS";
    else if (/linux/i.test(plat) || /linux/i.test(ua)) os = "Linux";

    var isTablet = /ipad/i.test(ua) || (/android/i.test(ua) && !/mobile/i.test(ua)) || os === "iPadOS";
    var isMobile = /mobi|iphone|ipod|android.*mobile|windows phone/i.test(ua);
    var deviceType = isTablet ? "Tablet" : (isMobile ? "Celular" : "PC");

    var label;
    if (deviceType === "Celular") label = os === "iOS" ? "iPhone" : "Celular (" + os + ")";
    else if (deviceType === "Tablet") label = (os === "iOS" || os === "iPadOS") ? "iPad" : "Tablet (" + os + ")";
    else label = os === "macOS" ? "Mac" : (os === "Windows" ? "PC (Windows)" : "PC (" + os + ")");

    var browser = "Desconocido", ver = "";
    function m(re) { var x = ua.match(re); return x ? x[1] : ""; }
    if (/edg\//i.test(ua)) { browser = "Edge"; ver = m(/edg\/([\d.]+)/i); }
    else if (/opr\/|opera/i.test(ua)) { browser = "Opera"; ver = m(/(?:opr|opera)[\/ ]([\d.]+)/i); }
    else if (/samsungbrowser/i.test(ua)) { browser = "Samsung Internet"; ver = m(/samsungbrowser\/([\d.]+)/i); }
    else if (/firefox|fxios/i.test(ua)) { browser = "Firefox"; ver = m(/(?:firefox|fxios)\/([\d.]+)/i); }
    else if (/chrome|crios/i.test(ua)) { browser = "Chrome"; ver = m(/(?:chrome|crios)\/([\d.]+)/i); }
    else if (/safari/i.test(ua)) { browser = "Safari"; ver = m(/version\/([\d.]+)/i); }

    return { os: os, device_type: deviceType, device_label: label,
             browser: browser, browser_version: ver, user_agent: ua, platform: plat };
  }

  /* ---------- UTM / query ---------- */
  function getParams() {
    var out = {}, q;
    try { q = new URLSearchParams(location.search); } catch (e) { return { raw_query: location.search }; }
    ["utm_source","utm_medium","utm_campaign","utm_term","utm_content","ref","gclid","fbclid"]
      .forEach(function (k) { var v = q.get(k); if (v) out[k] = v; });
    out.raw_query = location.search || "";
    return out;
  }

  /* ---------- datos de navegador ---------- */
  function browserData() {
    var nav = navigator, scr = screen || {};
    var conn = nav.connection || nav.mozConnection || nav.webkitConnection || {};
    return {
      languages: nav.languages || [nav.language], language: nav.language || "",
      timezone: (function () { try { return Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) { return ""; } })(),
      tz_offset_min: new Date().getTimezoneOffset(),
      screen: (scr.width || 0) + "x" + (scr.height || 0),
      viewport: (window.innerWidth || 0) + "x" + (window.innerHeight || 0),
      pixel_ratio: window.devicePixelRatio || 1, color_depth: scr.colorDepth || null,
      cpu_cores: nav.hardwareConcurrency || null, device_memory_gb: nav.deviceMemory || null,
      touch_points: nav.maxTouchPoints || 0,
      net_type: conn.effectiveType || null, net_downlink: conn.downlink || null, net_rtt: conn.rtt || null,
      do_not_track: nav.doNotTrack || window.doNotTrack || null, cookies_enabled: nav.cookieEnabled,
      referrer: document.referrer || "(directo)"
    };
  }

  /* ---------- geolocalización por IP (una vez, cacheada) ---------- */
  function fetchGeo() {
    function withTimeout(p) {
      return Promise.race([p, new Promise(function (_, rej) {
        setTimeout(function () { rej(new Error("timeout")); }, CONFIG.GEO_TIMEOUT_MS);
      })]);
    }
    return withTimeout(fetch("https://ipwho.is/").then(function (r) { return r.json(); }))
      .then(function (j) {
        if (!j || j.success === false) throw new Error("ipwho fail");
        return { ip: j.ip, ip_type: j.type, country: j.country, country_code: j.country_code,
          region: j.region, city: j.city, postal: j.postal, latitude: j.latitude, longitude: j.longitude,
          isp: (j.connection && j.connection.isp) || null, org: (j.connection && j.connection.org) || null,
          asn: (j.connection && j.connection.asn) || null,
          geo_timezone: (j.timezone && j.timezone.id) || null, geo_source: "ipwho.is" };
      })
      .catch(function () {
        return withTimeout(fetch("https://ipapi.co/json/").then(function (r) { return r.json(); }))
          .then(function (j) {
            return { ip: j.ip, country: j.country_name, country_code: j.country_code, region: j.region,
              city: j.city, postal: j.postal, latitude: j.latitude, longitude: j.longitude,
              isp: j.org || null, org: j.org || null, asn: j.asn || null,
              geo_timezone: j.timezone || null, geo_source: "ipapi.co" };
          })
          .catch(function () { return { geo_source: "unavailable" }; });
      });
  }

  /* ---------- info de la página actual ---------- */
  function pageInfo() {
    return { page: location.pathname, page_title: document.title || "(sin título)", page_url: location.href };
  }

  /* ---------- POST a JSONBin (un evento = un bin) ---------- */
  function postBin(payload) {
    if (!CONFIG.COLLECTION_ID || /PEGA_AQUI/.test(CONFIG.COLLECTION_ID) ||
        !CONFIG.CREATE_KEY || /PEGA_AQUI/.test(CONFIG.CREATE_KEY)) {
      console.warn("[track] Sin configurar — evento no enviado:", payload.event_type, payload.page);
      return Promise.resolve(false);
    }
    return fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Access-Key": CONFIG.CREATE_KEY,
                 "X-Collection-Id": CONFIG.COLLECTION_ID, "X-Bin-Private": "true" },
      body: JSON.stringify(payload), keepalive: true
    }).then(function (r) { return r.ok; }).catch(function () { return false; });
  }

  /* ---------- bandeja de salida (outbox) en localStorage ----------
     Garantiza que ningún evento se pierda: si un click navega antes de
     enviarse, queda guardado y se manda al cargar la próxima página.
     Cada evento se envía EXACTAMENTE una vez (se quita sólo al confirmar). */
  var OUTBOX = "__sigma_outbox";
  function obRead() { try { return JSON.parse(localStorage.getItem(OUTBOX) || "[]"); } catch (e) { return []; } }
  function obWrite(a) { try { localStorage.setItem(OUTBOX, JSON.stringify(a.slice(-200))); } catch (e) {} }
  function enqueue(payload) {
    var eid = "e_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 8);
    var a = obRead(); a.push({ eid: eid, payload: payload }); obWrite(a);
    return eid;
  }
  function dequeue(eid) { obWrite(obRead().filter(function (it) { return it.eid !== eid; })); }
  function trySend(item) {
    return postBin(item.payload).then(function (ok) { if (ok) dequeue(item.eid); return ok; });
  }
  function flushOutbox() { return Promise.all(obRead().map(trySend)); }

  /* ---------- estado compartido por página ---------- */
  var visitor = getVisitor(), dev = parseUA(), brw = browserData();
  var geoCache = null;
  var geoPromise = fetchGeo().then(function (g) { geoCache = g; return g; });  // UNA sola llamada de geo

  function build(eventType, geo, extra) {
    return Object.assign({
      event_type: eventType, ts_iso: new Date().toISOString(), ts_local: new Date().toString(),
      visitor_id: visitor.id, visit_count: visitor.visit_count, returning: visitor.returning,
      params: getParams()
    }, pageInfo(), dev, brw, geo, extra || {});
  }

  // Al cargar: reenvía lo que quedó pendiente (p. ej. clicks que navegaron).
  flushOutbox();

  /* ---------- pageview automático (espera geo: la página se queda) ---------- */
  var ready = geoPromise.then(function (geo) {
    var payload = build("pageview", geo, {});
    return trySend({ eid: enqueue(payload), payload: payload });
  });

  /* ---------- tracking de clicks ---------- */
  if (CONFIG.TRACK_CLICKS) {
    document.addEventListener("click", function (e) {
      var t = e.target; if (t && t.nodeType === 3) t = t.parentElement;
      var a = t && t.closest ? t.closest("a[href], [data-track]") : null;
      if (!a) return;
      var text = (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80);
      var label = a.getAttribute("data-track") || text || a.getAttribute("aria-label") || "(sin texto)";
      var href = a.getAttribute("href") || "";
      var payload = build("click", geoCache || {}, { target_href: href, target_text: text, target_label: label });
      var eid = enqueue(payload);   // guardado al instante (sobrevive a la navegación)

      var sameTabNav = a.tagName === "A" && a.href && e.button === 0 &&
        !e.metaKey && !e.ctrlKey && !e.shiftKey && !e.altKey &&
        (!a.target || a.target === "_self") &&
        !/^(#|mailto:|tel:|javascript:)/i.test(href);

      // Si navega en la misma pestaña: NO enviamos ahora (se mandaría a medias / duplicado).
      // Queda en el outbox y se envía al cargar la página destino → exactamente una vez.
      // Si la página se queda (target=_blank, botón, ancla): enviamos ya.
      if (!sameTabNav) { trySend({ eid: eid, payload: payload }); }
    }, true);
  }

  /* ---------- API pública ---------- */
  function log(eventType, extra) {
    var payload = build(eventType, geoCache || {}, extra);
    return trySend({ eid: enqueue(payload), payload: payload });
  }
  window.SigmaTrack = { ready: ready, log: log, flush: flushOutbox, config: CONFIG };
})();
