from datetime import date
from veg.calendario import armar_calendario, salidas_vendibles
from veg.modelos import Salida

HOY = date(2026, 10, 18)


def s(id, salida, cupo="disponible", verificado=HOY, especial=False):
    return Salida(id=id, destino=id, fecha_salida=salida, duracion="10 días", operador="Op", url="https://x",
                  cupo=cupo, verificado_en=verificado, especial=especial)


ESPECIAL = s("norte-espana-2027", date(2027, 5, 24), especial=True)
PERU = s("peru", date(2027, 3, 1))
MERCADILLOS = s("mercadillos", date(2026, 12, 2))
COREA = s("corea", date(2026, 11, 4))            # parte dentro del mes: no se vende
AGOTADA = s("agotada", date(2027, 1, 10), cupo="agotado")
VIEJA = s("vieja", date(2027, 2, 1), verificado=date(2026, 10, 1))
TODAS = [ESPECIAL, PERU, MERCADILLOS, COREA, AGOTADA, VIEJA]


def test_cantidad_de_piezas_noviembre_2026():
    piezas = armar_calendario(2026, 11, TODAS, HOY)
    por_formato = {}
    for p in piezas:
        por_formato[p.formato] = por_formato.get(p.formato, 0) + 1
    # 5 lunes (2,9,16,23,30), 4 miércoles, 4 viernes, 21 días hábiles
    assert por_formato["reel"] == 4
    assert por_formato["historias"] == 21
    assert por_formato.get("post", 0) + por_formato.get("carrusel", 0) == 9


def test_rotacion_de_reels():
    reels = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.formato == "reel"]
    assert [p.pilar for p in reels] == ["especial", "paquete", "destino", "agencia"]
    assert [p.fecha.day for p in reels] == [4, 11, 18, 25]
    assert all(p.hora == "20:00" for p in reels)


def test_quinto_lunes_repite_semana_uno():
    lunes = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.fecha.weekday() == 0 and p.formato != "historias"]
    assert [p.pilar for p in lunes] == ["educativo", "destino", "educativo", "agencia", "educativo"]
    assert all(p.formato == "carrusel" for p in lunes if p.pilar in ("educativo", "destino"))


def test_viernes_de_venta():
    viernes = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.fecha.weekday() == 4 and p.formato != "historias"]
    assert [p.pilar for p in viernes] == ["especial", "paquete", "especial", "paquete"]
    assert all(p.hora == "13:00" and p.formato == "post" for p in viernes)


def test_especial_va_con_la_salida_propia():
    piezas = armar_calendario(2026, 11, TODAS, HOY)
    assert {p.salida_id for p in piezas if p.pilar == "especial"} == {"norte-espana-2027"}


def test_paquetes_por_fecha_de_salida_y_sin_excluidas():
    paquetes = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.pilar == "paquete"]
    # en orden cronológico de publicación: mié 11 (reel), vie 13, vie 27
    assert [p.salida_id for p in paquetes] == ["mercadillos", "peru", "mercadillos"]


def test_vendibles_excluye_mes_actual_agotadas_y_no_verificadas():
    assert [x.id for x in salidas_vendibles(TODAS, 2026, 11, HOY)] == ["mercadillos", "peru"]


def test_sin_paquetes_pasa_a_destino():
    piezas = armar_calendario(2026, 11, [ESPECIAL], HOY)
    assert not [p for p in piezas if p.pilar == "paquete"]
    assert all(p.salida_id is None for p in piezas if p.pilar == "destino")


def test_sin_especial_verificado_pasa_a_destino():
    piezas = armar_calendario(2026, 11, [PERU], HOY)
    assert not [p for p in piezas if p.pilar == "especial"]


def test_historias_tema_por_dia_e_ids_unicos():
    piezas = armar_calendario(2026, 11, TODAS, HOY)
    historias = {p.fecha: p for p in piezas if p.formato == "historias"}
    assert historias[date(2026, 11, 3)].tema == "encuesta de destino"
    ids = [p.id for p in piezas]
    assert len(ids) == len(set(ids))
    assert "2026-11-04-reel" in ids


def test_especial_no_se_vende_en_su_mes_de_salida_ni_despues():
    for anio, mes in ((2027, 5), (2027, 6)):
        piezas = armar_calendario(anio, mes, [ESPECIAL], HOY)
        assert not [p for p in piezas if p.pilar == "especial"]
