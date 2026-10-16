from pathlib import Path
import pytest
from veg.reel import Toma, armar_reel, hacer_preview, recortar_tomas
from veg.render import render_png
from veg.sonda import info
from tests.conftest import clip_de_prueba


def test_recortar_tomas_respeta_maximo():
    tomas = [Toma(Path("a.mp4"), 0, 40), Toma(Path("b.mp4"), 10, 50), Toma(Path("c.mp4"), 0, 30)]
    r = recortar_tomas(tomas)
    assert sum(t.duracion for t in r) == pytest.approx(86.0)
    assert len(r) == 3 and r[2].fin == pytest.approx(6.0)


@pytest.fixture
def placas(tmp_path):
    portada = render_png("portada_reel", {"etiqueta": "Recap", "titulo": "La Dolce Vita"}, tmp_path / "portada.png")
    placa = render_png("placa_cierre", {"frase": "¿Nos acompañás?"}, tmp_path / "placa.png")
    return portada, placa


@pytest.mark.lento
def test_reel_vertical_con_clip_horizontal(tmp_path, clips, placas):
    tomas = [Toma(clips["horizontal"], 0, 4, "Así vivimos Verona"), Toma(clips["vertical"], 1, 3)]
    final, preview = armar_reel(tomas, *placas, tmp_path / "out", "prueba")
    ancho, alto, dur = info(final)
    assert (ancho, alto) == (1080, 1920)
    assert dur == pytest.approx(1 + 4 + 2 + 3, abs=0.5)
    assert info(preview)[:2] == (720, 1280)


@pytest.mark.lento
def test_reel_largo_no_pasa_90s(tmp_path, placas):
    largo = clip_de_prueba(tmp_path / "largo.mp4", 1080, 1920, 50)
    tomas = [Toma(largo, 0, 50), Toma(largo, 0, 50)]
    final, _ = armar_reel(tomas, *placas, tmp_path / "out", "largo")
    assert info(final)[2] <= 90.5


@pytest.mark.lento
def test_preview_pesada_queda_bajo_18mb(tmp_path):
    pesado = clip_de_prueba(tmp_path / "pesado.mp4", 1080, 1920, 90, ruido=True)
    preview = hacer_preview(pesado, tmp_path / "pesado-preview.mp4")
    assert preview.stat().st_size <= 18 * 1024 * 1024
