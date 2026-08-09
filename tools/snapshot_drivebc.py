#!/usr/bin/env python3
"""Baja DriveBC a JSON estático dentro de web/data/.

DriveBC responde 200 pero sin cabecera CORS: el navegador no puede pedirle
nada directamente. En GitHub Pages no hay proxy posible, así que la data se
congela acá y se sirve como archivo del mismo origen que la página.

Lo corre .github/workflows/refresh-drivebc.yml antes de publicar, así que
el sitio se despliega siempre con datos frescos y sin ensuciar el historial
del repo con commits automáticos.
"""
import json, math, pathlib, urllib.request
from datetime import datetime, timezone

UA = {'User-Agent': 'DemoCustomerOps/1.0 (mapa operativo publico)'}
EVENTOS = 'https://www.drivebc.ca/api/events/?format=json'
CAMARAS = 'https://www.drivebc.ca/api/webcams/?format=json'

CORREDORES = [
    (49.2186, -122.9122), (49.3760, -123.2720), (49.4560, -123.2380),
    (49.5560, -123.2340), (49.6200, -123.2050), (49.7016, -123.1558),
    (49.7825, -123.1226), (49.3800, -121.4400), (49.1145, -120.8566),
]
RADIO_KM = 25
DESTINO = pathlib.Path(__file__).resolve().parent.parent / 'web' / 'data'


def km(a, b):
    R = 6371.0
    p = math.pi / 180
    dl = (b[0] - a[0]) * p
    dg = (b[1] - a[1]) * p
    x = math.sin(dl / 2) ** 2 + math.cos(a[0] * p) * math.cos(b[0] * p) * math.sin(dg / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def cerca(lat, lon):
    return min(km(p, (lat, lon)) for p in CORREDORES) <= RADIO_KM


def bajar(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
        return json.load(r)


def punto(loc):
    if not isinstance(loc, dict):
        return None
    c = loc.get('coordinates')
    if not c:
        return None
    if isinstance(c[0], (list, tuple)):
        c = c[0]
    try:
        return float(c[1]), float(c[0])
    except (TypeError, ValueError, IndexError):
        return None


def main():
    sello = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
    DESTINO.mkdir(parents=True, exist_ok=True)

    eventos = [e for e in bajar(EVENTOS) if (pt := punto(e.get('location'))) and cerca(*pt)]

    camaras = []
    for c in bajar(CAMARAS):
        pt = punto(c.get('location'))
        if not pt or not c.get('is_on') or not cerca(*pt):
            continue
        img = (c.get('links') or {}).get('imageDisplay') or ''
        camaras.append({
            'id': c.get('id'),
            'nombre': c.get('name_override') or c.get('name'),
            'detalle': c.get('caption_override') or c.get('caption'),
            'ruta': str(c.get('highway') or ''),
            'lat': pt[0], 'lon': pt[1],
            'orientacion': c.get('orientation'),
            'elevacion': c.get('elevation'),
            # images.drivebc.ca devuelve un marcador de posición idéntico para
            # todas las cámaras; el host bueno es www.drivebc.ca.
            'imagen': 'https://www.drivebc.ca' + img.split('?')[0] if img else None,
            'actualizada': c.get('last_update_modified'),
        })

    (DESTINO / 'drivebc-eventos.json').write_text(
        json.dumps({'generado': sello, 'eventos': eventos}, ensure_ascii=False), encoding='utf-8')
    (DESTINO / 'drivebc-camaras.json').write_text(
        json.dumps({'generado': sello, 'camaras': camaras}, ensure_ascii=False), encoding='utf-8')

    print(f'{len(eventos)} eventos y {len(camaras)} cámaras · sello {sello}')


if __name__ == '__main__':
    main()
