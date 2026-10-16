from pathlib import Path
import pytest
from veg.reel import Toma, armar_reel, hacer_preview, recortar_tomas
from veg.render import render_png
from veg.sonda import info
from tests.conftest import clip_de_prueba


def test_recortar_tomas_respeta_maximo():
    tomas = [Toma(Path("a.mp4"), 0, 40), Toma(Path("b.mp4"), 10, 50), Toma(Path("c.mp4"), 0, 30)]
    r = recortar_tomas(tomas)
    assert sum(t.duracion for t in r) == pytest.approx(85.5)
    assert len(r) == 3 and r[2].fin == pytest.approx(5.5)


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


def test_recortar_tomas_redondea_a_frames_y_deja_margen():
    tomas = [Toma(Path("x.mp4"), 0, 3.17) for _ in range(28)]
    r = recortar_tomas(tomas)
    assert sum(t.duracion for t in r) <= 85.5 + 1e-9
    assert all(abs(t.duracion * 30 - round(t.duracion * 30)) < 1e-6 for t in r)
    assert all(t.duracion > 0 for t in r)


def test_recortar_tomas_descarta_tomas_vacias():
    assert recortar_tomas([Toma(Path("x.mp4"), 5, 5), Toma(Path("y.mp4"), 2, 1)]) == []


@pytest.mark.lento
def test_reel_con_muchas_tomas_fraccionarias_no_pasa_90s(tmp_path, placas):
    clip = clip_de_prueba(tmp_path / "c.mp4", 1080, 1920, 4)
    final, _ = armar_reel([Toma(clip, 0, 3.17) for _ in range(28)], *placas, tmp_path / "out", "muchas")
    assert info(final)[2] <= 90.0


@pytest.mark.lento
def test_toma_con_audio_conserva_el_sonido(tmp_path, placas):
    import subprocess
    from imageio_ffmpeg import get_ffmpeg_exe
    con_voz = tmp_path / "voz.mp4"
    subprocess.run([get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=1080x1920:rate=30",
                    "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000", "-t", "3", "-pix_fmt", "yuv420p", "-shortest", str(con_voz)], check=True)
    final, _ = armar_reel([Toma(con_voz, 0, 2, con_audio=True)], *placas, tmp_path / "out", "voz")
    r = subprocess.run([get_ffmpeg_exe(), "-hide_banner", "-ss", "1.2", "-t", "1", "-i", str(final), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    media = float(r.stderr.split("mean_volume:")[1].split("dB")[0])
    assert media > -40
