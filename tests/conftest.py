import subprocess
from pathlib import Path
import pytest
from imageio_ffmpeg import get_ffmpeg_exe


def clip_de_prueba(destino: Path, ancho: int, alto: int, segundos: float, ruido: bool = False) -> Path:
    fuente = f"testsrc2=size={ancho}x{alto}:rate=30"
    filtro = ["-vf", "noise=alls=80:allf=t"] if ruido else []
    subprocess.run([get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", fuente,
                    "-t", str(segundos), *filtro, "-pix_fmt", "yuv420p", str(destino)], check=True)
    return destino


@pytest.fixture
def clips(tmp_path):
    return {
        "horizontal": clip_de_prueba(tmp_path / "h.mp4", 1920, 1080, 5),
        "vertical": clip_de_prueba(tmp_path / "v.mp4", 1080, 1920, 4),
    }
