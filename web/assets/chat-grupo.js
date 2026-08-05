/* ============================================================================
   chat-grupo.js — chat del grupo de WhatsApp del dashboard, dentro de la página.
   Compartido por Dashboard_GemeloDigital_SIGMA.html y ..._ADR_SIGMA.html:
   los dos tenían su propia copia del chat y ya habían divergido. Una sola acá.

   MODELO DE EXPOSICIÓN — relay opt-in por mensaje
   -----------------------------------------------
   El broker es público y la página también. El emisor (📡 voz, tenant
   hermes-mineria) publica hacia la página SOLO los mensajes marcados
   explícitamente para el dashboard, nunca el flujo completo del grupo.

   CONTRATO ENTRANTE — TOPIC_IN, un JSON por mensaje
     { "id":"uuid", "ts":"2026-08-04T20:49:00Z", "group":"…@g.us",
       "from":"Jorge", "role":"user|bot", "text":"…" }

   CONTRATO SALIENTE — TOPIC_OUT, mismo formato, role:"user"
   Se escribe desde acá y el relay decide si lo mete en el grupo.

   La página está suscrita a LOS DOS topics: así los dashboards abiertos se ven
   entre sí sin depender del relay. Mientras el relay no exista, esto es un chat
   entre paneles y nada llega a WhatsApp.

   ⚠️ EL RELAY ES LA FRONTERA DE SEGURIDAD, NO ESTA PÁGINA.
   Esta página es pública: cualquiera puede abrir la consola y publicar en
   TOPIC_OUT con el nombre que quiera. El `from` que viaja acá es una etiqueta
   de cortesía, NO una identidad — no tiene forma de serlo desde un estático.
   El relay TIENE que autenticar/gatear antes de reenviar al grupo del cliente.
   Si el relay reenvía lo que le llegue, cualquiera postea en el grupo del
   cliente haciéndose pasar por quien quiera.

   Si el relay reenvía el mensaje de vuelta por TOPIC_IN, que conserve el `id`:
   el dedupe de acá lo colapsa con el eco local y no se ve duplicado.
   ========================================================================== */
(function (global) {
  'use strict';

  var MAX_TEXT   = 600;   // recorte defensivo: un mensaje enorme no rompe el panel
  var RETAIN     = 80;    // mensajes en pantalla
  var THROTTLE   = 800;   // ms mínimos entre envíos (página pública, freno al spam)

  /* Quien escribe desde el dashboard es la sala de control: se firma así, sin
     preguntar nada. No es una identidad verificable — ver la advertencia de
     arriba — es la etiqueta con la que el grupo ve entrar al panel.
     Va la sigla, con el rol completo en el tooltip para quien no la conozca. */
  var FROM      = 'OSC';
  var FROM_LONG = 'Operador de sala de control';

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function hhmm(ts) {
    var d = new Date(ts);
    if (isNaN(d.getTime())) return '';
    function p(n) { return n < 10 ? '0' + n : '' + n; }
    return p(d.getHours()) + ':' + p(d.getMinutes());
  }

  function uid() {
    return 'w' + Date.now().toString(36) + Math.random().toString(36).slice(2, 10);
  }

  /* Un mensaje solo se renderiza si cumple el contrato. Nada de confiar en que
     el emisor mande bien: esto viene de la red y es texto de terceros. */
  function valid(m, group) {
    if (!m || typeof m !== 'object') return false;
    if (typeof m.id !== 'string' || !m.id) return false;
    if (typeof m.text !== 'string' || !m.text.trim()) return false;
    if (isNaN(new Date(m.ts).getTime())) return false;
    if (group && m.group !== group) return false;
    return true;
  }

  function mount(opts) {
    var log = opts.log, input = opts.input, sendBtn = opts.sendBtn;
    if (!log || !input || !sendBtn) return null;

    var group   = opts.group || '';
    var setChip = typeof opts.setChip === 'function' ? opts.setChip : function () {};

    var msgs = [], seen = Object.create(null);
    var connected = false, client = null, lastSent = 0;
    var myName = opts.from || FROM;

    /* Aviso del propio panel, no del grupo. Entra al mismo array que los
       mensajes: si se hiciera appendChild, el próximo render() lo borraría
       — y el que se pierde es justo el «no se pudo enviar». */
    function note(html) {
      msgs.push({ id: uid(), ts: new Date().toISOString(), role: 'note', html: html });
      while (msgs.length > RETAIN) { delete seen[msgs.shift().id]; }
      render();
    }

    function render() {
      if (!msgs.length) {
        log.innerHTML = '<div class="cmsg bot">' + (connected
          ? '💬 <b>Conectado al grupo.</b> Todavía no hay mensajes marcados para el dashboard. Escribí abajo para participar.'
          : '🔌 <b>Sin conexión al grupo.</b> El panel vuelve solo cuando el feed esté disponible.'
        ) + '</div>';
        return;
      }
      log.innerHTML = msgs.map(function (m) {
        if (m.role === 'note') return '<div class="cmsg bot">' + m.html + '</div>';   // literal nuestro
        var txt = m.text.length > MAX_TEXT ? m.text.slice(0, MAX_TEXT) + '…' : m.text;
        var who = m.role === 'bot' ? 'Hefesto' : (m.from || 'Alguien');
        var t   = hhmm(m.ts);
        var mine = m.role !== 'bot' && myName && m.from === myName;
        var tip  = (m.from === FROM) ? ' title="' + esc(FROM_LONG) + '"' : '';
        return '<div class="cmsg ' + (mine ? 'you' : 'bot') + '">'
             + '<b' + tip + '>' + esc(who) + '</b>' + (t ? ' <span style="opacity:.6;font-size:10px">' + esc(t) + '</span>' : '')
             + '<br>' + esc(txt) + '</div>';
      }).join('');
      log.scrollTop = log.scrollHeight;
    }

    /* MQTT puede reentregar el mismo mensaje: dedupe por id, orden por ts. */
    function push(m) {
      if (!valid(m, group) || seen[m.id]) return;
      seen[m.id] = 1;
      msgs.push(m);
      msgs.sort(function (a, b) { return new Date(a.ts) - new Date(b.ts); });
      while (msgs.length > RETAIN) { delete seen[msgs.shift().id]; }
      render();
    }

    /* ---- envío: se habla acá, no se salta a WhatsApp ---- */
    function send() {
      var q = (input.value || '').trim();
      if (!q) return;
      input.value = '';

      var now = Date.now();
      if (now - lastSent < THROTTLE) { return; }
      lastSent = now;

      if (!connected || !client) {
        note('🔌 <b>Sin conexión al grupo.</b> No se pudo enviar; reintentá cuando el chip diga «grupo ON».');
        return;
      }

      var m = {
        id: uid(), ts: new Date().toISOString(), group: group,
        from: myName, role: 'user', text: q.slice(0, MAX_TEXT)
      };
      try {
        client.publish(opts.topicOut, JSON.stringify(m));
        push(m);                                 // eco local inmediato; el relay puede devolverlo con el mismo id
      } catch (e) {
        note('⚠️ <b>No se pudo enviar.</b> El mensaje no salió del navegador.');
      }
    }

    input.placeholder = 'Escribí como ' + myName + '…';
    if (myName === FROM) input.title = FROM_LONG;   // el rótulo largo no entra en el input
    render();
    sendBtn.addEventListener('click', send);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); send(); }
    });

    /* ---- transporte ---- */
    if (typeof global.mqtt === 'undefined') { setChip('grupo OFF', '#FF5A6A'); render(); return { push: push }; }

    setChip('grupo…', '#FFB02E');
    try {
      client = global.mqtt.connect(opts.broker, {
        clientId: 'sigmachat_' + Math.random().toString(36).slice(2, 10),
        reconnectPeriod: 4000, connectTimeout: 8000, clean: true
      });
      /* Escucha los DOS topics. El de entrada trae lo que el relay saca del
         grupo; el de salida trae lo que escriben los otros dashboards abiertos.
         Sin esto la página publicaría al vacío hasta que exista el relay, y dos
         dashboards no se verían entre sí. El dedupe por id absorbe el eco
         propio y el que devuelva el relay. */
      client.on('connect', function () {
        /* topicHist trae el backlog del grupo en UN mensaje retenido: el broker se
           lo entrega a cada panel apenas se suscribe. Sin esto el chat arranca en
           blanco aunque el grupo tenga conversación, porque qos 0 no guarda nada. */
        var subs = [opts.topicIn, opts.topicOut];
        if (opts.topicHist) subs.push(opts.topicHist);
        client.subscribe(subs);
        connected = true; setChip('💬 grupo ON', '#37D27D'); render();
      });
      client.on('reconnect', function () { setChip('grupo…', '#FFB02E'); });
      client.on('offline', function () { connected = false; setChip('grupo OFF', '#FF5A6A'); render(); });
      client.on('error', function () { connected = false; setChip('grupo OFF', '#FF5A6A'); render(); });
      client.on('message', function (t, p) {
        try {
          var d = JSON.parse(p.toString());
          /* El backlog viene como {messages:[…]}, no como un mensaje suelto. Cada
             uno pasa por el mismo push() — valida igual y el dedupe por id evita
             que se repita lo que ya estaba en pantalla. */
          if (opts.topicHist && t === opts.topicHist && d && d.messages) {
            for (var i = 0; i < d.messages.length; i++) push(d.messages[i]);
            return;
          }
          push(d);
        } catch (e) { /* payload roto: se ignora */ }
      });
    } catch (e) {
      connected = false; setChip('grupo OFF', '#FF5A6A'); render();
    }

    return { push: push };
  }

  global.ChatGrupo = { mount: mount, esc: esc };
})(window);
