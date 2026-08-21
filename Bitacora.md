# Bitácora — DemoCustomerOps

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
