# 🆘 EMERGENCIA — Volver a la versión estable

Si algo se rompe (la web, un commit malo, archivos editados por error), usa esta guía
para regresar **rápido** a la última versión impecable y respaldada.

> ⚠️ **Repo PÚBLICO.** Nunca subas a Git: `staging/`, `build_*.js`, `tools/`,
> `package*.json`, `_dis/`, `_vDemoCustomerOps/`. Todos están en `.gitignore`
> porque contienen **costos, tarifas y notas internas**. Si los ves "aparecer"
> para commit, **NO los subas**.

---

## ⚓ El ancla estable

La versión "impeque demo para el cliente" está marcada con una **etiqueta (tag) de Git**:

```
ANCLA:  demo-cliente-v1
```

Es un punto congelado en el tiempo. Siempre puedes volver a él.

Ver las anclas disponibles:

```bash
git tag -l
git show demo-cliente-v1   # ver qué incluye
```

---

## 🚑 Rollback rápido (lo más común)

### Caso 1 — "Edité/rompí archivos y aún NO hice commit"

Descarta tus cambios locales y vuelve a como estaba el último commit:

```bash
git restore .            # descarta cambios en archivos trackeados
```

> Esto **NO toca** tus archivos internos ignorados (`staging/`, `build_*.js`, etc.).

### Caso 2 — "Hice un commit malo y quiero deshacerlo"

Deshace el último commit pero **conserva tus cambios** en disco para revisarlos:

```bash
git reset --soft HEAD~1
```

Si quieres botar también los cambios de ese commit:

```bash
git reset --hard HEAD~1
```

### Caso 3 — "Todo se enredó, quiero volver ENTERO al ancla estable"

```bash
git reset --hard demo-cliente-v1
```

Esto deja el repo **exactamente** como el demo del cliente que respaldamos.

> ✅ Seguro: `git reset --hard` **no borra** archivos ignorados/sin trackear
> (tu trabajo interno en `staging/`, `build_*.js`, `tools/` queda intacto).
>
> ❌ **NUNCA uses `git clean -fdx`** en este repo: ese sí borraría tu trabajo
> interno no commiteado.

---

## ☁️ Si ya habías hecho push del error a GitHub

Vuelve la rama `main` remota al ancla (sobrescribe el remoto):

```bash
git reset --hard demo-cliente-v1
git push origin main --force-with-lease
```

`--force-with-lease` es más seguro que `--force`: aborta si alguien más subió algo.

---

## 🔎 Recuperar UN solo archivo del ancla

Si solo quieres restaurar un archivo (ej. el dashboard) sin tocar el resto:

```bash
git checkout demo-cliente-v1 -- web/Dashboard_GemeloDigital_SIGMA.html
```

---

## 🌐 Sobre la web publicada (GitHub Pages)

- Se publica **solo** la carpeta `web/` vía GitHub Actions, en cada push a `main`.
- Tras un rollback + push, el deploy se vuelve a disparar solo (1–2 min).
- Ver estado del deploy: pestaña **Actions** del repo en GitHub, o:

```bash
gh run list --limit 3
```

---

## 🆕 Crear una nueva ancla más adelante

Cuando llegues a otro estado "impecable" que quieras poder recuperar:

```bash
git tag -a demo-cliente-v2 -m "Descripción del hito"
git push origin demo-cliente-v2
```

---

_Última ancla creada: `demo-cliente-v1` — demo del Dashboard SIGMA para el cliente._
