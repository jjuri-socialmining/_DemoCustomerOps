# Mensajes de difusión — Gemelo Digital SIGMA

Plantillas listas para enviar por WhatsApp. Reemplazá `[ ]` y copiá/pegá.
Link del demo: https://jjuri-socialmining.github.io/_DemoCustomerOps/Dashboard_GemeloDigital_SIGMA.html

---

## 1) Equipo (interno)

> 🟢 *SIGMA · Gemelo Digital — update del demo*
>
> Equipo, subimos una tanda grande de mejoras al dashboard del cliente. Ya no es
> una presentación estática: está *vivo e interactivo*.
>
> • Simulación de planta de oro en tiempo real (recuperación, TOC, resina,
>   throughput, energía, relaves…).
> • Asistente IA "Sasha": diagnostica la causa probable y recomienda la acción del
>   metalurgista; se valida con el Ing. de procesos (confianza 90% → 99%).
> • Monitor de salud de planta estilo monitor cardíaco (verde / amarillo / rojo).
> • Slider "¿qué pasa si…?" para simular escenarios; *sincronizado PC ⇄ celular* en
>   tiempo real.
> • Indicador de capacidad Lean Six Sigma (σ, Cpk, DPMO, Yield).
> • Vista móvil real + badge de madurez (Digital Shadow → Gemelo Digital).
>
> Link: [URL]
> Próximos pasos en Todoist (proyecto *DemoCustomerOps*).

---

## 2) Cliente (express · valor de negocio, NO técnico)

> Hola [Nombre] 👋
>
> Le comparto el avance del *Gemelo Digital* de la planta. Ya no es una
> presentación: es un *tablero vivo* que puede explorar usted mismo.
>
> ✅ *Simule escenarios*: mueva un control y vea cómo reacciona la planta — por
>    ejemplo, qué pasa si cae la recuperación de oro.
> ✅ *Asistente inteligente*: ante una desviación le indica la *causa probable* y
>    *qué hacer*, anticipando pérdidas antes de que ocurran.
> ✅ *Salud de la planta de un vistazo* (verde / amarillo / rojo).
> ✅ *Calidad de proceso medible* con estándar *Lean Six Sigma*.
> ✅ *Desde cualquier dispositivo*: ábralo en el computador y en el celular,
>    sincronizado.
>
> 👉 [URL]
>
> Quedo atento a sus comentarios para seguir ajustándolo a su operación.

---

> **Nota sobre automatización:** estas plantillas quedan versionadas acá para
> reuso inmediato. El envío automático (WhatsApp Business API / n8n / etc.) es un
> paso aparte; ver "próximos pasos" en Todoist.

---

## 3) Solicitud de datos reales al ingeniero (para alimentar el gemelo)

> Hola [Nombre] 👋
>
> Estoy terminando el tablero del *Gemelo Digital* de la planta. Tiene un *semáforo
> de salud de la planta* con 4 estados (verde→rojo). Te los dejo definidos en
> términos de proceso para que me confirmes los *umbrales reales* y los valores:
>
> *Estados de salud de la planta*
> 🟢 *Bien (nominal):* recuperación en meta, KPIs en rango, sin desviaciones relevantes.
> 🟡 *Cuidado (moderado):* desviación moderada pero controlada — un KPI fuera de
>    rango (p.ej. recuperación unos pts bajo la meta), sin riesgo inmediato.
> 🟠 *Cuidado (significativo):* desviación marcada — varios KPIs fuera de rango o
>    caída clara de recuperación; requiere acción del turno.
> 🔴 *Peligro (crítico):* la planta cerca de un límite inaceptable (LSL) o con
>    riesgo de falla de equipo; una desviación más = pérdida grave / parada.
>
> *Lo que necesito que confirmes (umbrales):*
> • ¿A cuántos *puntos bajo la meta de recuperación* pasamos de Bien → Cuidado → Peligro?
> • ¿Qué otros disparadores son *críticos* (rojo)? (resina saturada, P80 alto, falla
>   de molino, pérdida de cianuro, etc.)
>
> *Y los valores reales (un típico + rango alcanza):*
> • Recuperación de Au: meta (%) y mínimo aceptable / LSL.
> • Ley de cabeza Au (g/t) · Throughput (tpd) · TOC (umbral) · Carga de resina (% y
>   saturación) · P80 (µm) · Au en relaves (g/t) · Disponibilidad (%).
> • Balance: NaCN (kg/t), agua (m³/h), energía (MW), elución (L/día), reposición de
>   resina (L/día).
> • Mezcla de alimentación por tipo de mineral (%) y su recuperación típica.
> • 2-3 causas raíz reales frecuentes del turno (para el asistente IA).
>
> Si tenés un export (Excel/CSV) de las últimas semanas, mejor — lo conecto directo.
> Con esto el tablero pasa de demo a herramienta real de tu operación. ¡Gracias!
