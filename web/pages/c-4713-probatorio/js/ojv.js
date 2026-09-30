/**
 * ojv.js — Expediente OJV (web/ojv.html?causa=<ROL>)
 *
 * Datos:       data/ojv/<causa>.json   ← scripts/build_ojv_causa.py (qué tenemos y qué falta, desde el disco)
 * Anotaciones: GET/POST /api/ojv/*     ← scripts/serve_web.py → data/ojv/<causa>.anotaciones.json
 *
 * Sin API (live-server, file://) la página se ve igual pero en solo lectura: un campo que parece
 * guardar y al recargar vuelve vacío es peor que un campo deshabilitado.
 */
const Ojv = (() => {
  const SVG = {
    pdf: '<svg viewBox="0 0 16 18" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M2.5 1.5h7l4 4v11h-11z"/><path d="M9.5 1.5v4h4"/><text x="3.4" y="14" font-size="4.6" font-family="Arial" font-weight="700" fill="currentColor" stroke="none">PDF</text></svg>',
    anexo: '<svg viewBox="0 0 18 16" fill="currentColor"><path d="M1 3.5C1 2.7 1.7 2 2.5 2h4l1.6 1.8h7.4c.8 0 1.5.7 1.5 1.5V6H4.2L1 13z"/><path d="M4.4 7H17l-2.6 7H1.5z"/></svg>',
    geo: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="8" cy="8" r="6.5"/><path d="M1.5 8h13M8 1.5c2 2 2 11 0 13M8 1.5c-2 2-2 11 0 13"/></svg>',
    nulo: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="8" cy="8" r="6"/><path d="M3.8 3.8l8.4 8.4"/></svg>',
  };
  const TABS = [
    ["historia", "📜 Historia"], ["litigantes", "👥 Litigantes"], ["notificaciones", "📬 Notificaciones"],
    ["escritos", "📝 Escritos por Resolver"], ["exhortos", "🌎 Exhortos"],
  ];
  // Peso = cuánto le sirve (o le pesa) el documento al caso de Jorge. Lo fija el equipo, no el tribunal.
  const PESOS = ["sin evaluar", "trámite sin incidencia", "contexto", "útil: apoya un punto de prueba",
    "importante: prueba un punto o fija posición", "decisivo: puede ganar o perder un punto"];
  const LEYENDA_PESO = PESOS.map((t, i) => `${i} = ${t}`).join("\n");
  // Riesgo = cuánto puede dañar el documento al caso de Jorge (lo que la contraria puede usar). Mismo criterio 0–5.
  const RIESGOS = ["sin evaluar", "sin riesgo", "bajo: la contraria difícilmente lo usa", "medio: la contraria puede usarlo",
    "alto: daña un punto o nos fija una posición", "crítico: puede hacernos perder un punto"];
  const LEYENDA_RIESGO = RIESGOS.map((t, i) => `${i} = ${t}`).join("\n");
  const causa = new URLSearchParams(location.search).get("causa") || "C-4713-2025";
  let D = null, ANO = { campos: [], filas: {}, notas_franco: [] }, API = false;
  let tab = "historia", filtro = "todos", texto = "";
  const timers = {};
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  async function iniciar() {
    document.querySelectorAll("[data-i]").forEach((e) => (e.innerHTML = SVG[e.dataset.i]));
    try {
      const r = await fetch(`data/ojv/${encodeURIComponent(causa)}.json`, { cache: "no-store" });
      if (!r.ok) throw new Error(r.status);
      D = await r.json();
    } catch (e) {
      $("vista").innerHTML = `<div class="aviso">No hay datos para ${esc(causa)}. Correr: <code>python3 scripts/build_ojv_causa.py ${esc(causa)}</code></div>`;
      return;
    }
    try {
      const r = await fetch(`/api/ojv/anotaciones?causa=${encodeURIComponent(causa)}`, { cache: "no-store" });
      if (r.ok) { const j = await r.json(); ANO = { campos: j.campos || [], filas: j.filas || {}, notas_franco: j.notas_franco || [] }; API = true; }
    } catch (_) { /* sin backend */ }
    let PUB = false;   // prod (DemoCustomerOps): anotaciones congeladas en un .json estático, solo lectura
    if (!API) {
      try {
        const r = await fetch(`data/ojv/${encodeURIComponent(causa)}.anotaciones.json`, { cache: "no-store" });
        if (r.ok) { const j = await r.json(); ANO = { campos: j.campos || [], filas: j.filas || {}, notas_franco: j.notas_franco || [] }; PUB = true; }
      } catch (_) { /* dev sin backend: sin anotaciones */ }
    }
    if (PUB) {
      $("nuevoCampo").disabled = $("btnCampo").disabled = true;
    } else if (!API) {
      const a = $("aviso");
      a.hidden = false;
      a.innerHTML = "Solo lectura: esta página no está servida por <code>scripts/serve_web.py</code>, así que peso, análisis y campos no se pueden guardar. Levantar con <code>python3 scripts/serve_web.py</code> y abrir <code>/ojv.html?causa=" + esc(causa) + "</code>.";
      $("nuevoCampo").disabled = $("btnCampo").disabled = true;
    }
    document.title = `Expediente OJV · ${D.causa}`;
    // El molde es uno solo: marca y «volver» salen de la cabecera del YAML de cada causa.
    $("marcaCausa").textContent = `Expediente ${D.causa}`;
    const v = D.cabecera.volver;
    if (v && v.href) { $("volver").href = v.href; $("volver").textContent = v.label || "← Volver"; }
    cabecera();
    pestañas();
    eventos();
    pintar();
  }

  function cabecera() {
    const c = D.cabecera;
    $("fuente").textContent = `transcrito de la OJV al ${c.capturado} · local, no es la OJV`;
    const campos = [["ROL", c.rol], ["F. Ing.", c.f_ing], ["", c.caratulado], ["Est. Adm.", c.est_adm], ["Proc.", c.proc],
      ["Ubicación", c.ubicacion], ["Estado Proc.", c.estado_proc], ["Etapa", c.etapa], ["Tribunal", c.tribunal]];
    $("cab").innerHTML = campos.map(([k, v]) => `<div>${k ? `<b>${k}:</b> ` : ""}${esc(v)}</div>`).join("");
    const e = D.enlaces;
    const enl = [["📘 Texto Demanda", e.texto_demanda, "pdf"], ["🗂️ Anexos de la causa", e.anexos, "anexo"],
      ["📨 Certificado de Envío", e.certificado_envio, "pdf"], ["📚 Ebook", e.ebook, "pdf"]];
    $("cabEnl").innerHTML = enl.map(([k, v, i]) => `<div><b>${k}:</b>${icono(i, v)}</div>`).join("");
    $("cuaderno").innerHTML = `<option>${esc(c.cuaderno)}</option>`;
    $("infoRec").innerHTML = icono("anexo", e.info_receptor);
    const r = D.resumen;
    $("cTen").textContent = `✅ ${r.tenemos} documentos tenemos`;
    $("cFal").textContent = `🔴 ${r.faltan} faltan`;
    $("cSin").textContent = `🚫 ${r.sin_doc} sin documento en la OJV`;
    $("notaPie").innerHTML = `Folios que la Historia de la OJV no muestra: <b>${D.no_aparecen.join(", ") || "ninguno"}</b>. ` +
      `Los documentos del ebook abren en su página. Tras cambiar el YAML: <code>python3 scripts/build_ojv_causa.py ${esc(D.causa)}</code>. ` +
      `Anotaciones: <code>data/ojv/${esc(D.causa)}.anotaciones.json</code> (historial en <code>data/registries/ojv-anotaciones.jsonl</code>).`;
  }

  function icono(tipo, doc, titulo) {
    const svg = SVG[tipo === "pdf2" || tipo === "copia" ? "pdf" : tipo] || SVG.pdf;
    const clase = `ic ${tipo}`;
    if (doc && doc.estado === "tenemos" && doc.href) {
      const t = titulo || [doc.archivo, doc.paginas, doc.kb != null ? `${doc.kb} KB` : "", doc.md5 ? `MD5 ${doc.md5}` : "", doc.nota].filter(Boolean).join(" · ");
      return `<a class="${clase}" href="${doc.href}" target="_blank" rel="noopener" title="${esc(t)}">${svg}</a>`;
    }
    const t = titulo || `FALTA — la OJV lo tiene y no está en el vault${doc && doc.archivo ? ": " + doc.archivo : ""}`;
    return `<span class="${clase} falta" title="${esc(t)}">${svg}</span>`;
  }

  function pestañas() {
    const n = { historia: D.historia.length, litigantes: D.litigantes.length,
      notificaciones: notificaciones().length, escritos: D.escritos_por_resolver.length, exhortos: 0 };
    $("tabs").innerHTML = TABS.map(([k, v]) =>
      `<button role="tab" data-t="${k}" class="${k === tab ? "on" : ""}">${v}<span class="n">${n[k]}</span></button>`).join("");
  }

  const notificaciones = () => D.historia.filter((h) => /Receptor|Notific/i.test(h.tramite + " " + h.desc));

  function eventos() {
    $("tabs").addEventListener("click", (e) => {
      const b = e.target.closest("button[data-t]"); if (!b) return;
      tab = b.dataset.t; pestañas(); pintar();
    });
    $("filtros").addEventListener("click", (e) => {
      const b = e.target.closest("button[data-f]"); if (!b) return;
      filtro = b.dataset.f;
      $("filtros").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
      filtrar();
    });
    $("buscar").addEventListener("input", (e) => { texto = e.target.value.toLowerCase(); filtrar(); });
    $("btnCampo").addEventListener("click", agregarCampo);
    $("nuevoCampo").addEventListener("keydown", (e) => { if (e.key === "Enter") agregarCampo(); });
    $("panelCerrar").addEventListener("click", cerrarPanel);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") cerrarPanel(); });
    $("vista").addEventListener("click", clickVista);
    $("vista").addEventListener("input", inputVista);
    $("vista").addEventListener("focusout", (e) => { const k = e.target.dataset && e.target.dataset.k; if (k && timers[k + e.target.dataset.c]) guardarAhora(e.target); });
  }

  // ── Pintar ────────────────────────────────────────────────────────────────
  function pintar() {
    const v = $("vista");
    $("barra").style.display = tab === "historia" || tab === "escritos" || tab === "notificaciones" ? "" : "none";
    if (tab === "historia") v.innerHTML = notasFranco() + tabla(D.historia, true);
    else if (tab === "notificaciones") v.innerHTML = tabla(notificaciones(), true);
    else if (tab === "escritos") v.innerHTML = tabla(D.escritos_por_resolver, false);
    else if (tab === "litigantes") v.innerHTML = litigantes();
    else v.innerHTML = `<div class="caja">Sin exhortos en la captura del ${esc(D.cabecera.capturado)}. <small>(No se capturó esta pestaña: verificar en la OJV.)</small></div>`;
    filtrar();
    score();
  }

  function cabezasPropias() {
    return `<th class="propio" title="Peso (0–5): cuánto le sirve el documento al caso\n${LEYENDA_PESO}">⚖️ Peso <span class="ayuda">ⓘ</span></th><th class="propio riesgo" title="Riesgo (0–5): cuánto puede dañar el documento al caso\n${LEYENDA_RIESGO}">⚠️ Riesgo <span class="ayuda">ⓘ</span></th><th class="propio">🧠 Análisis</th>` +
      ANO.campos.map((c) => `<th class="propio">${esc(c.nombre)}${API ? `<span class="x" data-quitar="${c.id}" title="Quitar la columna (los valores quedan guardados)">✕</span>` : ""}</th>`).join("");
  }

  function tabla(filas, esHistoria) {
    const cab = esHistoria
      ? "<th>🔢 Folio</th><th>📄 Doc.</th><th>📎 Anexo</th><th>🧭 Etapa</th><th>⚙️ Trámite</th><th>🗒️ Desc. Trámite</th><th>📅 Fec. Trámite</th><th>📑 Foja</th>"
      : "<th>📅 Fecha</th><th>📄 Doc.</th><th>🙋 Parte</th><th>📝 Escrito</th>";
    return `<div class="scroll"><table><thead><tr>${cab}${cabezasPropias()}</tr></thead><tbody>${
      filas.map((f) => fila(f, esHistoria)).join("")}</tbody></table></div>`;
  }

  function celdaDocs(f) {
    if (f.estado === "sin_doc") return `<span class="ic nulo" title="La OJV no tiene documento para este trámite">${SVG.nulo}</span>`;
    const docs = f.docs.filter((d) => d.tipo !== "anexo").map((d) => icono(d.tipo, d)).join("");
    const copias = (f.copias || []).filter((c) => c.estado === "tenemos").map((c) => icono("copia", c, `Copia propia: ${c.archivo}`)).join("");
    return `<div class="doc-cel">${docs}${copias}</div>`;
  }

  function fila(f, esHistoria) {
    const a = ANO.filas[f.clave] || {};
    const buscable = [f.folio, f.etapa, f.tramite, f.desc, f.fecha, f.parte, f.resumen, a.analisis,
      ...Object.values(a.campos || {})].join(" ").toLowerCase();
    const anexo = (f.docs || []).filter((d) => d.tipo === "anexo").map((d) => icono("anexo", d)).join("");
    const ojv = esHistoria
      ? `<td class="o folio">${f.folio}${enlaces(f)}</td><td class="o">${celdaDocs(f)}</td><td class="o">${anexo}</td>` +
        `<td class="o">${esc(f.etapa)}</td><td class="o">${esc(f.tramite)}</td><td class="o">${esc(f.desc)}</td>` +
        `<td class="o fecha">${esc(f.fecha)}</td><td class="o">${esc(f.foja)}</td>`
      : `<td class="o fecha">${esc(f.fecha)}</td><td class="o">${celdaDocs(f)}</td><td class="o">${esc(f.parte)}</td><td class="o">${esc(f.desc)}</td>`;
    const tieneAn = (f.analisis || []).length || (a.analisis || "").trim();
    return `<tr class="e-${f.estado}" data-folio="${f.folio ?? ""}" data-clave="${f.clave}" data-estado="${f.estado}" data-an="${tieneAn ? 1 : 0}" data-peso="${a.peso || 0}" data-riesgo="${a.riesgo || 0}" data-txt="${esc(buscable)}">` +
      ojv + `<td class="propio">${peso(f.clave, a.peso || 0)}</td><td class="propio">${escala(f.clave, a.riesgo || 0, "riesgo")}</td><td class="propio">${analisis(f, a)}</td>` +
      ANO.campos.map((c) => `<td class="propio"><input class="campo" data-k="${f.clave}" data-c="${c.id}" value="${esc((a.campos || {})[c.id] || "")}" ${API ? "" : "disabled"}></td>`).join("") +
      `</tr>`;
  }

  const escala = (clave, n, tipo) => {
    const T = tipo === "riesgo" ? RIESGOS : PESOS;
    const prop = (ANO.filas[clave] || {}).origen;
    return `<span class="peso ${tipo}" data-escala="${tipo}" data-peso-de="${clave}" aria-disabled="${!API}" title="${tipo === "riesgo" ? "Riesgo" : "Peso"} ${n}/5 · ${T[n]}${API ? " · clic para cambiar (clic en el mismo punto = 0)" : ""}">${
      [1, 2, 3, 4, 5].map((i) => `<i data-v="${i}" class="${i <= n ? "on" : ""}" title="${i} · ${T[i]}"></i>`).join("")}</span>${n ? `<small class="peso-txt ${tipo}">${T[n]}</small>` : ""}${prop && tipo === "peso" ? `<small class="propuesta" title="${esc(prop)}">🤖 propuesta · confirmar</small>` : ""}`;
  };
  const peso = (clave, n) => escala(clave, n, "peso");
  // Resolución ↔ escrito que provee (índice del ebook OJV): se salta de un folio al otro.
  const enlaces = (f) =>
    (f.provee || []).map((g) => `<button class="enlace" data-ir="${g}" title="Esta resolución provee el escrito del folio ${g}">↳ provee ${g}</button>`).join("") +
    (f.resuelto_por || []).map((g) => `<button class="enlace" data-ir="${g}" title="Este escrito lo proveyó la resolución del folio ${g}">↰ resuelto en ${g}</button>`).join("");
  function analisis(f, a) {
    const res = f.resumen ? `<div class="resumen">${esc(f.resumen)}</div>` : "";
    const links = (f.analisis || []).length
      ? `<div class="an-links">${f.analisis.map((x) => `<button data-md="${esc(x.ruta)}" title="${esc(x.ruta)}">📄 ${esc(x.nombre.length > 70 ? x.nombre.slice(0, 70) + "…" : x.nombre)}${x.existe ? "" : " ⚠️ no existe"}</button>`).join("")}</div>` : "";
    return res + links + notasDeFolio(f) + `<textarea class="nuestro" data-k="${f.clave}" data-c="analisis" placeholder="${API ? "Nuestro análisis…" : "solo lectura"}" ${API ? "" : "disabled"}>${esc(a.analisis || "")}</textarea>`;
  }

  // Notas de Franco (formulario de Google → scripts/importar_notas_franco.py). Van aparte de lo nuestro.
  const folioDe = (n) => (String(n.folio || "").match(/\d+/) || [""])[0];
  function notasDeFolio(f) {
    const ns = (ANO.notas_franco || []).filter((n) => f.folio != null && folioDe(n) === String(f.folio));
    return ns.map((n) => `<div class="nota-franco${n.urgente ? " urgente" : ""}">💬 <b>Franco</b> · ${esc(n.marca)}${n.urgente ? " · 🔴 urgente" : ""}<br>${esc(n.nota)}</div>`).join("");
  }
  function notasFranco() {
    const ns = [...(ANO.notas_franco || [])].reverse();
    if (!ns.length) return "";
    return `<details class="caja notas-franco" open><summary>💬 Notas de Franco <span class="n">${ns.length}</span></summary>${
      ns.map((n) => `<div class="nota-franco${n.urgente ? " urgente" : ""}"><b>${esc(n.folio || "sin folio")}</b> · ${esc(n.marca)}${n.urgente ? " · 🔴 urgente" : ""}<br>${esc(n.nota)}</div>`).join("")}</details>`;
  }

  function litigantes() {
    return `<div class="scroll"><table style="min-width:600px"><thead><tr><th>Participante</th><th>RUT</th><th>Persona</th><th>Nombre o Razón Social</th></tr></thead><tbody>${
      D.litigantes.map((l) => `<tr><td class="o">${esc(l.participante)}</td><td class="o">${esc(l.rut) || "<span style='opacity:.4'>—</span>"}</td><td class="o">${esc(l.persona)}</td><td class="o">${esc(l.nombre)}</td></tr>`).join("")
    }</tbody></table></div><p class="nota-pie">Transcrito del repo, no de la pestaña Litigantes de la OJV (no se capturó): los RUT quedan en blanco hasta verlos ahí.</p>`;
  }

  // Score: promedios sobre lo evaluado (0 = sin evaluar no cuenta) + los focos de riesgo.
  function score() {
    const el = $("score"); if (!el || !D) return;
    const claves = [...D.historia, ...D.escritos_por_resolver].filter((f) => f.estado !== "sin_doc").map((f) => f.clave);
    const vals = (k) => claves.map((c) => (ANO.filas[c] || {})[k] || 0).filter((v) => v > 0);
    const prom = (xs) => (xs.length ? (xs.reduce((a, b) => a + b, 0) / xs.length).toFixed(1) : "—");
    const P = vals("peso"), R = vals("riesgo");
    const altos = claves.filter((c) => ((ANO.filas[c] || {}).riesgo || 0) >= 4).length;
    const prop = claves.filter((c) => (ANO.filas[c] || {}).origen).length;
    el.innerHTML = `<b>📊 Score</b> <span class="chip">⚖️ peso ${prom(P)}/5 <small>(${P.length} evaluados)</small></span>` +
      `<span class="chip fa">⚠️ riesgo ${prom(R)}/5 <small>(${R.length} evaluados · ${claves.length - R.length} sin evaluar)</small></span>` +
      `<span class="chip fa">🔴 ${altos} con riesgo alto o crítico</span>` +
      (prop ? `<span class="chip">🤖 ${prop} propuestas por confirmar</span>` : "");
  }

  function filtrar() {
    document.querySelectorAll("#vista tbody tr[data-clave]").forEach((tr) => {
      let ok = true;
      if (filtro === "faltan") ok = tr.dataset.estado === "falta" || tr.dataset.estado === "parcial";
      else if (filtro === "con-analisis") ok = tr.dataset.an === "1";
      else if (filtro === "sin-peso") ok = tr.dataset.peso === "0" && tr.dataset.estado !== "sin_doc";
      else if (filtro === "riesgo-alto") ok = Number(tr.dataset.riesgo) >= 4;
      else if (filtro === "propuestas") ok = !!(ANO.filas[tr.dataset.clave] || {}).origen;
      if (ok && texto) ok = tr.dataset.txt.includes(texto);
      tr.classList.toggle("oculta", !ok);
    });
  }

  // ── Interacción ───────────────────────────────────────────────────────────
  function clickVista(e) {
    const ir = e.target.closest("[data-ir]");
    if (ir) {
      const dest = [...document.querySelectorAll(`tr[data-folio="${ir.dataset.ir}"]`)].find((t) => t.dataset.estado !== "sin_doc")
        || document.querySelector(`tr[data-folio="${ir.dataset.ir}"]`);
      if (dest) { dest.classList.remove("oculta"); dest.scrollIntoView({ block: "center", behavior: "smooth" });
        dest.classList.add("destello"); setTimeout(() => dest.classList.remove("destello"), 1800); }
      return;
    }
    const md = e.target.closest("button[data-md]");
    if (md) return abrirPanel(md.dataset.md);
    const q = e.target.closest("[data-quitar]");
    if (q) return quitarCampo(q.dataset.quitar);
    const bola = e.target.closest(".peso i");
    if (bola && API) {
      const cont = bola.parentElement, clave = cont.dataset.pesoDe, tipo = cont.dataset.escala || "peso";
      const actual = (ANO.filas[clave] || {})[tipo] || 0;
      const v = Number(bola.dataset.v) === actual ? 0 : Number(bola.dataset.v);
      enviar("/api/ojv/anotar", { causa, clave, cambios: { [tipo]: v } }).then((ok) => {
        if (!ok) return;
        const tr = document.querySelector(`tr[data-clave="${clave}"]`);
        if (tr) {
          tr.dataset[tipo] = v;
          const a = ANO.filas[clave] || {};
          tr.querySelectorAll("td.propio")[0].innerHTML = escala(clave, a.peso || 0, "peso");
          tr.querySelectorAll("td.propio")[1].innerHTML = escala(clave, a.riesgo || 0, "riesgo");
        }
        score();
      });
    }
  }

  function inputVista(e) {
    const t = e.target; if (!t.dataset.k) return;
    const id = t.dataset.k + t.dataset.c;
    t.classList.add("guardando"); t.classList.remove("guardado");
    clearTimeout(timers[id]);
    timers[id] = setTimeout(() => guardarAhora(t), 900);
  }

  function guardarAhora(t) {
    const id = t.dataset.k + t.dataset.c;
    clearTimeout(timers[id]); delete timers[id];
    const cambios = t.dataset.c === "analisis" ? { analisis: t.value } : { campos: { [t.dataset.c]: t.value } };
    enviar("/api/ojv/anotar", { causa, clave: t.dataset.k, cambios }).then((ok) => {
      t.classList.remove("guardando");
      if (ok) { t.classList.add("guardado"); setTimeout(() => t.classList.remove("guardado"), 1200); }
    });
  }

  function agregarCampo() {
    const nombre = $("nuevoCampo").value.trim();
    if (!nombre || !API) return;
    const id = "c" + Date.now().toString(36).slice(-8);
    enviar("/api/ojv/campos", { causa, campos: [...ANO.campos, { id, nombre }] }).then((ok) => {
      if (ok) { $("nuevoCampo").value = ""; pintar(); }
    });
  }

  function quitarCampo(id) {
    enviar("/api/ojv/campos", { causa, campos: ANO.campos.filter((c) => c.id !== id) }).then((ok) => ok && pintar());
  }

  async function enviar(url, cuerpo) {
    const est = $("estadoGuardado");
    est.textContent = "guardando…";
    try {
      const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json", "X-LegalOps": "1" }, body: JSON.stringify(cuerpo) });
      const j = await r.json();
      if (!r.ok || !j.ok) throw new Error(j.error || r.status);
      ANO = { campos: j.campos || [], filas: j.filas || {}, notas_franco: j.notas_franco || [] };
      est.textContent = "guardado en el repo · " + new Date().toLocaleTimeString("es-CL", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      return true;
    } catch (err) {
      est.textContent = "⛔ no se guardó: " + err.message;
      return false;
    }
  }

  // ── Panel de análisis (.md del repo) ──────────────────────────────────────
  async function abrirPanel(ruta) {
    $("panelTit").textContent = ruta.split("/").pop().replace(/\.md$/, "");
    $("panelRuta").textContent = ruta;
    $("panelMd").innerHTML = "cargando…";
    $("panel").classList.add("abierto"); $("panel").setAttribute("aria-hidden", "false");
    try {
      let texto;
      if (API) {
        const r = await fetch(`/api/md?ruta=${encodeURIComponent(ruta)}`, { cache: "no-store" });
        const j = await r.json();
        if (!j.ok) throw new Error(j.error);
        texto = j.texto;
      } else {   // prod: el publicador copia cada .md de análisis a analisis/<nombre>
        const r = await fetch(`analisis/${encodeURIComponent(ruta.split("/").pop())}`, { cache: "no-store" });
        if (!r.ok) throw new Error(r.status);
        texto = await r.text();
      }
      $("panelMd").innerHTML = md(texto);
    } catch (e) {
      $("panelMd").innerHTML = `<p>No se pudo leer (${esc(e.message)}). ${API ? "" : "Sin <code>serve_web.py</code> no hay lectura de .md."}</p><p><code>${esc(ruta)}</code></p>`;
    }
  }
  function cerrarPanel() { $("panel").classList.remove("abierto"); $("panel").setAttribute("aria-hidden", "true"); }

  // Markdown mínimo: lo justo para leer una ficha (encabezados, citas, listas, tablas, código, negrita).
  function md(src) {
    const cuerpo = src.replace(/^---\n[\s\S]*?\n---\n/, "");
    const inl = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, "$1<i>$2</i>").replace(/\[\[([^\]]+)\]\]/g, "<code>$1</code>");
    const out = []; let lista = null, tabla = null, pre = null;
    const cerrar = () => { if (lista) { out.push(`</${lista}>`); lista = null; } if (tabla) { out.push("</tbody></table>"); tabla = null; } };
    for (const l of cuerpo.split("\n")) {
      if (l.startsWith("```")) { if (pre !== null) { out.push(`<pre>${esc(pre)}</pre>`); pre = null; } else { cerrar(); pre = ""; } continue; }
      if (pre !== null) { pre += l + "\n"; continue; }
      let m;
      if ((m = l.match(/^(#{1,4})\s+(.*)/))) { cerrar(); out.push(`<h${m[1].length}>${inl(m[2])}</h${m[1].length}>`); }
      else if (/^\s*\|/.test(l)) {
        if (/^\s*\|[\s:|-]+\|\s*$/.test(l)) continue;
        if (lista) { out.push(`</${lista}>`); lista = null; }
        const celdas = l.trim().replace(/^\||\|$/g, "").split("|").map((c) => inl(c.trim()));
        if (!tabla) { out.push(`<table><tbody>`); tabla = true; }
        out.push(`<tr>${celdas.map((c) => `<td>${c}</td>`).join("")}</tr>`);
      }
      else if ((m = l.match(/^\s*>\s?(.*)/))) { cerrar(); out.push(`<blockquote>${inl(m[1])}</blockquote>`); }
      else if ((m = l.match(/^\s*(?:[-*]|\d+\.)\s+(.*)/))) {
        const tipo = /^\s*\d+\./.test(l) ? "ol" : "ul";
        if (tabla) { out.push("</tbody></table>"); tabla = null; }
        if (lista !== tipo) { if (lista) out.push(`</${lista}>`); out.push(`<${tipo}>`); lista = tipo; }
        out.push(`<li>${inl(m[1])}</li>`);
      }
      else if (!l.trim()) cerrar();
      else { cerrar(); out.push(`<p>${inl(l)}</p>`); }
    }
    cerrar();
    return out.join("\n");
  }

  return { iniciar };
})();
