#!/usr/bin/env python3
"""Acortador propio para GitHub Pages: genera stubs de redirect en web/go/.

Registro (fuente de verdad): web/go/links.json
Cada código corto => carpeta web/go/<codigo>/index.html que redirige a la
página destino con sus UTM. El link que se comparte queda corto:

    https://jjuri-socialmining.github.io/_DemoCustomerOps/go/<codigo>

Uso:
    # Crear (o actualizar) un código y regenerar su stub:
    python3 tools/make_shortlink.py add r-ds  --source r  --page ds
    python3 tools/make_shortlink.py add w-acme-ds --source w --page ds --client acme

    # Regenerar TODOS los stubs desde links.json (idempotente):
    python3 tools/make_shortlink.py rebuild

    # Listar los códigos y sus destinos:
    python3 tools/make_shortlink.py list

Convención de códigos: <fuente>[-cliente]-<pagina>   ej. r-ds, li-rag, w-acme-ds
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlencode

REPO = Path(__file__).resolve().parent.parent
GO_DIR = REPO / "web" / "go"
REGISTRY = GO_DIR / "links.json"

BASE_URL = "https://jjuri-socialmining.github.io/_DemoCustomerOps/"

# clave de fuente -> (utm_source, utm_medium)
SOURCES = {
    "r":   ("resume",   "pdf"),
    "w":   ("whatsapp", "chat"),
    "li":  ("linkedin", "social"),
    "web": ("web",      "referral"),
    "em":  ("email",    "email"),
}

# clave de página -> (ruta relativa al site o URL absoluta, utm_content)
# utm_content None = destino sin tracker propio: redirect limpio, sin UTM.
PAGES = {
    "ds":  ("Dashboard_GemeloDigital_SIGMA.html",   "dashboard-sigma"),
    "ds-en": ("Dashboard_DigitalTwin_SIGMA.html",   "dashboard-sigma-en"),
    "rag": ("projects/rag-pipeline-evidence.html",  "rag-evidence"),
    "svc": ("pages/sigma-services-en.html",         "services-en"),
    "home": ("index-en.html",                       "home-en"),
    "kpi": ("",                                     "kpi-panel"),
    "gh":  ("https://github.com/jjuri-socialmining", None),
    "lin": ("https://linkedin.com/in/jjuri-CI-vancouver", None),
    "3d":  ("https://jjuri-socialmining.github.io/miningops-capsule-demo/cic-adsorption-circuit-demo-v2.html", None),
}

STUB = """<!doctype html>
<html lang="es">
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0;url={dest}">
<script>location.replace({dest_js});</script>
<title>Redirigiendo…</title>
<p>Redirigiendo… <a href="{dest}">continuar</a></p>
</html>
"""

DOCS_HTML = GO_DIR / "docs-4b8e2d1.html"
DOCS_MD = GO_DIR / "README.md"

SOURCE_LABELS = {"r": "Resume", "w": "WhatsApp", "li": "LinkedIn",
                 "web": "Internet/otro", "em": "Email"}
PAGE_LABELS = {"ds": "Dashboard SIGMA", "ds-en": "Dashboard SIGMA (EN)",
               "rag": "Evidencia RAG",
               "svc": "Portafolio de servicios (EN)",
               "home": "Landing SIGMA (EN)",
               "kpi": "Landing KPI (ES)",
               "gh": "Perfil GitHub (externo)",
               "lin": "Perfil LinkedIn (externo)",
               "3d": "Demo 3D CIC (externo, sin tracker)"}


def load_registry():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {}


def save_registry(reg):
    GO_DIR.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")


def dest_url(entry):
    path, content = PAGES[entry["page"]]
    base = path if path.startswith("http") else BASE_URL + path
    if content is None:
        return base
    utm_source, utm_medium = SOURCES[entry["source"]]
    params = {
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": entry.get("client", "general"),
        "utm_content": content,
    }
    return base + "?" + urlencode(params)


def write_stub(code, entry):
    dest = dest_url(entry)
    stub_dir = GO_DIR / code
    stub_dir.mkdir(parents=True, exist_ok=True)
    (stub_dir / "index.html").write_text(
        STUB.format(dest=dest, dest_js=json.dumps(dest)), encoding="utf-8")
    return dest


def short_url(code):
    return BASE_URL + "go/" + code


def rows(reg):
    for code, entry in sorted(reg.items()):
        yield {
            "code": code,
            "short": short_url(code),
            "dest": dest_url(entry),
            "source": SOURCE_LABELS.get(entry["source"], entry["source"]),
            "page": PAGE_LABELS.get(entry["page"], entry["page"]),
            "client": entry.get("client", "general"),
        }


def write_docs(reg):
    """Regenera web/go/README.md y la página HTML de documentación desde el registro."""
    lines = [
        "# Links cortos — registro y convención",
        "",
        "Acortador propio sobre GitHub Pages. Cada código es una carpeta",
        "`web/go/<codigo>/` con un redirect instantáneo a la página real con sus UTM;",
        "el tracker (`web/assets/track.js`) captura fuente, campaña y contenido en cada visita.",
        "",
        "**No editar los stubs a mano** — la fuente de verdad es `links.json`;",
        "este README y `docs-4b8e2d1.html` se regeneran con el tool.",
        "",
        "## Convención de códigos",
        "",
        "`<fuente>[-cliente]-<pagina>` — ej. `r-ds`, `li-rag`, `w-acme-ds`",
        "",
        "| Clave | Fuente (`utm_source` / `utm_medium`) |",
        "|---|---|",
    ]
    for k, (s, m) in SOURCES.items():
        lines.append(f"| `{k}` | {SOURCE_LABELS.get(k, k)} — `{s}` / `{m}` |")
    lines += ["", "| Clave | Página (`utm_content`) |", "|---|---|"]
    for k, (path, content) in PAGES.items():
        lines.append(f"| `{k}` | {PAGE_LABELS.get(k, k)} — `{path or '(raíz)'}` (`{content or 'sin UTM'}`) |")
    lines += [
        "",
        "## Links activos",
        "",
        "| Código | Link corto | Fuente | Página | Campaña |",
        "|---|---|---|---|---|",
    ]
    for r in rows(reg):
        lines.append(f"| `{r['code']}` | {r['short']} | {r['source']} | {r['page']} | {r['client']} |")
    lines += [
        "",
        "## Uso del tool",
        "",
        "```bash",
        "python3 tools/make_shortlink.py add w-acme-ds --source w --page ds --client acme",
        "python3 tools/make_shortlink.py list",
        "python3 tools/make_shortlink.py rebuild   # regenera stubs + docs desde links.json",
        "```",
        "",
    ]
    DOCS_MD.write_text("\n".join(lines), encoding="utf-8")

    trs = "\n".join(
        f'<tr><td><code>{r["code"]}</code></td>'
        f'<td><button class="copy" data-url="{r["short"]}">copiar</button> '
        f'<a href="{r["short"]}" rel="noopener">{r["short"].replace(BASE_URL, "…/")}</a></td>'
        f'<td>{r["source"]}</td><td>{r["page"]}</td><td>{r["client"]}</td></tr>'
        for r in rows(reg))
    DOCS_HTML.write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Links cortos — documentación</title>
<meta name="robots" content="noindex, nofollow">
<style>
  :root{{--paper:#F4F6F5;--card:#fff;--ink:#14181B;--muted:#5C6866;--rule:#C3CCCA;--accent:#0B6E5F}}
  @media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
    --paper:#111517;--card:#181D20;--ink:#E9EFEE;--muted:#A7B4B7;--rule:#384346;--accent:#4FBFA8}}}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--paper);color:var(--ink);line-height:1.6;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:24px}}
  main{{max-width:64rem;margin:0 auto}}
  h1{{font-family:ui-serif,Georgia,serif;font-weight:600;font-size:26px;margin:0 0 4px}}
  p{{color:var(--muted);font-size:14.5px;margin:0 0 18px}}
  .tabla{{overflow-x:auto;background:var(--card);border:1px solid var(--rule);border-radius:8px}}
  table{{border-collapse:collapse;width:100%;font-size:14px}}
  th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--rule);white-space:nowrap}}
  th{{color:var(--muted);font-weight:600;font-size:12.5px;text-transform:uppercase;letter-spacing:.04em}}
  tr:last-child td{{border-bottom:0}}
  code{{background:var(--paper);border:1px solid var(--rule);border-radius:4px;padding:1px 6px;font-size:13px}}
  a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
  .copy{{font-size:12px;padding:2px 8px;margin-right:6px;cursor:pointer;border-radius:4px;
    border:1px solid var(--rule);background:var(--card);color:var(--accent)}}
  .nota{{font-size:13px;color:var(--muted);margin-top:16px}}
</style>
</head>
<body>
<main>
<h1>Links cortos</h1>
<p>Redirects <code>go/&lt;codigo&gt;</code> con UTM embebidos. Convención:
<code>&lt;fuente&gt;[-cliente]-&lt;pagina&gt;</code>. Generado desde
<code>links.json</code> — no editar a mano.</p>
<div class="tabla">
<table>
<thead><tr><th>Código</th><th>Link corto</th><th>Fuente</th><th>Página</th><th>Campaña</th></tr></thead>
<tbody>
{trs}
</tbody>
</table>
</div>
<p class="nota">Nuevo link: <code>python3 tools/make_shortlink.py add w-acme-ds --source w --page ds --client acme</code></p>
</main>
<script>
document.addEventListener("click",function(e){{
  var b=e.target.closest(".copy"); if(!b) return;
  navigator.clipboard.writeText(b.dataset.url).then(function(){{
    b.textContent="✓"; setTimeout(function(){{b.textContent="copiar";}},1200);
  }});
}});
</script>
</body>
</html>
""", encoding="utf-8")


def cmd_add(args):
    if args.source not in SOURCES:
        sys.exit(f"fuente desconocida {args.source!r}; opciones: {', '.join(SOURCES)}")
    if args.page not in PAGES:
        sys.exit(f"página desconocida {args.page!r}; opciones: {', '.join(PAGES)}")
    reg = load_registry()
    entry = {"source": args.source, "page": args.page}
    if args.client:
        entry["client"] = args.client
    reg[args.code] = entry
    save_registry(reg)
    dest = write_stub(args.code, entry)
    write_docs(reg)
    print(f"{short_url(args.code)}\n  -> {dest}")


def cmd_rebuild(_args):
    reg = load_registry()
    for code, entry in reg.items():
        write_stub(code, entry)
        print(f"{code}: ok")
    write_docs(reg)
    print(f"{len(reg)} stubs regenerados en {GO_DIR} (+ README.md y docs html)")


def cmd_docs(_args):
    write_docs(load_registry())
    print(f"docs regeneradas: {DOCS_MD} y {DOCS_HTML}")


def cmd_list(_args):
    reg = load_registry()
    for code, entry in sorted(reg.items()):
        print(f"{short_url(code)}\n  -> {dest_url(entry)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="crear/actualizar un código corto")
    p_add.add_argument("code", help="código corto, ej. r-ds")
    p_add.add_argument("--source", required=True, help="|".join(SOURCES))
    p_add.add_argument("--page", required=True, help="|".join(PAGES))
    p_add.add_argument("--client", help="cliente/destinatario (utm_campaign); default: general")
    p_add.set_defaults(func=cmd_add)

    sub.add_parser("rebuild", help="regenerar todos los stubs").set_defaults(func=cmd_rebuild)
    sub.add_parser("list", help="listar códigos").set_defaults(func=cmd_list)
    sub.add_parser("docs", help="regenerar README.md y página html de docs").set_defaults(func=cmd_docs)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
