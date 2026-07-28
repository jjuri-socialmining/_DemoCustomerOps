#!/usr/bin/env python3
"""
watermark_pdf.py — Estampa un sello de agua diagonal en cada página de un PDF.

Uso:
    python3 tools/watermark_pdf.py <input.pdf> [output.pdf] [--text "BORRADOR CONFIDENCIAL"]

Si no se da output, sobrescribe el input (vía archivo temporal).
Requiere: PyMuPDF (import fitz).
"""

import sys
import os
import argparse
import fitz  # PyMuPDF


def add_watermark(in_path, out_path, text, fontsize=46, opacity=0.05, angle=45):
    doc = fitz.open(in_path)
    for page in doc:
        rect = page.rect
        pivot = fitz.Point(rect.width / 2, rect.height / 2)
        morph = (pivot, fitz.Matrix(angle))
        tw = fitz.get_text_length(text, fontname="helv", fontsize=fontsize)
        # Punto base para centrar el texto horizontalmente respecto al pivote.
        point = fitz.Point(rect.width / 2 - tw / 2, rect.height / 2)
        page.insert_text(
            point,
            text,
            fontsize=fontsize,
            fontname="helv",
            color=(0.72, 0.12, 0.12),   # rojo apagado, tono "borrador"
            fill_opacity=opacity,
            morph=morph,
        )
    # Guardar (a temporal si se sobrescribe).
    if os.path.abspath(in_path) == os.path.abspath(out_path):
        tmp = out_path + ".tmp"
        doc.save(tmp, garbage=4, deflate=True)
        doc.close()
        os.replace(tmp, out_path)
    else:
        doc.save(out_path, garbage=4, deflate=True)
        doc.close()
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Estampa un sello de agua diagonal en un PDF.")
    ap.add_argument("input", help="PDF de entrada")
    ap.add_argument("output", nargs="?", help="PDF de salida (por defecto sobrescribe el input)")
    ap.add_argument("--text", default="BORRADOR CONFIDENCIAL", help="Texto del sello")
    ap.add_argument("--opacity", type=float, default=0.05, help="Opacidad 0–1")
    ap.add_argument("--fontsize", type=int, default=46, help="Tamaño de fuente")
    args = ap.parse_args()

    out = args.output or args.input
    add_watermark(args.input, out, args.text, fontsize=args.fontsize, opacity=args.opacity)
    print(f"✅  Sello '{args.text}' aplicado → {out}")


if __name__ == "__main__":
    main()
