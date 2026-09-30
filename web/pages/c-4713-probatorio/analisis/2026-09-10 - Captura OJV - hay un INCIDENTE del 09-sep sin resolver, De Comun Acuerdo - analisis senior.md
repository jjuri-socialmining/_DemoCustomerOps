---
type: documento-digerido
case_id: CHL-2026-C-4713-2025
source: "Captura de pantalla de la OJV — Detalle Causa Civil, pestaña «Escritos por Resolver» (aportada por Jorge)"
sha256: 726e8e1ad03dde33914d77144380a27f257580cea9b3141da0053bb2052dc0a9
md5: 1c899311a030ef93511a5f356a971c02
date_ingested: 2026-09-10
costo_tokens: 0.3k
vault: _ActiveOps/LegalOps/CHL-2026-C-4713-2025/2026-09-10 - Captura OJV - Escritos por Resolver - incidente 09-sep De Comun Acuerdo.png
compartible: solo-interno
privilege_level: confidential
tags: [legal, chile, C-4713, ojv, escritos-por-resolver, incidente, comun-acuerdo, art-64-CPC, franco-anabalon]
---

# 2026-09-10 — La OJV muestra un INCIDENTE del 09-sep sin resolver, y el solicitante dice «De Común Acuerdo»

## Fuente y metadata

Captura de pantalla del **Detalle Causa Civil** de la Oficina Judicial Virtual, con la pestaña
**«Escritos por Resolver»** seleccionada. Aportada por Jorge el 2026-09-10.

⚠️ **La captura es el puntero, no la fuente.** Muestra la *fila* del escrito, no su contenido: el
documento en sí está detrás del ícono «Doc.» y **no fue descargado**. Todo lo que sigue distingue
lo que la captura **dice** de lo que **no dice**.

## Qué muestra — leído literal

### Cabecera de la causa

| Campo | Valor |
|---|---|
| ROL | C-4713-2025 |
| F. Ing. | 01/04/2025 |
| Caratulado | JURI/ARAYA |
| Est. Adm. | Sin archivar |
| Proc. | **Sumario** |
| Estado Proc. | Tramitación |
| **Etapa** | **2 Aud.Contes.y Concil./Recib. a prueba** |
| **Ubicación** | 🔴 **Corte de Apelaciones** |
| Tribunal | 3° Juzgado Civil de Santiago |

Disponibles para descarga: **Texto Demanda** (PDF) · **Anexos de la causa** (carpeta) ·
**Certificado de Envío** (PDF) · **Ebook** (PDF). Cuaderno: `1 - Principal`.

### 🔥 La tabla «Escritos por Resolver» — una sola fila

| Doc. | Anexo | Fecha de Ingreso | Tipo Escrito | Solicitante |
|---|---|---|---|---|
| 📄 | *(vacío)* | **09/09/2026** | **Incidente** | **De Común Acuerdo** |

---

## Por qué esta fila importa, y no es un detalle de trámite

Tres hechos que se cruzan, y el cruce es el hallazgo:

1. **El 04-09-2026 Franco presentó el folio 48** pidiendo *«dar curso progresivo a los autos»*
   → [[2026-09-08 - Folio 48 y resolucion - AUTOS PARA RESOLVER en rebeldia de la demandante - analisis senior]]
2. **El 08-09-2026 el tribunal proveyó**: *«Dando curso progresivo, autos para resolver»*.
3. **El 09-09-2026 —al día siguiente— ingresa un «Incidente»** que hoy sigue **sin resolver**.

🔴 **Y la postura declarada de Franco en esta causa es exactamente la contraria a un incidente.**
Jorge lo confirmó el 2026-09-10: *«Franco en ese caso no quería más incidencias, que avance»*.
Eso es coherente con todo el registro previo — el folio 48 pide literalmente curso progresivo, y
el propio repo ya tenía destilado que en C-4713 Franco defendió el procedimiento sumario **tres
veces** contra intentos de ensancharlo, con escritos de dos páginas y secos.

**Un «Incidente» ingresado al día siguiente de «autos para resolver» va en dirección opuesta a esa
estrategia.** Ese es el punto que obliga a abrir el documento.

## ⚠️ Qué puede ser — hipótesis, NINGUNA verificada

Se listan porque orientan qué buscar, **no** porque se sepa cuál es. La captura no permite
decidir entre ellas.

| Hipótesis | Qué implicaría | Señal a favor |
|---|---|---|
| **Suspensión del procedimiento de común acuerdo** (art. 64 CPC) | 🔴 La causa **se detiene**, justo cuando acababa de retomar curso. Contradice «que avance» | Es el escrito «De Común Acuerdo» más frecuente |
| Avenimiento / conciliación parcial | Habría negociación en curso que Jorge debe conocer | La etapa registra «Aud. Contes. y Concil.» |
| Gestión conjunta sobre el probatorio | Neutro o bueno | El folio 43 está en «autos para resolver» |
| Etiqueta del sistema, no acuerdo real | Nada; sería ruido de la OJV | El campo «Solicitante» de la OJV no siempre refleja autoría |

⛔ **No se elige ninguna acá.** Escribir cuál es sin el PDF sería inventar, y sobre una causa que
Jorge lleva con un patrocinante que tiene estrategia declarada.

## Clasificación honesta

**Qué ES:** una **captura de estado de la OJV** en un instante — el equivalente a una foto del
tablero. Sirve para saber **que** existe un escrito pendiente y **desde cuándo**.

**Qué NO es:** no es el escrito, no es una resolución, y **no prueba el contenido de nada**. Su
valor es de alerta, no probatorio.

**Autoridad:** alta para lo que muestra (es la interfaz oficial del PJUD), nula para lo que no
muestra.

**Vigencia:** ⚠️ **se vence rápido.** Una captura de «Escritos por Resolver» describe un momento;
en cuanto el tribunal provea, la fila desaparece de esa pestaña y pasa a Historia.

## Lo que NO consta

1. 🔴 **Qué dice el escrito del 09-09-2026.** Es la única pregunta que importa.
2. **Quién lo presentó de verdad.** «De Común Acuerdo» sugiere ambas partes, pero **no está
   verificado** que Franco lo haya firmado ni que Jorge lo supiera.
3. **Qué número de folio le tocó** — la captura no lo muestra.
4. **Si el folio 43 ya se resolvió.** La pestaña abierta es «Escritos por Resolver», no
   «Historia»; el estado del folio 43 **no se ve en esta captura**.
5. **Qué se está viendo en la Corte de Apelaciones.** La `Ubicación: Corte de Apelaciones` es
   consistente con la apelación de la sustitución de procedimiento (ing. 15942-2025, solo efecto
   devolutivo), pero la captura no lo dice.

## Pendientes

1. 🔴 ⬜ **Bajar el escrito del 09-09-2026** desde el ícono «Doc.» de esa fila. **Es la tarea
   número uno de esta causa.** Sin él no se sabe si la causa avanza o acaba de detenerse.
2. 🔴 ⬜ **Preguntarle a Franco por ese escrito** — un tema, una pregunta decidible, ventana
   7-9 AM Chile: *¿qué es el incidente que ingresó el 9 de septiembre y quién lo presentó?*
   ⛔ No mezclarlo con el probatorio ni con el abandono en el mismo mensaje.
3. ⬜ **Bajar también el Ebook y los Anexos** — están disponibles en esta misma pantalla y el
   expediente digerido en el repo es del **14-07-2026**, ya desactualizado.
4. ⬜ **Verificar en «Historia» si el folio 43 se resolvió** — no se ve acá.
5. ⬜ Si resulta ser suspensión de común acuerdo: **recalcular el efecto sobre el abandono**, que
   con el folio 48 había quedado despejado hasta ~08-03-2027.

---

Ver: [[2026-09-08 - Folio 48 y resolucion - AUTOS PARA RESOLVER en rebeldia de la demandante - analisis senior]] ·
[[Case_Metadata]] · [[Decision_Log]] · [[franco-anabalon-rol-limitado]]
