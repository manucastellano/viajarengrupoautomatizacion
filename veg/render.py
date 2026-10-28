from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from PIL import Image
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from .formato import formatear_precio

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLAS = RAIZ / "plantillas"
CHROMIUM_NUBE = Path("/opt/pw-browsers/chromium")
TAMANOS = {
    "post_paquete": (1080, 1350), "lamina": (1080, 1350),
    "lamina_linkedin": (1080, 1350), "placa_resena": (1080, 1350),
    "portada_reel": (1080, 1920), "historia": (1080, 1920),
    "placa_cierre": (1080, 1920), "subtitulo": (1080, 1920),
    "historia_postal": (1080, 1920), "historia_frase": (1080, 1920),
}
_env = Environment(loader=FileSystemLoader(PLANTILLAS), autoescape=select_autoescape(["html", "j2"]))


def html(plantilla: str, datos: dict) -> str:
    datos = {k: (v.resolve().as_uri() if isinstance(v, Path) else v) for k, v in datos.items()}
    if "precio" in datos and not isinstance(datos["precio"], str):
        datos["precio"] = formatear_precio(datos["precio"])
    datos = {k: ("" if v is None and k != "foto" else v) for k, v in datos.items()}
    datos.setdefault("foto", None)
    return _env.get_template(f"{plantilla}.html.j2").render(raiz=PLANTILLAS.as_uri(), **datos)


def _abrir_navegador(p):
    # En esta PC el Chromium descargado por Playwright no puede ejecutarse; Edge (que trae Windows) sí.
    try:
        return p.chromium.launch(channel="msedge")
    except PlaywrightError:
        pass
    try:
        return p.chromium.launch()
    except PlaywrightError:
        # En la nube el Chromium ya instalado no coincide con la versión de Playwright del venv.
        if not CHROMIUM_NUBE.exists():
            raise
        return p.chromium.launch(executable_path=str(CHROMIUM_NUBE), args=["--no-sandbox"])


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


def render_pdf(pngs: list[Path], salida: Path) -> Path:
    """Une las láminas en un PDF de una página por lámina (carrusel de documento de LinkedIn)."""
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    paginas = [Image.open(png).convert("RGB") for png in pngs]
    paginas[0].save(salida, save_all=True, append_images=paginas[1:], resolution=144)
    return salida
