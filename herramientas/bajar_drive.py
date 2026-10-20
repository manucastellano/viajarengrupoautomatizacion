"""Descarga las fotos de carpetas públicas de Google Drive, con subcarpetas.

Uso: .venv/Scripts/python herramientas/bajar_drive.py <destino> <id_carpeta>=<nombre> [...]
Guarda en <destino>/<nombre>/<subcarpeta...>/<archivo>. Solo baja imágenes (jpg, png, heic);
los videos se listan en <destino>/videos.tsv para elegirlos después. Saltea lo ya descargado.
Nota: la vista pública de Drive muestra hasta ~50 archivos por carpeta.
"""
import re
import sys
import time
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0"}
ITEM = re.compile(r'\["([A-Za-z0-9_-]{25,44})",\["([A-Za-z0-9_-]{25,44})"\],"([^"]{1,160})","([a-z/.\-+0-9]+)"')
SEGURO = re.compile(r'[\\/:*?"<>|]')


def bajar(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def listar(folder_id: str) -> list[tuple[str, str, str]]:
    html = bajar(f"https://drive.google.com/drive/folders/{folder_id}").decode("utf-8", "replace")
    i = html.find("_DRIVE_ivd")
    dec = (html[i:i + 2_000_000].replace("\\x22", '"').replace("\\x5b", "[").replace("\\x5d", "]")
           .replace("\\/", "/").replace("\\u0026", "&"))
    return [(fid, nombre, mime) for fid, padre, nombre, mime in ITEM.findall(dec) if padre == folder_id]


def main(destino: Path, carpetas: list[tuple[str, str]]):
    destino.mkdir(parents=True, exist_ok=True)
    cola = [(fid, destino / nombre) for fid, nombre in carpetas]
    vistos, videos, ok, saltados, errores = set(), [], 0, 0, 0
    while cola:
        fid, ruta = cola.pop(0)
        if fid in vistos:
            continue
        vistos.add(fid)
        try:
            items = listar(fid)
        except Exception as e:  # noqa: BLE001
            print("no pude listar", ruta, e)
            errores += 1
            continue
        for item_id, nombre, mime in items:
            limpio = SEGURO.sub("_", nombre).strip()
            if mime == "application/vnd.google-apps.folder":
                cola.append((item_id, ruta / limpio))
            elif mime.startswith("image/"):
                archivo = ruta / limpio
                if archivo.exists() and archivo.stat().st_size > 0:
                    saltados += 1
                    continue
                try:
                    datos = bajar(f"https://drive.google.com/uc?export=download&id={item_id}")
                    if datos[:15].lower().startswith(b"<!doctype html") or datos[:5].lower() == b"<html":
                        print("no descargable:", archivo)
                        errores += 1
                        continue
                    archivo.parent.mkdir(parents=True, exist_ok=True)
                    archivo.write_bytes(datos)
                    ok += 1
                    if ok % 50 == 0:
                        print(f"{ok} fotos bajadas…", flush=True)
                except Exception as e:  # noqa: BLE001
                    print("error", archivo, e)
                    errores += 1
                time.sleep(0.2)
            elif mime.startswith("video/"):
                videos.append(f"{item_id}\t{mime}\t{ruta.relative_to(destino) / limpio}")
    (destino / "videos.tsv").write_text("id\ttipo\truta\n" + "\n".join(videos) + "\n", encoding="utf-8")
    print(f"listo: {ok} fotos nuevas, {saltados} ya estaban, {len(videos)} videos listados, {errores} errores")


if __name__ == "__main__":
    pares = [a.split("=", 1) for a in sys.argv[2:]]
    main(Path(sys.argv[1]), [(p[0], p[1]) for p in pares])
