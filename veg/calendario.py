from __future__ import annotations

import calendar
from datetime import date

from .modelos import Pieza, Salida

REEL = ["especial", "paquete", "destino", "agencia"]
VIERNES = ["especial", "paquete", "especial", "paquete"]
LUNES = ["educativo", "destino", "educativo", "agencia"]
TEMA_HISTORIAS = {0: "tip", 1: "encuesta de destino", 2: "reel y cupos", 3: "Bettina / detrás de escena", 4: "próximas salidas"}


def _dias(anio: int, mes: int, dia_semana: int) -> list[date]:
    ultimo = calendar.monthrange(anio, mes)[1]
    return [date(anio, mes, d) for d in range(1, ultimo + 1) if date(anio, mes, d).weekday() == dia_semana]


def salidas_vendibles(salidas: list[Salida], anio: int, mes: int, hoy: date) -> list[Salida]:
    validas = [
        x for x in salidas
        if x.vendible and x.verificado_en == hoy and not x.especial
        and (x.fecha_salida.year, x.fecha_salida.month) > (anio, mes)
    ]
    return sorted(validas, key=lambda x: x.fecha_salida)


def armar_calendario(anio: int, mes: int, salidas: list[Salida], hoy: date) -> list[Pieza]:
    especial = next((x for x in salidas if x.especial and x.vendible and x.verificado_en == hoy), None)
    paquetes = salidas_vendibles(salidas, anio, mes, hoy)

    huecos: list[tuple[date, str, str, str]] = []  # (fecha, hora, formato, pilar)
    for k, d in enumerate(_dias(anio, mes, 0)):
        huecos.append((d, "19:00", "post", LUNES[k % 4]))
    for k, d in enumerate(_dias(anio, mes, 2)):
        huecos.append((d, "20:00", "reel", REEL[k % 4]))
    for k, d in enumerate(_dias(anio, mes, 4)):
        huecos.append((d, "13:00", "post", VIERNES[k % 4]))
    huecos.sort(key=lambda h: (h[0], h[1]))

    piezas: list[Pieza] = []
    i_paquete = 0
    for fecha, hora, formato, pilar in huecos:
        salida_id = None
        if pilar == "especial":
            if especial:
                salida_id = especial.id
            else:
                pilar = "destino"
        elif pilar == "paquete":
            if paquetes:
                salida_id = paquetes[i_paquete % len(paquetes)].id
                i_paquete += 1
            else:
                pilar = "destino"
        if formato == "post" and pilar in ("educativo", "destino") and fecha.weekday() == 0:
            formato = "carrusel"
        piezas.append(Pieza(id=f"{fecha.isoformat()}-{formato}", fecha=fecha, hora=hora, formato=formato,
                            pilar=pilar, tema="", salida_id=salida_id))

    ultimo = calendar.monthrange(anio, mes)[1]
    for d in range(1, ultimo + 1):
        fecha = date(anio, mes, d)
        if fecha.weekday() < 5:
            piezas.append(Pieza(id=f"{fecha.isoformat()}-historias", fecha=fecha, hora="10:00", formato="historias",
                                pilar="agencia", tema=TEMA_HISTORIAS[fecha.weekday()]))

    return sorted(piezas, key=lambda p: (p.fecha, p.hora))
