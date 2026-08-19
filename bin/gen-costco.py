#!/usr/bin/env python3
"""gen-costco.py — arma web/costco-ofertas.html: mosaico de ofertas con fotos.

Fuentes (ambas en web/data/):
  costco-bodega.json — instant savings de bodega BC/AB/SK/MB (cocowest.ca),
                       con la foto que el blog publica de cada cartel
  costco-online.tsv  — catalogo online de costco.ca via la API gdx-api, con
                       foto oficial, categoria y link de compra

La pagina es PUBLICA. No debe llevar nada personal: ni codigo postal, ni bodega
asignada, ni historial de compras. Solo precios de retail, que ya son publicos.

Las fotos NO se copian al repo (serian ~350 archivos): se enlazan al host de
origen con loading=lazy. Si alguno bloquea el hotlink, la tarjeta cae al
placeholder y el resto de la info sigue sirviendo.
"""

import html
import json
import re
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WEB = RAIZ / "web"

CDN = "https://bfasset.costco-static.com/"
IMG_Q = "?auto=webp&format=jpg&width=400&height=400&fit=bounds&canvas=400,400"

# La bodega viene sin categoria: cocowest solo da nombre y precio. Se infiere por
# palabra clave, con el mismo vocabulario que usa Costco online para que los dos
# catalogos filtren por las mismas etiquetas.
REGLAS = [
    ("Mascotas", r"\bDOG\b|\bCAT\b|PET |PUPPY|KITTEN|LITTER|GREENIES|PURINA|IAMS"),
    ("Electronica", r"\bTV\b|LED|QLED|OLED|SOUNDBAR|HEADPHONE|EARBUD|SPEAKER|BATTER|"
                    r"CAMERA|DRONE|TABLET|IPAD|GALAXY|ECHO|ROKU|XBOX|PLAYSTATION|CHARGER"),
    ("Computacion", r"LAPTOP|DESKTOP|MONITOR|CHROMEBOOK|PRINTER|SSD|ROUTER|KEYBOARD|"
                    r"OMNIBOOK|IDEAPAD|MACBOOK|NOTEBOOK|PC\b"),
    ("Electrodomesticos", r"VACUUM|DISHWASHER|FRIDGE|REFRIGERAT|WASHER|DRYER|MICROWAVE|"
                          r"AIR FRYER|BLENDER|COFFEE MAKER|KETTLE|TOASTER|MIXER|"
                          r"ROBOT|STEAM|IRON\b|PURIFIER|HUMIDIFIER|PORTABLE AC|FAN\b"),
    ("Salud y belleza", r"SHAMPOO|CONDITIONER|LOTION|CREAM|SERUM|VITAMIN|SUPPLEMENT|"
                        r"TOOTHPASTE|TOOTHBRUSH|RAZOR|SHAVER|SOAP|BODY WASH|DEODORANT|"
                        r"SUNSCREEN|MASSAGE|COLLAGEN|PROBIOTIC|ADVIL|TYLENOL|OMEGA"),
    ("Ropa y equipaje", r"MEN'S|WOMEN'S|MENS|WOMENS|KIDS|SHOE|SOCK|JACKET|SWEATER|"
                        r"HOODIE|SHIRT|PANT|JEAN|LEGGING|DRESS|LUGGAGE|BACKPACK|"
                        r"SANDAL|BOOT|SLIPPER|BRA\b|UNDERWEAR|PYJAMA|PAJAMA"),
    ("Hogar y cocina", r"PILLOW|DUVET|SHEET|TOWEL|BLANKET|MATTRESS TOPPER|COOKWARE|"
                       r"\bPAN\b|\bPOT\b|KNIFE|STORAGE|HANGER|CURTAIN|RUG\b|LAMP|"
                       r"DETERGENT|TIDE|BOUNCE|PAPER TOWEL|TOILET PAPER|GARBAGE BAG|"
                       r"CLOROX|LYSOL|DISH SOAP"),
    ("Muebles y colchones", r"MATTRESS|SOFA|SECTIONAL|RECLINER|CHAIR|DESK\b|TABLE|"
                            r"DRESSER|BED FRAME|CABINET|BOOKCASE"),
    ("Patio y jardin", r"PATIO|GAZEBO|BBQ|GRILL|FIRE TABLE|LAWN|GARDEN|PLANTER|"
                       r"UMBRELLA|COOLER|CAMPING|TENT"),
    ("Deportes", r"BIKE|BICYCLE|TREADMILL|WEIGHT|YOGA|GOLF|KAYAK|SAUNA|FITNESS|"
                 r"DUMBBELL|SKI\b|SNOWBOARD|HOCKEY"),
    ("Ferreteria", r"DRILL|TOOL|LADDER|SHELVING|PAINT|HOSE|GENERATOR|CEILING FAN|"
                   r"LIGHTING|BULB|LED SHOP"),
    ("Automotriz", r"TIRE|MOTOR OIL|WIPER|CAR WASH|AUTOMOTIVE|MEGUIAR"),
    ("Juguetes", r"\bTOY\b|LEGO|PUZZLE|GAME\b|DOLL|PLAYSET|BARBIE|NERF"),
]


def categorizar(nombre):
    n = nombre.upper()
    for etiqueta, patron in REGLAS:
        if re.search(patron, n):
            return etiqueta
    return "Supermercado"


def cargar():
    bodega = json.loads((WEB / "data" / "costco-bodega.json").read_text())
    items = []

    for o in bodega["ofertas"]:
        items.append({
            "n": o["nombre"].title(),
            "precio": o["precio"],
            "antes": o["precio"] + o["ahorro"],
            "ahorro": o["ahorro"],
            "vence": o["vence"],
            "img": o.get("foto", ""),
            "url": "",
            "cat": categorizar(o["nombre"]),
            "src": "bodega",
            "id": "b" + o["articulo"],
        })

    for linea in (WEB / "data" / "costco-online.tsv").read_text().splitlines():
        p = linea.split("\t")
        if len(p) != 7:
            continue
        nombre, precio, antes, off, url, img, cat = p
        items.append({
            "n": nombre,
            "precio": float(precio),
            "antes": float(antes),
            "ahorro": float(off),
            "vence": "",
            "img": CDN + img + IMG_Q if img else "",
            "url": "https://www.costco.ca" + url,
            "cat": cat,
            "src": "online",
            "id": "o" + url.rsplit("/", 1)[-1],
        })

    return bodega, items


def tarjeta(it):
    pct = round(it["ahorro"] / it["antes"] * 100) if it["antes"] else 0
    esc = html.escape
    foto = (f'<img src="{esc(it["img"])}" alt="" loading="lazy" decoding="async" '
            f'referrerpolicy="no-referrer" onerror="this.closest(\'.ph\').classList.add(\'sinfoto\')">'
            if it["img"] else "")
    pie = (f'<a class="btn" href="{esc(it["url"])}" target="_blank" rel="noopener">Comprar</a>'
           if it["url"] else
           f'<span class="vence">vence {it["vence"]}</span>')
    return (
        f'<article class="card" data-n="{esc(it["n"].lower())}" data-cat="{esc(it["cat"])}"'
        f' data-src="{it["src"]}" data-ah="{it["ahorro"]}" data-pr="{it["precio"]}"'
        f' data-id="{esc(it["id"])}">'
        f'<div class="ph">{foto}<span class="badge">-{pct}%</span>'
        f'<button class="fav" type="button" aria-label="Guardar en la lista">&#9825;</button></div>'
        f'<div class="body"><h3>{esc(it["n"])}</h3>'
        f'<p class="precio">${it["precio"]:,.2f}'
        f'<span class="antes">${it["antes"]:,.2f}</span></p>'
        f'<p class="ah">ahorras ${it["ahorro"]:,.2f}</p>'
        f'<div class="pie">{pie}</div></div></article>'
    )


CSS = """
:root{--bg:#f5f6f8;--card:#fff;--tx:#14161a;--mut:#6b7280;--bor:#e3e6ea;
  --ac:#005daa;--warn:#c0392b;--fav:#d6336c;--sh:0 1px 3px rgba(0,0,0,.07);}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0f1216;--card:#171b21;--tx:#e8eaed;--mut:#9aa2ad;--bor:#272d36;
  --ac:#5aa9ef;--warn:#f87171;--fav:#f472b6;--sh:0 1px 3px rgba(0,0,0,.4);}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1240px;margin:0 auto;padding:22px 16px 72px}
h1{font-size:26px;margin:0 0 3px;letter-spacing:-.02em}
.sub{color:var(--mut);font-size:14px;margin:0 0 18px}
.stats{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:18px}
.stat{background:var(--card);border:1px solid var(--bor);border-radius:10px;
  padding:9px 13px;flex:1 1 140px}
.stat b{display:block;font-size:19px;font-variant-numeric:tabular-nums}
.stat span{color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.05em}
.barra{position:sticky;top:0;z-index:20;background:var(--bg);
  padding:10px 0 12px;border-bottom:1px solid var(--bor);margin-bottom:18px}
.fila{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.fila+.fila{margin-top:9px}
#q{flex:1 1 240px;padding:10px 13px;border:1px solid var(--bor);border-radius:9px;
  background:var(--card);color:var(--tx);font-size:15px}
select{padding:10px 12px;border:1px solid var(--bor);border-radius:9px;
  background:var(--card);color:var(--tx);font-size:14px}
.chip{background:var(--card);border:1px solid var(--bor);color:var(--tx);
  padding:6px 12px;border-radius:999px;cursor:pointer;font-size:13px;white-space:nowrap}
.chip[aria-pressed="true"]{background:var(--ac);color:#fff;border-color:var(--ac)}
.chip.fv[aria-pressed="true"]{background:var(--fav);border-color:var(--fav)}
.cuenta{color:var(--mut);font-size:13px;margin:0 0 12px}
.grid{display:grid;gap:14px;
  grid-template-columns:repeat(auto-fill,minmax(196px,1fr))}
.card{background:var(--card);border:1px solid var(--bor);border-radius:12px;
  overflow:hidden;box-shadow:var(--sh);display:flex;flex-direction:column}
.ph{position:relative;aspect-ratio:1;background:#fff;display:flex;
  align-items:center;justify-content:center;overflow:hidden}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .ph{background:#f2f2f2}}
.ph img{width:100%;height:100%;object-fit:contain;padding:8px}
.ph.sinfoto::after{content:"sin foto";color:#9aa2ad;font-size:12px}
.ph.sinfoto img{display:none}
.badge{position:absolute;left:8px;top:8px;background:var(--warn);color:#fff;
  font-size:12px;font-weight:650;padding:3px 8px;border-radius:6px}
.fav{position:absolute;right:7px;top:7px;width:32px;height:32px;border-radius:50%;
  border:1px solid var(--bor);background:rgba(255,255,255,.92);color:var(--fav);
  font-size:17px;line-height:1;cursor:pointer;display:flex;align-items:center;
  justify-content:center;padding:0}
.fav:hover{transform:scale(1.08)}
.fav[aria-pressed="true"]{background:var(--fav);color:#fff;border-color:var(--fav)}
.body{padding:11px 12px 12px;display:flex;flex-direction:column;flex:1;gap:3px}
.body h3{font-size:13px;font-weight:550;margin:0;line-height:1.35;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.precio{margin:4px 0 0;font-size:17px;font-weight:700;font-variant-numeric:tabular-nums}
.antes{font-weight:400;font-size:12px;color:var(--mut);text-decoration:line-through;
  margin-left:6px}
.ah{margin:0;font-size:12px;color:var(--warn);font-weight:600}
.pie{margin-top:auto;padding-top:9px}
.btn{display:block;text-align:center;background:var(--ac);color:#fff;
  text-decoration:none;padding:7px 10px;border-radius:7px;font-size:13px;font-weight:550}
.vence{color:var(--mut);font-size:12px}
.vacio{padding:44px 16px;text-align:center;color:var(--mut)}
.nota{margin-top:26px;padding:14px 16px;background:var(--card);border:1px solid var(--bor);
  border-left:3px solid var(--ac);border-radius:8px;font-size:13px;color:var(--mut)}
.nota a{color:var(--ac)}
.hidden{display:none}
"""

JS = """
const $ = s => document.querySelector(s);
const cards = [...document.querySelectorAll('.card')];
const LS = 'costco-wishlist';
let lista = new Set(JSON.parse(localStorage.getItem(LS) || '[]'));
let cat = 'todas', fuente = 'todas', soloFav = false;

function guardar(){ localStorage.setItem(LS, JSON.stringify([...lista])); }

function pintarFav(){
  cards.forEach(c => {
    const on = lista.has(c.dataset.id);
    const b = c.querySelector('.fav');
    b.setAttribute('aria-pressed', on);
    b.innerHTML = on ? '&#9829;' : '&#9825;';
  });
  $('#nfav').textContent = lista.size;
  $('#fav-chip').setAttribute('aria-pressed', soloFav);
}

function aplicar(){
  const q = $('#q').value.trim().toLowerCase();
  let n = 0;
  cards.forEach(c => {
    const ok = (!q || c.dataset.n.includes(q))
      && (cat === 'todas' || c.dataset.cat === cat)
      && (fuente === 'todas' || c.dataset.src === fuente)
      && (!soloFav || lista.has(c.dataset.id));
    c.classList.toggle('hidden', !ok);
    if (ok) n++;
  });
  $('#cuenta').textContent = n + (n === 1 ? ' producto' : ' productos');
  $('#vacio').classList.toggle('hidden', n > 0);
}

function ordenar(){
  const modo = $('#orden').value;
  const g = $('#grid');
  const orden = [...cards].sort((a, b) => {
    if (modo === 'ahorro') return b.dataset.ah - a.dataset.ah;
    if (modo === 'precio') return a.dataset.pr - b.dataset.pr;
    if (modo === 'precio-desc') return b.dataset.pr - a.dataset.pr;
    return a.dataset.n.localeCompare(b.dataset.n);
  });
  orden.forEach(c => g.appendChild(c));
}

document.addEventListener('click', e => {
  const f = e.target.closest('.fav');
  if (f) {
    const id = f.closest('.card').dataset.id;
    lista.has(id) ? lista.delete(id) : lista.add(id);
    guardar(); pintarFav(); if (soloFav) aplicar();
    return;
  }
  const ch = e.target.closest('.chip');
  if (!ch) return;
  if (ch.id === 'fav-chip') { soloFav = !soloFav; pintarFav(); aplicar(); return; }
  const grupo = ch.dataset.grupo;
  document.querySelectorAll(`.chip[data-grupo="${grupo}"]`)
    .forEach(o => o.setAttribute('aria-pressed', o === ch));
  if (grupo === 'cat') cat = ch.dataset.v; else fuente = ch.dataset.v;
  aplicar();
});

$('#q').addEventListener('input', aplicar);
$('#orden').addEventListener('change', ordenar);
$('#limpiar').addEventListener('click', () => {
  lista.clear(); guardar(); pintarFav(); aplicar();
});

ordenar(); pintarFav(); aplicar();
"""


def main():
    bodega, items = cargar()
    items.sort(key=lambda i: -i["ahorro"])
    hoy = date.today().isoformat()

    nb = sum(1 for i in items if i["src"] == "bodega")
    no = sum(1 for i in items if i["src"] == "online")
    ahorro_total = sum(i["ahorro"] for i in items)
    con_foto = sum(1 for i in items if i["img"])

    cats = sorted({i["cat"] for i in items})
    chips_cat = '<button class="chip" data-grupo="cat" data-v="todas" aria-pressed="true">Todas</button>'
    chips_cat += "".join(
        f'<button class="chip" data-grupo="cat" data-v="{html.escape(c)}" '
        f'aria-pressed="false">{html.escape(c)}'
        f' <small>{sum(1 for i in items if i["cat"] == c)}</small></button>'
        for c in cats)

    tarjetas = "\n".join(tarjeta(i) for i in items)
    fuente_b = html.escape(bodega["fuente"])

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
  <p class="sub">Columbia Brit&aacute;nica &middot; {hoy} &middot; {con_foto} de {len(items)} con foto</p>

  <div class="stats">
    <div class="stat"><b>{len(items)}</b><span>ofertas</span></div>
    <div class="stat"><b>{nb}</b><span>en bodega</span></div>
    <div class="stat"><b>{no}</b><span>online con link</span></div>
    <div class="stat"><b>${ahorro_total:,.0f}</b><span>ahorro sumado</span></div>
    <div class="stat"><b id="nfav">0</b><span>en mi lista</span></div>
  </div>

  <div class="barra">
    <div class="fila">
      <input id="q" type="search" placeholder="Buscar producto... (pollo, caf&eacute;, Dyson)" autocomplete="off">
      <select id="orden" aria-label="Ordenar">
        <option value="ahorro">Mayor ahorro</option>
        <option value="precio">Precio: menor a mayor</option>
        <option value="precio-desc">Precio: mayor a menor</option>
        <option value="nombre">Nombre A-Z</option>
      </select>
      <button class="chip fv" id="fav-chip" aria-pressed="false">&#9825; Mi lista</button>
      <button class="chip" id="limpiar" type="button">Vaciar lista</button>
    </div>
    <div class="fila">
      <button class="chip" data-grupo="src" data-v="todas" aria-pressed="true">Todo</button>
      <button class="chip" data-grupo="src" data-v="bodega" aria-pressed="false">Bodega <small>{nb}</small></button>
      <button class="chip" data-grupo="src" data-v="online" aria-pressed="false">Online <small>{no}</small></button>
    </div>
    <div class="fila">{chips_cat}</div>
  </div>

  <p class="cuenta" id="cuenta"></p>
  <div class="grid" id="grid">
{tarjetas}
  </div>
  <p class="vacio hidden" id="vacio">Nada coincide con ese filtro.</p>

  <p class="nota">
    <b>Bodega ({nb}):</b> instant savings de BC/AB/SK/MB seg&uacute;n
    <a href="{fuente_b}" target="_blank" rel="noopener">cocowest.ca</a>, un fan blog no
    oficial que fotograf&iacute;a el flyer. Los precios pueden variar por bodega:
    confirmalo en el local. El t&iacute;tulo del post dice &laquo;2025&raquo; por un error
    del propio blog; valen las fechas de vencimiento de cada item. Estos no tienen link
    de compra porque no se venden online.<br><br>
    <b>Online ({no}):</b> de
    <a href="https://www.costco.ca/offers-ending.html" target="_blank" rel="noopener">Offers Ending Sunday</a>,
    con foto oficial y link a la ficha real. Los precios online no son los mismos que en bodega.<br><br>
    <b>Mi lista</b> se guarda en este navegador (localStorage). No se env&iacute;a a ning&uacute;n
    lado y no se comparte entre dispositivos. Las fotos se enlazan a su servidor de origen.<br><br>
    P&aacute;gina informativa sin relaci&oacute;n con Costco Wholesale.
  </p>
</div>
<script>{JS}</script>
</body>
</html>
"""
    salida = WEB / "costco-ofertas.html"
    salida.write_text(doc)
    print(f"{salida}  ({len(doc):,} bytes)")
    print(f"  {len(items)} ofertas ({nb} bodega + {no} online), {con_foto} con foto")
    print(f"  categorias: {', '.join(cats)}")


if __name__ == "__main__":
    main()
