# Changelog — DemoCustomerOps

## 2026-06-18 · Demo interactivo del Gemelo Digital SIGMA

El dashboard del gemelo digital (planta de oro, proceso RIL) pasó de **KPIs
estáticos** a una **simulación interactiva en vivo**. Archivo:
`web/Dashboard_GemeloDigital_SIGMA.html`. Sigue siendo "datos representativos"
(disclaimer mantenido) — a reemplazar por KPIs reales del piloto.

### Simulación en tiempo real
- Motor coherente de planta de oro: recuperación, TOC (carbón orgánico), carga
  de resina, throughput, ley de cabeza, energía, P80, Au en relaves, etc., con
  correlaciones reales (pico de TOC → cae la recuperación; resina que se satura
  y se eluciona; oro recuperado **derivado** de tonelaje × ley × recuperación).
- Anima las 4 vistas: Sala de Control, Tablero de Turnos, Vista Móvil, Analítica.
- Sparklines que ruedan, balance de proceso dinámico, gráfico 24 h Real vs Gemelo
  con **muestreo en vivo** + velocidad de adquisición.

### Monitor de salud de la planta (estilo Resident Evil)
- ECG en la barra superior cuyo estado/color deriva de la salud real: **FINE
  (verde) → CAUTION (verde-lima) → CAUTION (naranja) → DANGER (rojo)**, con el
  latido propagado a la página (degradé). Velocidad y picos constantes.

### Asistente IA "Sasha" + alertas predictivas
- Reacciona al estado/slider: ~10 **supuestos** con acción del **metalurgista**;
  nunca dice "sin causa clara" (siempre propone una causa concreta con % de
  acertividad).
- **Validación del Ing. de procesos** sube la confianza a **99%**; el 1% queda al
  criterio del metalurgista en terreno.
- En estado crítico (DANGER): diagnósticos catastróficos (falla del molino de
  bolas, colapso de adsorción, derrame de NaCN, rotura de hidrociclón) con
  predicción del efecto en cascada.
- Chat placeholder ("En construcción…").

### Capacidad de proceso · Lean Six Sigma (Analítica)
- Nivel σ, Cpk, DPMO y Yield calculados en vivo sobre la variación de la
  recuperación vs LSL 90%, con interpretación (capaz / marginal / fuera de control).

### Interacción y sincronización
- Slider **"Rec Au · 👈 Simular"** (topbar y celular) para simular escenarios.
- **Sync en tiempo real PC ⇄ celular** vía MQTT sobre WebSocket (broker público,
  sin backend); indicador de estado "sync ON/OFF".
- Velocímetros del Tablero de Turnos con aguja + número + readout sincronizados,
  fluctuación tipo sensor real.

### Estructura / navegación
- Logo SIGMA → enlaza al Dashboard.
- **Vista Móvil real** (sin marco de teléfono mockup): la vista responsive que se
  ve de verdad en el celular.
- **Badge de madurez**: Modelo › **Digital Shadow** › Gemelo Digital (P3 · Nivel 1).

### Notas técnicas
- WebRTC no se usó: requiere un signaling server que GitHub Pages (estático) no
  hospeda; MQTT pub/sub es el patrón correcto para sync cross-device sin backend.
- El canal de sync es público (solo viaja el estado de la simulación, sin datos
  sensibles); en producción se usaría un canal privado/autenticado.
