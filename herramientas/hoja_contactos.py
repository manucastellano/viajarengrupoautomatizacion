"""Hoja de contactos numerada de una carpeta de fotos (para elegir cuáles usar).

Uso: .venv/Scripts/python herramientas/hoja_contactos.py <carpeta> <salida.png>
Imprime "n<TAB>archivo" por cada foto numerada. Ignora HEIC (Pillow no los abre).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

carpeta, salida = Path(sys.argv[1]), Path(sys.argv[2])
fotos = sorted(p for p in carpeta.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))[:60]
W, H, COLS = 200, 266, 10
filas = (len(fotos) + COLS - 1) // COLS
hoja = Image.new("RGB", (COLS * (W + 6) + 6, filas * (H + 24) + 6), "#ffffff")
d = ImageDraw.Draw(hoja)
for k, f in enumerate(fotos, 1):
    try:
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
    except Exception:  # noqa: BLE001
        continue
    im.thumbnail((W, H))
    x, y = 6 + (k - 1) % COLS * (W + 6), 6 + (k - 1) // COLS * (H + 24)
    d.text((x, y), str(k), fill="#d00000")
    hoja.paste(im, (x, y + 14))
    print(f"{k}\t{f.name}")
salida.parent.mkdir(parents=True, exist_ok=True)
hoja.save(salida)
