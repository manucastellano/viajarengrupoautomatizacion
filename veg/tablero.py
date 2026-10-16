from __future__ import annotations

import json
from pathlib import Path

from .modelos import Pieza, Salida

RAIZ = Path(__file__).resolve().parent.parent
NOMBRES_MES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
               "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def fila(pieza: Pieza, assets: list[dict], salida: Salida | None) -> dict:
    return {"doc_id": pieza.id, "data": {
        "id": pieza.id, "fecha": pieza.fecha.isoformat(), "hora": pieza.hora, "formato": pieza.formato,
        "pilar": pieza.pilar, "tema": pieza.tema, "titulo": pieza.titulo, "texto": pieza.texto,
        "hashtags": pieza.hashtags, "assets": assets, "version": pieza.version, "estado": pieza.estado,
        "comentario": pieza.comentario,
        "verificacion": {"fuente": salida.operador, "fecha": salida.verificado_en.isoformat()} if salida else None,
    }}


def escribir_filas(piezas: list[Pieza], assets_por_pieza: dict[str, list[dict]], salidas: list[Salida], ruta: Path) -> Path:
    por_id = {s.id: s for s in salidas}
    filas = [fila(p, assets_por_pieza.get(p.id, []), por_id.get(p.salida_id)) for p in piezas]
    ruta = Path(ruta)
    ruta.write_text(json.dumps(filas, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta


def escribir_documentos(filas_json: Path, carpeta: Path) -> list[Path]:
    """Un JSON por pieza (`<doc_id>.json` con su `data`), para la carga por lotes de ArtifactData."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    archivos = []
    for f in json.loads(Path(filas_json).read_text(encoding="utf-8")):
        ruta = carpeta / f"{f['doc_id']}.json"
        ruta.write_text(json.dumps(f["data"], ensure_ascii=False, indent=2), encoding="utf-8")
        archivos.append(ruta)
    return archivos


def preparar_pagina(anio: int, mes: int, destino: Path) -> Path:
    plantilla = (RAIZ / "tablero" / "index.html").read_text(encoding="utf-8")
    pagina = (plantilla.replace("__TITULO__", f"{NOMBRES_MES[mes - 1]} {anio}")
                        .replace("__MES__", f"{anio}-{mes:02d}"))
    destino = Path(destino)
    destino.write_text(pagina, encoding="utf-8")
    return destino
