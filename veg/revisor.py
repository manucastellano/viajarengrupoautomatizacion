from __future__ import annotations

import re
from datetime import date

from .modelos import Pieza, Salida

CTAS = ("whatsapp", "link en bio", "escribinos", "dejanos tu comentario", "sumate", "mensaje privado")
_MAYUSCULAS = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{4,}(?:\s+[A-ZÁÉÍÓÚÑ]{4,}){2,}\b")
_PRECIO = re.compile(r"\bUSD\s?\d[\d.]*")


def revisar(pieza: Pieza, salida: Salida | None, hoy: date) -> list[str]:
    problemas: list[str] = []
    if pieza.formato != "historias":
        if len(pieza.titulo.split()) > 5:
            problemas.append("El titular tiene más de 5 palabras")
        if not 5 <= len(pieza.hashtags) <= 8:
            problemas.append("Debe tener entre 5 y 8 hashtags")
        if not pieza.hashtags or pieza.hashtags[0] != "#viajarengrupo":
            problemas.append("El primer hashtag debe ser #viajarengrupo")
        if not any(c in pieza.texto.lower() for c in CTAS):
            problemas.append("Falta un llamado a la acción")
    if _PRECIO.search(pieza.texto) and "desde" not in pieza.texto.lower():
        problemas.append('El precio va con "desde"')
    if _MAYUSCULAS.search(pieza.texto):
        problemas.append("Mayúsculas sostenidas en el texto")
    if pieza.pilar in ("especial", "paquete"):
        if salida is None:
            problemas.append("Pieza de venta sin salida asociada")
        else:
            if salida.verificado_en != hoy:
                problemas.append(f"Cupo de {salida.destino} no verificado hoy")
            if not salida.vendible:
                problemas.append(f"{salida.destino} sin cupo")
            if pieza.pilar == "especial" and not salida.especial:
                problemas.append("Solo las salidas propias pueden ir como especial de agencia")
    return problemas
