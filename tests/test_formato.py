from datetime import date
from veg.formato import formatear_precio, rango_fechas, LETRA_CHICA_VENTA


def test_precio_con_miles():
    assert formatear_precio(9680) == "USD 9.680"


def test_precio_millon_y_decimales():
    assert formatear_precio(1234567.4) == "USD 1.234.567"


def test_precio_a_consultar():
    assert formatear_precio(None) == "CONSULTÁ CUPOS"


def test_rango_distintos_meses():
    assert rango_fechas(date(2027, 5, 24), date(2027, 6, 10)) == "24 may – 10 jun 2027"


def test_rango_mismo_mes():
    assert rango_fechas(date(2026, 11, 6), date(2026, 11, 20)) == "6 – 20 nov 2026"


def test_rango_distintos_anios():
    assert rango_fechas(date(2026, 12, 28), date(2027, 1, 8)) == "28 dic 2026 – 8 ene 2027"


def test_letra_chica():
    assert LETRA_CHICA_VENTA == "Leg. 19725 · Precios sujetos a disponibilidad y cambio"
