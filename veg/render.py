from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLAS = RAIZ / "plantillas"
TAMANOS = {
    "post_paquete": (1080, 1350), "lamina": (1080, 1350),
    "portada_reel": (1080, 1920), "historia": (1080, 1920),
    "placa_cierre": (1080, 1920), "subtitulo": (1080, 1920),
}
_env = Environment(loader=FileSystemLoader(PLANTILLAS), autoescape=select_autoescape(["html", "j2"]))


def html(plantilla: str, datos: dict) -> str:
    datos = {k: (v.resolve().as_uri() if isinstance(v, Path) else v) for k, v in datos.items()}
    datos.setdefault("foto", None)
    return _env.get_template(f"{plantilla}.html.j2").render(raiz=PLANTILLAS.as_uri(), **datos)


def _abrir_navegador(p):
    # En esta PC el Chromium descargado por Playwright no puede ejecutarse; Edge (que trae Windows) sí.
    try:
        return p.chromium.launch(channel="msedge")
    except PlaywrightError:
        return p.chromium.launch()


def render_png(plantilla: str, datos: dict, salida: Path, transparente: bool = False) -> Path:
    ancho, alto = TAMANOS[plantilla]
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    temporal = salida.with_suffix(".tmp.html")
    temporal.write_text(html(plantilla, datos), encoding="utf-8")
    try:
        with sync_playwright() as p:
            navegador = _abrir_navegador(p)
            pagina = navegador.new_page(viewport={"width": ancho, "height": alto})
            pagina.goto(temporal.resolve().as_uri())
            pagina.evaluate("document.fonts.ready.then(() => true)")
            pagina.screenshot(path=str(salida), omit_background=transparente)
            navegador.close()
    finally:
        temporal.unlink(missing_ok=True)
    return salida
