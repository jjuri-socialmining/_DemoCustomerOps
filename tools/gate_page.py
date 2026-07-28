#!/usr/bin/env python3
"""
gate_page.py — Deja una página detrás de una clave, cifrando su contenido.

Uso:
    python3 tools/gate_page.py <input.html> --password CLAVE [opciones]

    python3 tools/gate_page.py web/informe/index.html --password 6511
    python3 tools/gate_page.py borrador.html -p "Laso-2026" -o web/caso/index.html
    python3 tools/gate_page.py nota.html -p 1234 --attach informe.pdf --label "Descargar informe"

No es una pantalla que tapa el contenido: el HTML resultante **solo transporta
texto cifrado**. Sin la clave no hay nada legible en el código fuente, que es la
diferencia entre esto y un `prompt()` de JavaScript.

    Cifrado   AES-256-GCM
    Clave     PBKDF2-SHA256, 600.000 iteraciones por defecto, salt aleatorio
    Descifra  el navegador de quien entra, vía Web Crypto. Sin red, sin servidor.

⚠️  La fuerza real la da la clave, no el algoritmo. Cuatro dígitos son diez mil
    combinaciones y se recorren con un script: eso frena al que llega de
    casualidad, no al que va a buscar. Para material sensible, usar una frase.

Requiere: cryptography  (pip install cryptography)
"""

import argparse
import base64
import os
import re
import sys
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

DEFAULT_ITERATIONS = 600_000

# Estilo mínimo para la portada, sólo si la página no trae el suyo.
FALLBACK_CSS = """
  :root{--ground:#E9EBE8;--surface:#FCFCFB;--surface-2:#F1F3F0;--ink:#15191A;
    --ink-2:#4E585B;--ink-3:#798488;--rule:#CBD1CD;--oxide:#9C3A2C;
    --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
  @media (prefers-color-scheme:dark){:root{--ground:#111415;--surface:#191D1E;
    --surface-2:#222728;--ink:#E7EAE8;--ink-2:#A5AFB1;--ink-3:#7C8688;
    --rule:#323839;--oxide:#E08471}}
  *{box-sizing:border-box}
  body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);line-height:1.6}
  .eyebrow{font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;
    text-transform:uppercase;color:var(--ink-3)}
"""

GATE_TEMPLATE = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>__TITLE__</title>
<style>__CSS__
  .gate{min-height:100vh;display:grid;place-items:center;padding:1.5rem}
  .gate form{background:var(--surface);border:1px solid var(--rule);padding:2rem 1.9rem;
    max-width:24rem;width:100%;display:flex;flex-direction:column;gap:1rem}
  .gate h1{font-size:1.35rem;margin:0}
  .gate p{font-size:.9rem;color:var(--ink-2);margin:0}
  .gate input{font-family:var(--mono);font-size:1.3rem;letter-spacing:.35em;text-align:center;
    padding:.7rem;border:1px solid var(--rule);background:var(--surface-2);color:var(--ink);width:100%}
  .gate input:focus{outline:2px solid var(--oxide);outline-offset:1px}
  .gate button{font-family:var(--mono);font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;
    font-weight:700;padding:.75rem;border:1px solid var(--oxide);background:var(--oxide);
    color:var(--surface);cursor:pointer}
  .gate button:disabled{opacity:.55;cursor:wait}
  .gate button:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
  .gate .err{color:var(--oxide);font-size:.85rem;min-height:1.2em;margin:0}
</style></head><body>
<div class="gate"><form id="f">
  <div class="eyebrow">__EYEBROW__</div>
  <h1>__HEADING__</h1>
  <p>__PROMPT__</p>
  <input id="p" type="password" inputmode="__INPUTMODE__" autocomplete="off" aria-label="Clave">
  <button id="b" type="submit">Abrir</button>
  <p class="err" id="e" role="status"></p>
</form></div>
<script>
const S="__SALT__",N="__NONCE__",C="__CT__",IT=__ITER__;
const dec=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
document.getElementById("f").addEventListener("submit",async ev=>{
  ev.preventDefault();
  const b=document.getElementById("b"),e=document.getElementById("e");
  b.disabled=true; e.textContent="Abriendo\\u2026";
  try{
    const km=await crypto.subtle.importKey("raw",
      new TextEncoder().encode(document.getElementById("p").value),"PBKDF2",false,["deriveKey"]);
    const k=await crypto.subtle.deriveKey(
      {name:"PBKDF2",salt:dec(S),iterations:IT,hash:"SHA-256"},km,
      {name:"AES-GCM",length:256},false,["decrypt"]);
    const pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:dec(N)},k,dec(C));
    document.body.innerHTML=new TextDecoder().decode(pt);
    window.scrollTo(0,0);
  }catch(_){ e.textContent="Clave incorrecta."; b.disabled=false; }
});
document.getElementById("p").focus();
</script></body></html>
"""


def split_document(html: str) -> tuple[str, str, str]:
    """Separa (título, css, cuerpo). Acepta documento completo o fragmento."""
    title = ""
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if m:
        title = m.group(1).strip()
        html = html[: m.start()] + html[m.end() :]

    css = ""
    for m in list(re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)):
        css += m.group(1)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S | re.I)

    # Nos quedamos sólo con lo que iría dentro de <body>.
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S | re.I)
    if m:
        html = m.group(1)
    else:
        html = re.sub(r"</?(?:!doctype|html|head|meta|link)[^>]*>", "", html, flags=re.I)

    return title, css, html.strip()


def attachment_block(pdf: Path, label: str) -> str:
    data = base64.b64encode(pdf.read_bytes()).decode()
    size = pdf.stat().st_size // 1024
    return (
        '<div style="margin:1.2rem 0">'
        f'<a href="data:application/pdf;base64,{data}" download="{pdf.name}" '
        'style="display:inline-flex;gap:.5rem;align-items:center;text-decoration:none;'
        'font-family:var(--mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;'
        'font-weight:600;color:var(--oxide);border:1px solid var(--oxide);padding:.55rem .85rem">'
        f"&#8595;&nbsp; {label}</a>"
        f'<span style="font-family:var(--mono);font-size:.7rem;color:var(--ink-3);'
        f'margin-left:.6rem">{size} KB</span></div>'
    )


def gate(html: str, password: str, iterations: int, opts) -> str:
    title, css, body = split_document(html)
    if opts.attach:
        body = attachment_block(Path(opts.attach), opts.attach_label) + body

    salt, nonce = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations
    ).derive(password.encode("utf-8"))
    ciphertext = AESGCM(key).encrypt(nonce, body.encode("utf-8"), None)

    page = GATE_TEMPLATE
    for token, value in {
        "__TITLE__": opts.title or title or "Documento reservado",
        "__CSS__": css or FALLBACK_CSS,
        "__EYEBROW__": opts.eyebrow,
        "__HEADING__": opts.heading,
        "__PROMPT__": opts.prompt,
        "__INPUTMODE__": "numeric" if password.isdigit() else "text",
        "__SALT__": base64.b64encode(salt).decode(),
        "__NONCE__": base64.b64encode(nonce).decode(),
        "__ITER__": str(iterations),
        "__CT__": base64.b64encode(ciphertext).decode(),
    }.items():
        page = page.replace(token, value)
    return page


def verify(page: str, password: str, canary: str) -> bool:
    """Descifra como lo haría el navegador y confirma que el contenido volvió."""
    grab = lambda name: re.search(rf'{name}="([^"]*)"', page).group(1)
    salt, nonce, ct = (base64.b64decode(grab(n)) for n in ("S", "N", "C"))
    iters = int(re.search(r"IT=(\d+)", page).group(1))
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iters
    ).derive(password.encode("utf-8"))
    return canary in AESGCM(key).decrypt(nonce, ct, None).decode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("input", type=Path, help="archivo .html de origen")
    ap.add_argument("-p", "--password", required=True, help="clave de acceso")
    ap.add_argument("-o", "--out", type=Path, help="salida (por defecto, sobrescribe el input)")
    ap.add_argument("--iterations", type=int, default=DEFAULT_ITERATIONS)
    ap.add_argument("--title", help="título del navegador; por defecto, el de la página")
    ap.add_argument("--eyebrow", default="Documento privado", help="línea superior de la portada")
    ap.add_argument("--heading", default="Documento reservado")
    ap.add_argument("--prompt", default="Ingresa la clave para abrir el documento.")
    ap.add_argument("--attach", help="PDF a incrustar dentro del contenido cifrado")
    ap.add_argument("--attach-label", default="Descargar PDF")
    args = ap.parse_args()

    if not args.input.is_file():
        print(f"ERROR: no existe {args.input}", file=sys.stderr)
        return 1
    if args.attach and not Path(args.attach).is_file():
        print(f"ERROR: no existe el adjunto {args.attach}", file=sys.stderr)
        return 1

    source = args.input.read_text(encoding="utf-8")
    page = gate(source, args.password, args.iterations, args)

    # Gemba: no basta con que cifre — hay que ver que descifre y que no se filtre.
    # El canario tiene que salir del TEXTO, no del marcado: un nombre de clase como
    # "masthead" vive también en el CSS, que no se cifra, y daría una fuga falsa.
    _, css_kept, body_only = split_document(source)
    plain_text = re.sub(r"<[^>]+>", " ", body_only)
    reserved = css_kept + GATE_TEMPLATE
    canary = next(
        (
            w
            for w in re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{7,}", plain_text)
            if w not in reserved
        ),
        None,
    )
    if canary:
        if not verify(page, args.password, canary):
            print("ERROR: el contenido cifrado no se recupera con esa clave", file=sys.stderr)
            return 1
        if canary in page:
            print("ERROR: quedó contenido en claro en el HTML", file=sys.stderr)
            return 1

    out = args.out or args.input
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")

    print(f"✓ {out}  ({out.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"  clave: {args.password}  ·  PBKDF2-SHA256 × {args.iterations:,}  ·  AES-256-GCM")
    if canary:
        print("  verificado: descifra con la clave y no deja texto en claro")
    if len(args.password) < 8:
        print(
            f"  ⚠️  clave corta ({len(args.password)} caracteres): frena al curioso, "
            "no a quien pruebe combinaciones con un script"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
