from datetime import date
import pytest
from veg.modelos import Salida, Pieza, guardar, cargar_salidas, cargar_piezas


def salida(**kw):
    base = dict(id="norte-espana-2027", destino="Norte de España", fecha_salida=date(2027, 5, 24),
                duracion="18 días", operador="Viajar en Grupo", url="https://www.viajarengrupo.tur.ar/norte-espana-2027",
                cupo="disponible", verificado_en=date(2026, 10, 18), precio_desde=9680, suplemento_single=2290, especial=True)
    base.update(kw)
    return Salida(**base)


def test_salida_ida_y_vuelta_json(tmp_path):
    ruta = tmp_path / "salidas.json"
    guardar(ruta, [salida()])
    assert cargar_salidas(ruta) == [salida()]


def test_pieza_ida_y_vuelta_json(tmp_path):
    p = Pieza(id="2026-11-04-reel", fecha=date(2026, 11, 4), hora="20:00", formato="reel",
              pilar="especial", tema="Norte de España con los 5 sentidos", hashtags=["#viajarengrupo"])
    ruta = tmp_path / "piezas.json"
    guardar(ruta, [p])
    assert cargar_piezas(ruta) == [p]


def test_cupo_invalido():
    with pytest.raises(ValueError):
        salida(cupo="lleno")


@pytest.mark.parametrize("cupo,vendible", [("disponible", True), ("ultimos", True), ("agotado", False), ("sin_verificar", False)])
def test_vendible(cupo, vendible):
    assert salida(cupo=cupo).vendible is vendible
