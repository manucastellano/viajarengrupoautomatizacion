from __future__ import annotations

import re
from datetime import date

from .formato import formatear_precio
from .modelos import Pieza, Salida

CTAS = ("whatsapp", "link en bio", "escribinos", "dejanos tu comentario", "sumate", "mensaje privado", "comentá")
_MAYUSCULAS = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{4,}(?:\s+[A-ZÁÉÍÓÚÑ]{4,}){2,}\b")
WHATSAPP = "+54 9 11 4434-0161"
NUMERO_VIEJO = "5944-4920"
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
    if NUMERO_VIEJO in pieza.texto:
        problemas.append(f"Número de WhatsApp desactualizado: usar {WHATSAPP}")
    if pieza.formato != "historias" and not ("link" in pieza.texto.lower() and "perfil" in pieza.texto.lower()):
        problemas.append("Falta aclarar que el contacto está en el link del perfil")
    if _PRECIO.search(pieza.texto) and "desde" not in pieza.texto.lower():
        problemas.append('El precio va con "desde"')
    if _MAYUSCULAS.search(pieza.texto):
        problemas.append("Mayúsculas sostenidas en el texto")
    es_historia_de_venta = pieza.formato == "historias" and (_PRECIO.search(pieza.texto) or "cupo" in pieza.texto.lower())
    if es_historia_de_venta and (salida is None or salida.verificado_en != hoy or not salida.vendible):
        problemas.append("Historia con cupos o precio sin salida verificada hoy")
    if pieza.pilar in ("especial", "paquete") or (es_historia_de_venta and salida is not None):
        if salida is None:
            problemas.append("Pieza de venta sin salida asociada")
        else:
            if salida.verificado_en != hoy:
                problemas.append(f"Cupo de {salida.destino} no verificado hoy")
            if not salida.vendible:
                problemas.append(f"{salida.destino} sin cupo")
            if (salida.fecha_salida.year, salida.fecha_salida.month) <= (pieza.fecha.year, pieza.fecha.month):
                problemas.append("La salida parte en el mes de la pieza o antes: no se vende")
            if salida.precio_desde is not None and formatear_precio(salida.precio_desde, salida.moneda) not in pieza.texto:
                problemas.append(f"El precio del texto no coincide con la salida ({formatear_precio(salida.precio_desde, salida.moneda)})")
            if pieza.pilar == "especial" and not salida.especial:
                problemas.append("Solo las salidas propias pueden ir como especial de agencia")
    return problemas
