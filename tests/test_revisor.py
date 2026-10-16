from datetime import date
from veg.modelos import Pieza, Salida
from veg.revisor import revisar

HOY = date(2026, 10, 24)
HASHTAGS = ["#viajarengrupo", "#viajesgrupales", "#agenciadeviajes", "#españa", "#nortedeespaña"]
NORTE = Salida(id="norte", destino="Norte de España", fecha_salida=date(2027, 5, 24), duracion="18 días",
               operador="Viajar en Grupo", url="https://x", cupo="disponible", verificado_en=HOY,
               precio_desde=9680, especial=True)


def pieza(**kw):
    base = dict(id="2026-11-06-post", fecha=date(2026, 11, 6), hora="13:00", formato="post", pilar="especial",
                tema="Norte de España", salida_id="norte", titulo="Norte de España",
                texto="Del 24 de mayo al 10 de junio de 2027. Desde USD 9.680. ¿Nos acompañás? Escribinos por WhatsApp al +54 9 11 5944-4920 ✈️",
                hashtags=HASHTAGS)
    base.update(kw)
    return Pieza(**base)


def test_pieza_correcta_sin_problemas():
    assert revisar(pieza(), NORTE, HOY) == []


def test_titular_largo():
    assert "El titular tiene más de 5 palabras" in revisar(pieza(titulo="El norte de España con los cinco sentidos"), NORTE, HOY)


def test_hashtags():
    problemas = revisar(pieza(hashtags=["#viajes", "#viajarengrupo"]), NORTE, HOY)
    assert "Debe tener entre 5 y 8 hashtags" in problemas
    assert "El primer hashtag debe ser #viajarengrupo" in problemas


def test_sin_cta():
    assert "Falta un llamado a la acción" in revisar(pieza(texto="Un viaje soñado. Desde USD 9.680."), NORTE, HOY)


def test_precio_sin_desde():
    assert 'El precio va con "desde"' in revisar(pieza(texto="USD 9.680. Escribinos por WhatsApp."), NORTE, HOY)


def test_cupo_no_verificado_hoy():
    vieja = Salida(**{**NORTE.__dict__, "verificado_en": date(2026, 10, 18)})
    assert "Cupo de Norte de España no verificado hoy" in revisar(pieza(), vieja, HOY)


def test_especial_con_salida_de_mayorista():
    mayorista = Salida(**{**NORTE.__dict__, "especial": False})
    assert "Solo las salidas propias pueden ir como especial de agencia" in revisar(pieza(), mayorista, HOY)


def test_venta_sin_salida():
    assert "Pieza de venta sin salida asociada" in revisar(pieza(), None, HOY)


def test_mayusculas_sostenidas():
    assert "Mayúsculas sostenidas en el texto" in revisar(pieza(texto="ÚLTIMOS LUGARES DISPONIBLES YA. Escribinos por WhatsApp."), NORTE, HOY)


def test_historias_no_exigen_hashtags_ni_titular():
    h = pieza(formato="historias", pilar="agencia", salida_id=None, titulo="", texto="", hashtags=[])
    assert revisar(h, None, HOY) == []


def test_salida_que_parte_en_el_mes_de_la_pieza():
    p = pieza(fecha=date(2027, 5, 7))
    assert "La salida parte en el mes de la pieza o antes: no se vende" in revisar(p, NORTE, HOY)


def test_precio_desactualizado_en_el_texto():
    nuevo = Salida(**{**NORTE.__dict__, "precio_desde": 9900})
    assert "El precio del texto no coincide con la salida (USD 9.900)" in revisar(pieza(), nuevo, HOY)


def test_historia_de_venta_sin_salida_verificada():
    h = pieza(formato="historias", pilar="agencia", salida_id=None, titulo="", hashtags=[],
              texto="Quedan pocos cupos para Mercadillos\nDesde USD 4.500\nEscribinos")
    assert "Historia con cupos o precio sin salida verificada hoy" in revisar(h, None, HOY)


def test_historia_de_venta_con_salida_verificada_pasa():
    h = pieza(formato="historias", pilar="agencia", salida_id="norte", titulo="", hashtags=[],
              texto="Quedan pocos cupos\nDesde USD 9.680")
    assert revisar(h, NORTE, HOY) == []
