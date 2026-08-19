#!/usr/bin/env python3
"""gen-costco.py — arma web/costco-ofertas.html con las dos fuentes de ofertas.

  web/data/costco-bodega.json  — instant savings de bodega BC/AB/SK/MB (cocowest.ca)
  web/data/costco-online.tsv   — catalogo online de costco.ca, con link de compra

La pagina es PUBLICA. No debe llevar nada personal: ni codigo postal, ni bodega
asignada, ni historial de compras. Solo precios de retail, que ya son publicos.
"""

import html
import json
import re
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WEB = RAIZ / "web"


def cargar():
    bodega = json.loads((WEB / "data" / "costco-bodega.json").read_text())
    online = []
    for linea in (WEB / "data" / "costco-online.tsv").read_text().splitlines():
        p = linea.split("\t")
        if len(p) != 5:
            continue
        nombre, precio, antes, off, url = p
        m = re.search(r"([\d.]+)", off)
        online.append({
            "nombre": nombre,
            "precio": float(precio),
            "antes": float(antes) if antes else 0.0,
            "ahorro": float(m.group(1)) if m else 0.0,
            "url": url,
        })
    return bodega, online


def fila_bodega(o):
    pct = round(o["ahorro"] / (o["precio"] + o["ahorro"]) * 100) if o["precio"] else 0
    return (
        f'<tr data-nombre="{html.escape(o["nombre"].lower())}">'
        f'<td class="nom">{html.escape(o["nombre"])}<span class="art">#{o["articulo"]}</span></td>'
        f'<td class="ah">-${o["ahorro"]:,.2f}<span class="pct">{pct}%</span></td>'
        f'<td class="pr">${o["precio"]:,.2f}</td>'
        f'<td class="vc">{o["vence"]}</td></tr>'
    )


def fila_online(o):
    pct = round(o["ahorro"] / o["antes"] * 100) if o["antes"] else 0
    link = html.escape("https://www.costco.ca" + o["url"])
    antes = (f'<span class="antes">${o["antes"]:,.2f}</span>'
             if o["antes"] > o["precio"] else "")
    return (
        f'<tr data-nombre="{html.escape(o["nombre"].lower())}">'
        f'<td class="nom"><a href="{link}" target="_blank" rel="noopener">'
        f'{html.escape(o["nombre"])}</a></td>'
        f'<td class="ah">-${o["ahorro"]:,.2f}<span class="pct">{pct}%</span></td>'
        f'<td class="pr">${o["precio"]:,.2f}{antes}</td>'
        f'<td class="vc"><a class="btn" href="{link}" target="_blank" rel="noopener">Comprar</a></td>'
        f'</tr>'
    )


CSS = """
:root {
  --bg:#f6f7f9; --card:#fff; --tx:#14161a; --mut:#6b7280; --bor:#e3e6ea;
  --ac:#005daa; --warn:#b4341c;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:#0f1216; --card:#171b21; --tx:#e8eaed; --mut:#9aa2ad; --bor:#272d36;
    --ac:#5aa9ef; --warn:#f87171;
  }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--tx);
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
.wrap { max-width:1080px; margin:0 auto; padding:24px 16px 64px; }
h1 { font-size:26px; margin:0 0 4px; letter-spacing:-.02em; }
.sub { color:var(--mut); font-size:14px; margin-bottom:20px; }
.stats { display:flex; flex-wrap:wrap; gap:10px; margin-bottom:20px; }
.stat { background:var(--card); border:1px solid var(--bor); border-radius:10px;
  padding:10px 14px; flex:1 1 150px; }
.stat b { display:block; font-size:20px; font-variant-numeric:tabular-nums; }
.stat span { color:var(--mut); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
.tabs { display:flex; gap:6px; margin-bottom:14px; flex-wrap:wrap; }
.tab { background:var(--card); border:1px solid var(--bor); color:var(--tx);
  padding:8px 14px; border-radius:999px; cursor:pointer; font-size:14px; }
.tab[aria-selected="true"] { background:var(--ac); color:#fff; border-color:var(--ac); }
#q { width:100%; padding:11px 14px; border:1px solid var(--bor); border-radius:10px;
  background:var(--card); color:var(--tx); font-size:15px; margin-bottom:14px; }
.panel { background:var(--card); border:1px solid var(--bor); border-radius:12px;
  overflow-x:auto; }
table { width:100%; border-collapse:collapse; min-width:560px; }
th,td { text-align:left; padding:10px 14px; border-bottom:1px solid var(--bor);
  vertical-align:top; }
th { font-size:12px; text-transform:uppercase; letter-spacing:.04em; color:var(--mut);
  position:sticky; top:0; background:var(--card); }
tr:last-child td { border-bottom:none; }
.nom { width:56%; }
.nom a { color:var(--tx); text-decoration:none; }
.nom a:hover { color:var(--ac); text-decoration:underline; }
.art { display:block; color:var(--mut); font-size:12px; font-variant-numeric:tabular-nums; }
.ah { color:var(--warn); font-weight:650; white-space:nowrap; font-variant-numeric:tabular-nums; }
.pct { display:block; font-weight:400; font-size:12px; color:var(--mut); }
.pr { font-weight:650; white-space:nowrap; font-variant-numeric:tabular-nums; }
.antes { display:block; font-weight:400; font-size:12px; color:var(--mut);
  text-decoration:line-through; }
.vc { color:var(--mut); font-size:13px; white-space:nowrap; }
.btn { display:inline-block; background:var(--ac); color:#fff; text-decoration:none;
  padding:6px 12px; border-radius:7px; font-size:13px; }
.nota { margin-top:18px; padding:14px 16px; background:var(--card);
  border:1px solid var(--bor); border-left:3px solid var(--ac); border-radius:8px;
  font-size:13px; color:var(--mut); }
.nota a { color:var(--ac); }
.hidden { display:none; }
"""

JS = """
const tabs = document.querySelectorAll('.tab');
const q = document.getElementById('q');
function filtrar() {
  const t = q.value.trim().toLowerCase();
  document.querySelectorAll('tbody tr').forEach(tr => {
    tr.classList.toggle('hidden', !!t && !tr.dataset.nombre.includes(t));
  });
}
tabs.forEach(b => b.addEventListener('click', () => {
  tabs.forEach(o => o.setAttribute('aria-selected', String(o === b)));
  document.getElementById('p-bodega').classList.toggle('hidden', b.dataset.p !== 'bodega');
  document.getElementById('p-online').classList.toggle('hidden', b.dataset.p !== 'online');
}));
q.addEventListener('input', filtrar);
"""


def main():
    bodega, online = cargar()
    ofb = sorted(bodega["ofertas"], key=lambda o: -o["ahorro"])
    ofo = sorted(online, key=lambda o: -o["ahorro"])
    hoy = date.today().isoformat()
    total_b = sum(o["ahorro"] for o in ofb)
    total_o = sum(o["ahorro"] for o in ofo)
    fuente_b = html.escape(bodega["fuente"])

    filas_b = "\n".join("        " + fila_bodega(o) for o in ofb)
    filas_o = "\n".join("        " + fila_online(o) for o in ofo)

    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Ofertas Costco &middot; BC</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <h1>Ofertas Costco</h1>
  <p class="sub">Columbia Brit&aacute;nica &middot; generado el {hoy}</p>

  <div class="stats">
    <div class="stat"><b>{len(ofb)}</b><span>rebajas en bodega</span></div>
    <div class="stat"><b>{len(ofo)}</b><span>ofertas online</span></div>
    <div class="stat"><b>${total_b:,.0f}</b><span>ahorro total bodega</span></div>
    <div class="stat"><b>${total_o:,.0f}</b><span>ahorro total online</span></div>
  </div>

  <div class="tabs" role="tablist">
    <button class="tab" role="tab" aria-selected="true" data-p="bodega">Bodega ({len(ofb)})</button>
    <button class="tab" role="tab" aria-selected="false" data-p="online">Online &middot; con link ({len(ofo)})</button>
  </div>

  <input id="q" type="search" placeholder="Filtrar por producto... (ej: pollo, caf&eacute;, Dyson)" autocomplete="off">

  <div class="panel" id="p-bodega">
    <table>
      <thead><tr><th>Producto</th><th>Ahorro</th><th>Precio</th><th>Vence</th></tr></thead>
      <tbody>
{filas_b}
      </tbody>
    </table>
  </div>

  <div class="panel hidden" id="p-online">
    <table>
      <thead><tr><th>Producto</th><th>Ahorro</th><th>Precio</th><th></th></tr></thead>
      <tbody>
{filas_o}
      </tbody>
    </table>
  </div>

  <p class="nota">
    <b>Bodega:</b> instant savings de BC/AB/SK/MB seg&uacute;n
    <a href="{fuente_b}" target="_blank" rel="noopener">cocowest.ca</a>, un fan blog no
    oficial que fotograf&iacute;a el flyer. Los precios pueden variar por bodega:
    confirmalo en el local. El t&iacute;tulo del post dice &laquo;2025&raquo; por un error
    del propio blog; las fechas de vencimiento de cada item son las que valen.<br><br>
    <b>Online:</b> tomado de
    <a href="https://www.costco.ca/offers-ending.html" target="_blank" rel="noopener">Offers Ending Sunday</a>
    de costco.ca. Cada fila enlaza a la ficha real del producto. Los precios online no son
    los mismos que en bodega.<br><br>
    P&aacute;gina informativa sin relaci&oacute;n con Costco Wholesale.
  </p>
</div>
<script>{JS}</script>
</body>
</html>
"""
    salida = WEB / "costco-ofertas.html"
    salida.write_text(doc)
    print(f"{salida}  ({len(doc):,} bytes)  bodega={len(ofb)} online={len(ofo)}")


if __name__ == "__main__":
    main()
