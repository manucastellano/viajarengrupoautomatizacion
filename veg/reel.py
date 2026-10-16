from __future__ import annotations

import math
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from imageio_ffmpeg import get_ffmpeg_exe

from .render import render_png
from .sonda import info

ANCHO, ALTO, FPS = 1080, 1920, 30
MAX_TOTAL, PORTADA_S, PLACA_S, MARGEN_S = 90.0, 1.0, 3.0, 0.5
LIMITE_PREVIEW = 18 * 1024 * 1024
ENCUADRE = f"scale={ANCHO}:{ALTO}:force_original_aspect_ratio=increase,crop={ANCHO}:{ALTO},setsar=1,fps={FPS}"
SILENCIO = ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
CODIFICAR = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
             "-c:a", "aac", "-ar", "48000", "-ac", "2"]


@dataclass
class Toma:
    archivo: Path
    inicio: float
    fin: float
    subtitulo: str = ""
    con_audio: bool = False  # True solo para tomas con sonido propio que debe oírse (Bettina hablando)

    @property
    def duracion(self) -> float:
        return self.fin - self.inicio


def _ff(*args) -> None:
    subprocess.run([get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


def recortar_tomas(tomas: list[Toma], maximo: float = MAX_TOTAL - PORTADA_S - PLACA_S - MARGEN_S) -> list[Toma]:
    # Cada toma dura un número entero de frames: ffmpeg redondea hacia arriba y el desvío se acumula entre tomas.
    resultado, frames_total, frames_max = [], 0, math.floor(maximo * FPS)
    for t in tomas:
        frames = min(math.floor(t.duracion * FPS + 1e-6), frames_max - frames_total)
        if frames <= 0:
            continue
        resultado.append(Toma(t.archivo, t.inicio, t.inicio + frames / FPS, t.subtitulo, t.con_audio))
        frames_total += frames
    return resultado


def _segmento_toma(t: Toma, subtitulo_png: Path | None, destino: Path) -> None:
    entradas = ["-ss", t.inicio, "-t", t.duracion, "-i", t.archivo]
    if subtitulo_png:
        entradas += ["-i", subtitulo_png]
        filtro, audio = f"[0:v]{ENCUADRE}[b];[b][1:v]overlay=0:0[v]", 2
    else:
        filtro, audio = f"[0:v]{ENCUADRE}[v]", 1
    pista = "0:a" if t.con_audio else f"{audio}:a"
    _ff(*entradas, *SILENCIO, "-filter_complex", filtro, "-map", "[v]", "-map", pista,
        "-t", t.duracion, *CODIFICAR, destino)


def _segmento_imagen(png: Path, segundos: float, destino: Path, fundido: bool = False) -> None:
    filtro = f"[0:v]{ENCUADRE}" + (",fade=t=in:st=0:d=0.3" if fundido else "") + "[v]"
    _ff("-loop", "1", "-t", segundos, "-i", png, *SILENCIO, "-filter_complex", filtro,
        "-map", "[v]", "-map", "1:a", "-t", segundos, *CODIFICAR, destino)


def hacer_preview(final: Path, preview: Path, limite: int = LIMITE_PREVIEW) -> Path:
    _, _, dur = info(final)
    kbps = int(min(2500, limite * 8 / 1024 / max(dur, 1.0) * 0.85 - 96))
    _ff("-i", final, "-vf", "scale=720:1280", "-c:v", "libx264", "-b:v", f"{kbps}k", "-maxrate", f"{kbps}k",
        "-bufsize", f"{kbps * 2}k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart", preview)
    return Path(preview)


def armar_reel(tomas: list[Toma], portada_png: Path, placa_png: Path, carpeta: Path, nombre: str) -> tuple[Path, Path]:
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    tomas = recortar_tomas(tomas)
    final = carpeta / f"{nombre}.mp4"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        partes = [tmp / "000_portada.mp4"]
        _segmento_imagen(portada_png, PORTADA_S, partes[0])
        for i, t in enumerate(tomas, 1):
            sub = render_png("subtitulo", {"texto": t.subtitulo}, tmp / f"sub_{i:03}.png", transparente=True) if t.subtitulo else None
            parte = tmp / f"{i:03}_toma.mp4"
            _segmento_toma(t, sub, parte)
            partes.append(parte)
        placa = tmp / "999_placa.mp4"
        _segmento_imagen(placa_png, PLACA_S, placa, fundido=True)
        partes.append(placa)
        lista = tmp / "lista.txt"
        lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
        # Re-codificar la unión: con copia directa, el relleno del audio AAC de cada tramo abre huecos
        # que se acumulan y el reel supera los 90 s.
        _ff("-f", "concat", "-safe", "0", "-i", lista, "-af", "aresample=async=1", *CODIFICAR,
            "-t", MAX_TOTAL, "-movflags", "+faststart", final)
    preview = hacer_preview(final, carpeta / f"{nombre}-preview.mp4")
    return final, preview
