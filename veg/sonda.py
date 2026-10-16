import re
import subprocess
from pathlib import Path

from imageio_ffmpeg import count_frames_and_secs, get_ffmpeg_exe

_DIM = re.compile(r"Video:.*?,\s(\d{2,5})x(\d{2,5})")


def info(path: Path) -> tuple[int, int, float]:
    r = subprocess.run([get_ffmpeg_exe(), "-hide_banner", "-i", str(path)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = _DIM.search(r.stderr)
    if not m:
        raise ValueError(f"No se pudo leer el video: {path}")
    _, segundos = count_frames_and_secs(str(path))
    return int(m.group(1)), int(m.group(2)), float(segundos)
