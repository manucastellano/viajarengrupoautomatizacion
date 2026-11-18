"""Edición de los videos grabados el 12/11 (Bettina 1, Bettina 2 y Juana 1).

Uso: .venv/bin/python herramientas/editar_videos_2026_11.py <carpeta_videos> <carpeta_salida>

<carpeta_videos> tiene bettu1/, bettu2/ y juana/ tal como vinieron de Drive, más los JSON de
palabras con tiempos (transcripción con faster-whisper). Para cada video:
- saca la "claqueta" ("Bettina 1, toma 1") y los silencios de punta,
- une arranque + desarrollo + cierre con su audio,
- en Juana, tapa parte de la presentación con las tomas de apoyo (se sigue oyendo su voz),
- quema subtítulos (Raleway, blanco con borde) y agrega la placa de cierre con el logo,
- normaliza el volumen y exporta 1080x1920 MP4 + portada JPG.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from veg.render import render_png  # noqa: E402

FPS = 30
VF = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
COD = ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
FUENTES = RAIZ / "plantillas" / "fuentes"


def ff(*a):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, a)], check=True)


def palabras(carpeta: Path, clip: str, desde: int, correcciones: dict[int, str]) -> list[dict]:
    """Palabras del clip a partir del índice `desde` (saltea la claqueta), con correcciones por índice."""
    sesgada = json.loads((carpeta / "palabras.json").read_text(encoding="utf-8"))
    alt = carpeta / (clip.replace("/", "_") + ".json")
    lista = json.loads(alt.read_text(encoding="utf-8")) if alt.exists() else sesgada[clip]
    res = []
    for i, w in enumerate(lista):
        if i < desde:
            continue
        w = dict(w)
        w["w"] = correcciones.get(i, w["w"])
        res.append(w)
    return res


CORTAS = {"a", "al", "de", "del", "el", "la", "las", "los", "en", "y", "que", "una", "un", "se", "me", "te", "no", "san"}


def frases(ws: list[dict], max_chars: int = 24) -> list[tuple[float, float, str]]:
    """Agrupa palabras en frases cortas: corta en puntuación o al pasarse del largo,
    sin dejar una palabra corta ("de", "la", "una") colgando al final de la línea."""
    grupos, actual = [], []
    for w in ws:
        if actual and len(" ".join(x["w"] for x in actual + [w])) > max_chars:
            colgada = [] if len(actual) < 2 or actual[-1]["w"].lower() not in CORTAS else [actual.pop()]
            grupos.append(actual)
            actual = colgada
        actual.append(w)
        if w["w"][-1] in ".?!" or (w["w"][-1] == "," and len(" ".join(x["w"] for x in actual)) >= 10):
            grupos.append(actual)
            actual = []
    if actual:
        grupos.append(actual)
    out = [(g[0]["s"], g[-1]["e"], " ".join(x["w"] for x in g)) for g in grupos]
    return [(s, (out[i + 1][0] if i + 1 < len(out) else e + 0.3), t) for i, (s, e, t) in enumerate(out)]


def ass_tiempo(t: float) -> str:
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02}:{s:05.2f}"


def escribir_ass(lineas: list[tuple[float, float, str]], destino: Path):
    cab = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Raleway,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,4,2,2,90,90,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    cuerpo = "".join(f"Dialogue: 0,{ass_tiempo(s)},{ass_tiempo(e)},Sub,,0,0,0,,{t}\n" for s, e, t in lineas)
    destino.write_text(cab + cuerpo, encoding="utf-8")


def armar(nombre: str, tramos: list[dict], placa: Path, salida: Path, apoyos: list[dict] | None = None):
    """tramos: [{clip, ws}] en orden. apoyos: [{archivo, en, dur}] tiempos sobre la línea final."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        partes, lineas, t0 = [], [], 0.0
        for i, tr in enumerate(tramos):
            ws = tr["ws"]
            ini = max(ws[0]["s"] - 0.25, 0)
            fin = ws[-1]["e"] + 0.45
            parte = tmp / f"{i:02}.mp4"
            ff("-ss", f"{ini:.2f}", "-to", f"{fin:.2f}", "-i", tr["clip"], "-vf", VF, *COD, parte)
            dur = fin - ini
            for s, e, t in frases(ws):
                lineas.append((t0 + s - ini, t0 + min(e, fin) - ini, t))
            partes.append(parte)
            t0 += dur
        habla = tmp / "habla.mp4"
        lista = tmp / "l.txt"
        lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes))
        ff("-f", "concat", "-safe", "0", "-i", lista, *COD, habla)
        # tomas de apoyo encima (video), el audio sigue siendo el de la persona que habla
        if apoyos:
            entradas, filtro, prev = ["-i", habla], "", "0:v"
            for j, a in enumerate(apoyos, 1):
                entradas += ["-ss", f"{a.get('desde', 1.0):.2f}", "-t", f"{a['dur']:.2f}", "-i", a["archivo"]]
                filtro += (f"[{j}:v]{VF},setpts=PTS-STARTPTS+{a['en']:.2f}/TB[a{j}];"
                           f"[{prev}][a{j}]overlay=0:0:eof_action=pass:enable='between(t,{a['en']:.2f},{a['en'] + a['dur']:.2f})'[o{j}];")
                prev = f"o{j}"
            con_apoyo = tmp / "apoyo.mp4"
            ff(*entradas, "-filter_complex", filtro.rstrip(";"), "-map", f"[{prev}]", "-map", "0:a", *COD, con_apoyo)
            habla = con_apoyo
        ass = tmp / "subs.ass"
        escribir_ass(lineas, ass)
        con_subs = tmp / "subs.mp4"
        ff("-i", habla, "-vf", f"subtitles={ass.as_posix()}:fontsdir={FUENTES.as_posix()}",
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", *COD, con_subs)
        cierre = tmp / "cierre.mp4"
        ff("-loop", "1", "-t", "3", "-i", placa, "-f", "lavfi", "-t", "3", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
           "-vf", f"{VF},fade=t=in:st=0:d=0.3", "-map", "0:v", "-map", "1:a", *COD, cierre)
        lista.write_text(f"file '{con_subs.as_posix()}'\nfile '{cierre.as_posix()}'\n")
        final = salida / f"{nombre}.mp4"
        ff("-f", "concat", "-safe", "0", "-i", lista, "-af", "aresample=async=1", *COD, "-movflags", "+faststart", final)
        # portada: un cuadro del arranque con el título
        cuadro = salida / f"{nombre}-cuadro.jpg"
        ff("-ss", "1.0", "-i", partes[0], "-frames:v", "1", cuadro)
        return final, cuadro, lineas


def main(carpeta: Path, salida: Path):
    salida.mkdir(parents=True, exist_ok=True)
    c = carpeta
    norte = render_png("placa_cierre", {"frase": "Norte de España con los 5 sentidos"}, salida / "placa-norte.png")
    veg = render_png("placa_cierre", {"frase": "Viajar en Grupo. ¿Venís?"}, salida / "placa-juana.png")

    videos = {
        "2026-11-bettina-norte-vista": dict(placa=norte, titulo="La vista", tramos=[
            dict(clip=c / "bettu1/IMG_0084.mov", ws=palabras(c, "bettu1/IMG_0084.mov", 4, {})),
            dict(clip=c / "bettu1/IMG_0088.mov", ws=palabras(c, "bettu1/IMG_0088.mov", 0, {})),
            dict(clip=c / "bettu1/IMG_0085.mov", ws=palabras(c, "bettu1/IMG_0085.mov", 4,
                                                          {15: "querés", 18: "comentá", 19: "NORTE."})),
        ]),
        "2026-11-bettina-norte-gusto": dict(placa=norte, titulo="El gusto", tramos=[
            dict(clip=c / "bettu2/IMG_0092.mov", ws=palabras(c, "bettu2/IMG_0092.mov", 2, {})),
            dict(clip=c / "bettu2/IMG_0093.mov", ws=palabras(c, "bettu2/IMG_0093.mov", 2, {})),
            dict(clip=c / "bettu2/IMG_0094.mov", ws=palabras(c, "bettu2/IMG_0094.mov", 0,
                                                          {1: "Norte", 6: "Comentá", 7: "NORTE"})),
        ]),
        "2026-11-juana-presentacion": dict(placa=veg, titulo="Hola, soy Juana", tramos=[
            dict(clip=c / "juana/presentacion.mov", ws=palabras(c, "juana/presentacion.mov", 8,
                                                             {14: "viajes", 15: "en", 16: "Viajar", 18: "Grupo.",
                                                              61: "dudes"})),
        ]),
    }
    for nombre, v in videos.items():
        apoyos = None
        if nombre.endswith("juana-presentacion"):
            # "las salidas grupales ... consejos para que puedas viajar tranquilo" va tapado con Juana trabajando
            ws = v["tramos"][0]["ws"]
            ini = ws[0]["s"] - 0.25
            t_sal = next(w["s"] for w in ws if w["w"] == "las" and w["s"] > 15) - ini
            t_tam = next(w["s"] for w in ws if w["w"] == "también") - ini
            t_fin = next(w["e"] for w in ws if w["w"].startswith("tranquilo")) - ini
            apoyos = [dict(archivo=c / "juana/apoyo.mov", en=t_sal, dur=t_tam - t_sal, desde=2.0),
                      dict(archivo=c / "juana/apoyo 3.mov", en=t_tam, dur=t_fin - t_tam, desde=1.0)]
        final, cuadro, lineas = armar(nombre, v["tramos"], v["placa"], salida, apoyos)
        render_png("portada_reel", {"foto": cuadro, "titulo": v["titulo"], "posicion": "abajo"},
                   salida / f"{nombre}-portada.png")
        (salida / f"{nombre}-subtitulos.txt").write_text("\n".join(t for _, _, t in lineas), encoding="utf-8")
        print("ok", final)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
