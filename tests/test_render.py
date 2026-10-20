import pytest
from PIL import Image
from veg.render import html, render_png
from veg.formato import formatear_precio

POST = dict(etiqueta="Especial de agencia", titulo="Norte de España", subtitulo="24 may – 10 jun 2027 · 18 días",
            precio=formatear_precio(9680), letra_chica="Por persona en base doble · Leg. 19725")


def test_html_post_contiene_datos_y_desde():
    h = html("post_paquete", POST)
    assert "Norte de España" in h and "USD 9.680" in h and "Desde" in h


def test_html_precio_a_consultar_sin_desde():
    h = html("post_paquete", {**POST, "precio": formatear_precio(None)})
    assert "Consultá cupos" in h and "Desde" not in h and "None" not in h


def test_html_escapa_texto():
    assert "<script>" not in html("placa_cierre", {"frase": "<script>x</script>"})


@pytest.mark.lento
@pytest.mark.parametrize("plantilla,datos,tamano", [
    ("post_paquete", POST, (1080, 1350)),
    ("portada_reel", {"etiqueta": "Recap", "titulo": "La Dolce Vita", "subtitulo": "Italia 2026"}, (1080, 1920)),
    ("historia", {"etiqueta": "Charla informativa", "titulo": "Norte de España", "texto": "Martes 18 h", "cta": "Escribinos por WhatsApp"}, (1080, 1920)),
    ("lamina", {"titulo": "5 mitos de viajar en grupo", "oscuro": True, "etiqueta": "Tips de viaje"}, (1080, 1350)),
    ("placa_cierre", {"frase": "¿Nos acompañás?"}, (1080, 1920)),
    ("historia_postal", {"anio": "2025", "lugar": "Sur de Francia", "esquina": "abajo"}, (1080, 1920)),
    ("historia_frase", {"frase": "Viajar es lo único que comprás y te hace más rico."}, (1080, 1920)),
])
def test_render_tamano(tmp_path, plantilla, datos, tamano):
    png = render_png(plantilla, datos, tmp_path / f"{plantilla}.png")
    assert Image.open(png).size == tamano


@pytest.mark.lento
def test_subtitulo_transparente(tmp_path):
    png = render_png("subtitulo", {"texto": "Así vivimos la ópera en Verona"}, tmp_path / "sub.png", transparente=True)
    img = Image.open(png).convert("RGBA")
    assert img.size == (1080, 1920)
    assert img.getpixel((10, 10))[3] == 0  # esquina transparente


def test_html_precio_crudo_none_no_imprime_none():
    h = html("post_paquete", {**POST, "precio": None, "letra_chica": None})
    assert "Consultá cupos" in h and "Desde" not in h and "None" not in h


def test_html_precio_numerico_se_formatea():
    h = html("post_paquete", {**POST, "precio": 9680})
    assert "USD 9.680" in h and "Desde" in h
