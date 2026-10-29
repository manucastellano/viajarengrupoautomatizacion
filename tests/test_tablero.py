import json
from datetime import date
from veg.modelos import Pieza, Salida
from veg.tablero import escribir_documentos, escribir_filas, fila, preparar_pagina

NORTE = Salida(id="norte", destino="Norte de España", fecha_salida=date(2027, 5, 24), duracion="18 días",
               operador="Viajar en Grupo", url="https://x", cupo="disponible", verificado_en=date(2026, 10, 24), especial=True)
P = Pieza(id="2026-11-06-post", fecha=date(2026, 11, 6), hora="13:00", formato="post", pilar="especial",
          tema="Norte", salida_id="norte", titulo="Norte de España", texto="Hola", hashtags=["#viajarengrupo"])
A = [{"id": "c4722e25534c8b0ed90b45356b4663bd", "tipo": "imagen", "nombre": "post.png"}]


def test_fila_con_verificacion():
    f = fila(P, A, NORTE)
    assert f["doc_id"] == "2026-11-06-post"
    d = f["data"]
    assert d["fecha"] == "2026-11-06" and d["estado"] == "pendiente" and d["version"] == 1
    assert d["verificacion"] == {"fuente": "Viajar en Grupo", "fecha": "2026-10-24"}
    assert d["assets"] == A


def test_fila_sin_salida():
    assert fila(P, [], None)["data"]["verificacion"] is None


def test_escribir_filas(tmp_path):
    ruta = escribir_filas([P], {P.id: A}, [NORTE], tmp_path / "filas.json")
    assert json.loads(ruta.read_text(encoding="utf-8"))[0]["doc_id"] == P.id


def test_preparar_pagina(tmp_path):
    destino = preparar_pagina(2026, 11, tmp_path / "tablero.html")
    contenido = destino.read_text(encoding="utf-8")
    assert "<title>Tablero Noviembre 2026</title>" in contenido
    assert '"2026-11"' in contenido and "__MES__" not in contenido and "__TITULO__" not in contenido


def test_escribir_documentos_un_archivo_por_pieza(tmp_path):
    filas = escribir_filas([P], {P.id: A}, [NORTE], tmp_path / "filas.json")
    archivos = escribir_documentos(filas, tmp_path / "docs")
    assert [a.name for a in archivos] == ["2026-11-06-post.json"]
    assert json.loads(archivos[0].read_text(encoding="utf-8"))["titulo"] == "Norte de España"


def test_fila_lleva_el_programa():
    from dataclasses import replace
    assert fila(replace(P, programa="espana"), [], None)["data"]["programa"] == "espana"
    assert fila(P, [], None)["data"]["programa"] is None
