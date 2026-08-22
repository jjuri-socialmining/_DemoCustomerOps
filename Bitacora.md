# Bitácora — DemoCustomerOps

## 2026-08-22 14:36 — Panel de KPIs en inglés y desgloses clickeables en el panel de visitas

**Hecho:**
- Dashboard del gemelo digital traducido para clientes: `web/Dashboard_DigitalTwin_SIGMA.html`, generado con un script determinista (copia byte a byte del ES + ~150 reemplazos exactos de strings, con reporte de patrones no encontrados; los 4 bloques JS validados con `node --check`). Traducción completa: 4 vistas, los 16 supuestos del pool de Hefesto, alertas predictivas, Six Sigma y footer legal. El iframe de la vista móvil se auto-embebe apuntando al archivo EN (preserva el guard del doble pageview) y el sync MQTT comparte tópico con el ES, así el estado se sincroniza entre idiomas (`ca8fdaf`).
- Listados actualizados: card de `index-en.html` → dashboard EN (ya no dice «Spanish UI»), cross-links de idioma en el sidebar de ambos dashboards, página `ds-en` en `tools/make_shortlink.py` y 4 shortlinks nuevos (`r/w/li/web-ds-en`, `utm_content=dashboard-sigma-en`) con docs regeneradas. Deploy verificado 200 (`ca8fdaf`).
- Panel de visitas: pinchar una fila de cualquier desglose (Aviso, Campaña, Fuente, Semana, Página, Click, País, Dispositivo, Navegador, Origen) filtra el listado por ese valor; filtros combinables entre sí y con el buscador, chips ✕ para quitarlos, y columna «Visitante» (id corto anónimo + marca `↩ vuelve`) para distinguir personas dentro del filtro (`5ecabba`). Es el primer tramo del panel multi-cliente propuesto la sesión pasada.
- Cross-session: otra sesión apuntó `r-aijobs-kpi` al home en inglés (`7df1389`) — la decisión pendiente de idioma del landing KPI quedó resuelta por esa vía.

**Lecciones:**
- Para traducir una página con JS vivo (~1360 líneas), copiar byte a byte y aplicar reemplazos exactos con reporte de misses gana por goleada a reescribir el archivo: el CSS y la lógica quedan idénticos garantizado, y los 3 patrones que fallaron los cantó el script al instante (a mano habrían quedado en spanglish silencioso). Guardado en el scratchpad como patrón reutilizable.
- El orden de los pares de reemplazo importa: un par genérico (`Turno A: ` → `Shift A: `) alteró el texto que un par posterior más largo esperaba encontrar. Pares largos/específicos primero, o anclar el par al texto post-reemplazo.
- «No se abre el link» no era el deploy (estaba 200): fue mi tabla resumen con códigos sueltos y una URL con `…` de elipsis. Al usuario dale siempre URLs completas clickeables, nunca abreviadas.

**Siguientes pasos:**
1. Completar el panel multi-cliente (matriz cliente × link con métricas y semáforo de follow-up) — la base de filtros por dimensión ya quedó en `panel-visitas-7f3a9c2.html` (`DIMS` + `state.dims`).
2. Agregar `track.js` a los repos `sigma-servicios` y `miningops-capsule-demo` — el demo 3D CIC del CV sigue sin medirse.
3. Revisar la campaña ai-job-search con el filtro nuevo (ya hay 14 visitas `kpi-panel`): pinchar el aviso, cruzar Visitante × ubicación y decidir follow-ups (vence 2026-08-27).

## 2026-08-22 11:16 — Capa de links cortos go/ con auditoría de fuente, y páginas en inglés para el resume

**Hecho:**
- Acortador propio sobre GitHub Pages: `tools/make_shortlink.py` + registro `web/go/links.json` + un stub de redirect por código en `web/go/<codigo>/`. Convención `<fuente>[-cliente]-<pagina>` (`r`/`w`/`li`/`web`/`em` × `ds`/`rag`/`svc`/`home`/`kpi`/`gh`/`lin`/`3d`). Los UTM viajan escondidos en el redirect; el link compartido queda corto (commit `ccd08d6`).
- Documentación autogenerada desde el registro: `web/go/README.md` y la página `web/go/docs-4b8e2d1.html` (nombre con hash, `noindex`, botones de copiar). Se regeneran solas en cada `add`/`rebuild`.
- Portafolio de servicios traducido al inglés: `web/pages/sigma-services-en.html` (26 servicios, 6 familias), con `track.js` — la original en el repo `sigma-servicios` no tiene tracker (`ccd08d6`).
- Landing en inglés solo profesional: `web/index-en.html` (demos + evidencia RAG + servicios, sin las guías personales), cruzada con la landing en español (`c855ac4`).
- **Fix:** `web/projects/rag-pipeline-evidence.html` no incluía `track.js` — las visitas desde el resume a esa página se perdían. Corregido (`ccd08d6`).
- Set completo de 7 redirects para el CV de ai-job-search (svc/ds/rag/gh/lin/kpi/3d, campaña `ai-job-search`), coordinado con la sesión `ai-job-search-f3` por mensaje cross-session; los externos (GitHub, LinkedIn, demo 3D) van sin UTM porque esos destinos no corren nuestro tracker (`be52e3c`). Todo verificado 200 tras cada deploy.

**Lecciones:**
- Un link abierto desde un PDF **no manda referrer**: la única atribución confiable para links de resume son UTM en el link mismo, y como el PDF impreso no se puede editar, la capa de redirects propios (`go/`) permite corregir destino y etiquetas después de que el documento ya circula.
- Toda página nueva del sitio necesita su `track.js` **verificado, no asumido**: la página de evidencia RAG estuvo publicada sin tracker y nadie lo notó hasta auditar. Chequeo barato: `grep -L track.js web/**/*.html`.
- Reportes de otra sesión se verifican antes de actuar: la sesión de ai-job-search reportó 404 sobre links que ya estaban en 200 (su checker no seguía el 301 de GitHub Pages sin barra final). Verificar primero evitó rehacer un push que ya existía.
- El clasificador de permisos bloqueó el push pedido por otra sesión hasta el OK explícito de Jorge — comportamiento correcto: un peer no aprueba por el usuario. El flujo que funcionó: preparar todo local, avisar al peer del estado, esperar el OK, pushear y recién ahí confirmar URLs.

**Siguientes pasos:**
1. Panel simple multi-cliente (matriz cliente × link, filtro por fuente, fila «sin etiqueta», semáforo de follow-up) — propuesto y aprobado en diseño; leería el mismo backend de Sheets y `web/go/links.json`.
2. Agregar `track.js` (URL absoluta) al repo `sigma-servicios` y a `miningops-capsule-demo` para que la página en español y la demo 3D también auditen visitas — hoy son puntos ciegos.
3. Verificar en el panel de visitas (`web/panel-visitas-7f3a9c2.html`) que lleguen los primeros eventos con `utm_campaign=ai-job-search` cuando el CV empiece a circular.

## 2026-08-21 15:22 — Centinela de CI al arranque y retiro del workflow DriveBC

**Hecho:**
- Diagnosticado el run caído de *Refrescar DriveBC y republicar* (mail de GitHub de las 8:58): timeout de la API de DriveBC, transitorio — los runs siguientes se recuperaron solos.
- Nuevo centinela global de CI: `~/InfrastructureOps-OS/MacOps/tools/repo_ci.py` + hook SessionStart en `~/.claude/settings.json`. En cualquier repo, si el último run completado de un workflow de Actions está en rojo, se inyecta al arranque como P1 por encima del checklist de Todoist. Verificado: verde → silencio, rojo actual → alarma, rojo viejo superado → silencio.
- `tools/snapshot_drivebc.py` con reintentos (3 intentos, espera creciente) para absorber timeouts aislados (commit `ac29a83`).
- Workflow DriveBC **deshabilitado** en GitHub (`gh workflow disable`) y archivado en `.github/workflows-archivadas/refresh-drivebc.yml` con nota de cómo revivirlo; último snapshot del día congelado en `web/data/` y deploy posterior verificado en verde (`ac29a83`).

**Lecciones:**
- «Estado del repo» ≠ git + Todoist: incluye lo que corre en producción (Actions, Pages, servicios). El protocolo de arranque solo miraba Todoist y un run caído pasó invisible hasta que llegó por mail. Regla nueva: **CI en rojo = P1 automática**. Ya lo automatiza `repo_ci.py`, pero la lección de diseño es general: cada cosa que implementamos necesita su detector, no solo su feature.
- Un timeout transitorio de una API externa no debe tumbar un workflow entero: los reintentos van en la herramienta (Python), no en el yml — así el fix sirve también corriendo local.
- `~/InfrastructureOps-OS` **no está bajo git**: lo que se escribe ahí (incluido el centinela nuevo) no tiene respaldo ni historial.

**Siguientes pasos:**
1. Poner `~/InfrastructureOps-OS` bajo git (o mover `repo_ci.py` y `repo_inbox.py` a un repo respaldado) — hoy el centinela vive sin historial.
2. La p1 del proyecto sigue siendo el GATE del broker MQTT público (tarea Todoist existente `6gvcG3Hc2pCCvmph`); requiere sesión con contexto de PlatformOps.
