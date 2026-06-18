Este repo es parte del ecosistema OpsNexus. Apenas comience la sesión, antes de esperar instrucciones del usuario, hacé esto y solo esto hasta proponerlo:

1. Leé el checklist del proyecto Todoist que se llama **igual que este repo** (MCP de Todoist: find-projects con el nombre del repo → find-tasks por ese projectId; quedate con las tareas abiertas).
2. Identificá la siguiente tarea **p1 desbloqueada** (respetá dependencias: una decisión/gate abierto bloquea lo que depende de ella; preferí la p1 accionable que no dependa de nada).
3. Proponé al usuario arrancar con ella en **una sola línea**, formato sugerencia (ej.: «¿Arranco con X?»). No ejecutes nada todavía; esperá el OK.

Objetivo: que el usuario no tenga que pensar qué sigue al abrir el repo.

> Para matices propios de este repo (dependencias específicas, contexto de arquitectura, rutas de ADRs), agregalos debajo de esta línea — el hook inyecta el archivo completo.

- **Nombre del proyecto en Todoist**: se llama `DemoCustomerOps` (sin el prefijo `z_` de la carpeta local). Al buscar con find-projects, quitá prefijos locales (`z_`, `-OS`) del basename antes de matchear. ProjectId: `6gvHfx92JRFQM79h`.
- Este repo (`z_DemoCustomerOps`) es material de customer-ops de un engagement de digital twins: docs de propuesta, nota de handoff y un demo de dashboard de digital twin SIGMA (`_dis/`, `_vDemoCustomerOps/`, `web/`).
- Opera bajo el **framework WAT** (Workflows, Agents, Tools): leé el workflow en `workflows/` antes de actuar, reutilizá herramientas existentes en `tools/`, y los secretos viven solo en `.env`. Ver `CLAUDE.md`.
