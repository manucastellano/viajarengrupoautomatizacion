# Community Manager VEG Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir el sistema que, con el pedido "armá <mes>", produce el calendario, los textos, las gráficas y los reels del mes de Instagram de Viajar en Grupo y los publica en un tablero web donde Manuel aprueba o pide cambios.

**Architecture:** Un paquete Python (`veg/`) con funciones puras y testeadas para lo determinístico: modelos, calendario, formato de precios, revisión automática, render de plantillas HTML a PNG (Playwright) y armado de reels (ffmpeg vía imageio-ffmpeg). El juicio (investigar webs, elegir temas, escribir textos, elegir tomas) lo hacen agentes de Claude Code guiados por archivos `agentes/*.md`, orquestados por la skill de proyecto `arma-mes`. El tablero es un artifact de claude.ai (HTML + capacidades `db`, `downloads`, `user`) que Claude llena con `ArtifactData`.

**Tech Stack:** Python 3.13, pytest, Jinja2, Playwright (Chromium), Pillow, imageio-ffmpeg; HTML/CSS/JS sin librerías para el tablero.

**Spec:** `docs/specs/2026-10-15-community-manager-veg-design.md`

**Prerequisito (antes de la Tarea 1):** mover la sesión a la carpeta definitiva del proyecto (por ejemplo `Documentos/Community Manager VEG`). Todas las rutas de este plan son relativas a esa carpeta. Copiar ahí `docs/` de la carpeta temporal actual.

## Global Constraints

- Lienzos: post y lámina 1080×1350; historia, portada y placa 1080×1920.
- Reel: 1080×1920, 30 fps, duración total ≤ 90 s (1 s portada + tomas + 3 s placa de cierre).
- Preview de reel para el tablero: 720×1280, ≤ 18 MB (el tablero acepta archivos de hasta 20 MB).
- Colores y tipografías: solo los del manual (`selva #1F2B20`, `bosque #2A3C2E`, `turquesa #28AAA3`, `turquesa-profundo #0E7A75`, `dorado #C3A065`, `dorado-profundo #AB844A`, `salvia #7A9F85`, `crema #FAF6EF`, `crema-profunda #F0EBE4`, `blanco #FFFFFF`, `tinta-suave #595959`, `whatsapp #13824A`); titulares en Unica One en mayúsculas, textos en Raleway.
- Grilla: lunes 19:00 post/carrusel, miércoles 20:00 reel, viernes 13:00 post de venta, historias lunes a viernes.
- Rotación por semana k (0-based, k % 4): reel `[especial, paquete, destino, agencia]`; viernes `[especial, paquete, especial, paquete]`; lunes `[educativo, destino, educativo, agencia]`.
- Venta: solo salidas con cupo `disponible` o `ultimos` verificado el mismo día; nunca las que parten dentro del mes calendario; las más próximas primero. "ESPECIAL DE AGENCIA" solo para salidas propias (`especial: true`), hoy Norte de España 24 may – 10 jun 2027.
- Precio siempre "desde" + base; sin precio → "CONSULTÁ CUPOS". Toda pieza de venta lleva "Leg. 19725 · Precios sujetos a disponibilidad y cambio".
- Hashtags: 5 a 8, `#viajarengrupo` primero. Titular ≤ 5 palabras. Un llamado a la acción.
- WhatsApp: +54 9 11 5944-4920. Web: viajarengrupo.tur.ar. Instagram: @viajar.en.grupo.
- IA generativa solo para ambientar; nunca hoteles, comidas, actividades o personas de un paquete, ni Bettina.
- Nada se publica en Instagram desde el sistema.

## Review Focus

1. Clip horizontal (1920×1080) o con otra proporción → el reel sale 1080×1920 recortado al centro, sin deformar. Test en Tarea 6.
2. Tomas que suman más de 86 s → el reel final dura ≤ 90 s. Test en Tarea 6.
3. Mes con 5 lunes que empieza a mitad de semana (noviembre 2026) → la 5.ª semana repite el esquema de la semana 1. Test en Tarea 3.
4. Salida con precio "a consultar" (`precio_desde = None`) → la pieza muestra "CONSULTÁ CUPOS", nunca "USD 0" ni "None". Tests en Tareas 2 y 5.
5. Reel con material muy "pesado" (mucho detalle/movimiento) → la preview igual pesa ≤ 18 MB. Test en Tarea 6.

---

## File Structure

```
requirements.txt                 dependencias
pytest.ini                       config de tests
veg/__init__.py
veg/modelos.py                   Salida, Pieza, carga/guardado JSON
veg/formato.py                   precios y rangos de fechas en castellano
veg/calendario.py                grilla mensual + asignación de salidas
veg/revisor.py                   checklist automática del manual
veg/render.py                    plantilla HTML → PNG (Playwright)
veg/sonda.py                     ancho, alto y duración de un video
veg/reel.py                      armado de reel + preview
veg/tablero.py                   filas para la base del tablero + página del mes
plantillas/base.css              tokens y fuentes locales
plantillas/fuentes/*.ttf         Unica One, Raleway
plantillas/logo-circular.png     logo oficial
plantillas/{post_paquete,portada_reel,historia,lamina,placa_cierre,subtitulo}.html.j2
tablero/index.html               página del tablero (plantilla por mes)
agentes/{investigador,estratega,copywriter,disenador,editor-video,revisor}.md
.claude/skills/arma-mes/SKILL.md orquestación de "armá <mes>"
CLAUDE.md                        contexto del proyecto
tests/...
material/                        fotos y clips (no se versiona)
meses/AAAA-MM/                   salidas.json, calendario.json, piezas/, finales/ (no se versiona)
```

---

### Task 1: Base del proyecto y modelos

**Files:**
- Create: `requirements.txt`, `pytest.ini`, `.gitignore`, `veg/__init__.py`, `veg/modelos.py`
- Create: `plantillas/fuentes/UnicaOne-Regular.ttf`, `plantillas/fuentes/Raleway.ttf`, `plantillas/logo-circular.png`
- Test: `tests/test_modelos.py`

**Interfaces:**
- Produces: `Salida`, `Pieza` (dataclasses), `Salida.vendible -> bool`, `guardar(path, objs)`, `cargar_salidas(path) -> list[Salida]`, `cargar_piezas(path) -> list[Pieza]`, constantes `CUPOS`, `FORMATOS`, `PILARES`, `ESTADOS`.

- [ ] **Step 1: Inicializar repo, dependencias y recursos**

```bash
git init
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m playwright install chromium
mkdir -p plantillas/fuentes veg tests agentes tablero material meses
curl -L -o plantillas/fuentes/UnicaOne-Regular.ttf "https://github.com/google/fonts/raw/main/ofl/unicaone/UnicaOne-Regular.ttf"
curl -L -o plantillas/fuentes/Raleway.ttf "https://github.com/google/fonts/raw/main/ofl/raleway/Raleway%5Bwght%5D.ttf"
```
(Crear `requirements.txt` antes del `pip install`.) Copiar el logo publicado en el manual a `plantillas/logo-circular.png` (se descarga con Artifact `read`, `url` del manual y `path` = `c4722e25534c8b0ed90b45356b4663bd`).

`requirements.txt`:
```
pytest==8.3.3
jinja2==3.1.4
playwright==1.48.0
pillow==11.0.0
imageio-ffmpeg==0.5.1
```
`pytest.ini`:
```ini
[pytest]
testpaths = tests
markers =
    lento: tests que codifican video o abren Chromium
```
`.gitignore`:
```
.venv/
__pycache__/
material/
meses/
```
`veg/__init__.py` y `tests/__init__.py`: vacíos.

- [ ] **Step 2: Write the failing test**

`tests/test_modelos.py`:
```python
from datetime import date
import pytest
from veg.modelos import Salida, Pieza, guardar, cargar_salidas, cargar_piezas


def salida(**kw):
    base = dict(id="norte-espana-2027", destino="Norte de España", fecha_salida=date(2027, 5, 24),
                duracion="18 días", operador="Viajar en Grupo", url="https://www.viajarengrupo.tur.ar/norte-espana-2027",
                cupo="disponible", verificado_en=date(2026, 10, 18), precio_desde=9680, suplemento_single=2290, especial=True)
    base.update(kw)
    return Salida(**base)


def test_salida_ida_y_vuelta_json(tmp_path):
    ruta = tmp_path / "salidas.json"
    guardar(ruta, [salida()])
    assert cargar_salidas(ruta) == [salida()]


def test_pieza_ida_y_vuelta_json(tmp_path):
    p = Pieza(id="2026-11-04-reel", fecha=date(2026, 11, 4), hora="20:00", formato="reel",
              pilar="especial", tema="Norte de España con los 5 sentidos", hashtags=["#viajarengrupo"])
    ruta = tmp_path / "piezas.json"
    guardar(ruta, [p])
    assert cargar_piezas(ruta) == [p]


def test_cupo_invalido():
    with pytest.raises(ValueError):
        salida(cupo="lleno")


@pytest.mark.parametrize("cupo,vendible", [("disponible", True), ("ultimos", True), ("agotado", False), ("sin_verificar", False)])
def test_vendible(cupo, vendible):
    assert salida(cupo=cupo).vendible is vendible
```

- [ ] **Step 3: Run test to verify it fails**

Run: `.venv/Scripts/python -m pytest tests/test_modelos.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'veg.modelos'`

- [ ] **Step 4: Write minimal implementation**

`veg/modelos.py`:
```python
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

CUPOS = ("disponible", "ultimos", "agotado", "sin_verificar")
FORMATOS = ("reel", "post", "carrusel", "historias")
PILARES = ("especial", "paquete", "destino", "educativo", "agencia")
ESTADOS = ("pendiente", "aprobada", "cambios", "descartada")


@dataclass
class Salida:
    id: str
    destino: str
    fecha_salida: date
    duracion: str
    operador: str
    url: str
    cupo: str
    verificado_en: date
    precio_desde: float | None = None
    moneda: str = "USD"
    base: str = "por persona en base doble"
    suplemento_single: float | None = None
    especial: bool = False
    fecha_regreso: date | None = None

    def __post_init__(self):
        if self.cupo not in CUPOS:
            raise ValueError(f"cupo inválido: {self.cupo}")

    @property
    def vendible(self) -> bool:
        return self.cupo in ("disponible", "ultimos")


@dataclass
class Pieza:
    id: str
    fecha: date
    hora: str
    formato: str
    pilar: str
    tema: str
    salida_id: str | None = None
    titulo: str = ""
    texto: str = ""
    hashtags: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    version: int = 1
    estado: str = "pendiente"
    comentario: str = ""


def _a_json(obj) -> dict:
    return {k: (v.isoformat() if isinstance(v, date) else v) for k, v in asdict(obj).items()}


def _con_fechas(d: dict, claves: set[str]) -> dict:
    return {k: (date.fromisoformat(v) if k in claves and isinstance(v, str) else v) for k, v in d.items()}


def guardar(path, objs) -> None:
    Path(path).write_text(json.dumps([_a_json(o) for o in objs], ensure_ascii=False, indent=2), encoding="utf-8")


def cargar_salidas(path) -> list[Salida]:
    filas = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Salida(**_con_fechas(d, {"fecha_salida", "verificado_en", "fecha_regreso"})) for d in filas]


def cargar_piezas(path) -> list[Pieza]:
    filas = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Pieza(**_con_fechas(d, {"fecha"})) for d in filas]
```

- [ ] **Step 5: Run test to verify it passes**

Run: `.venv/Scripts/python -m pytest tests/test_modelos.py -v`
Expected: 7 passed

- [ ] **Step 6: Commit**

```bash
git add requirements.txt pytest.ini .gitignore veg plantillas tests docs
git commit -m "feat: base del proyecto y modelos Salida/Pieza"
```

---

### Task 2: Formato de precios y fechas

**Files:**
- Create: `veg/formato.py`
- Test: `tests/test_formato.py`

**Interfaces:**
- Produces: `formatear_precio(monto: float | None, moneda: str = "USD") -> str`, `rango_fechas(desde: date, hasta: date) -> str`, `LETRA_CHICA_VENTA: str`

- [ ] **Step 1: Write the failing test**

`tests/test_formato.py`:
```python
from datetime import date
from veg.formato import formatear_precio, rango_fechas, LETRA_CHICA_VENTA


def test_precio_con_miles():
    assert formatear_precio(9680) == "USD 9.680"


def test_precio_millon_y_decimales():
    assert formatear_precio(1234567.4) == "USD 1.234.567"


def test_precio_a_consultar():
    assert formatear_precio(None) == "CONSULTÁ CUPOS"


def test_rango_distintos_meses():
    assert rango_fechas(date(2027, 5, 24), date(2027, 6, 10)) == "24 may – 10 jun 2027"


def test_rango_mismo_mes():
    assert rango_fechas(date(2026, 11, 6), date(2026, 11, 20)) == "6 – 20 nov 2026"


def test_rango_distintos_anios():
    assert rango_fechas(date(2026, 12, 28), date(2027, 1, 8)) == "28 dic 2026 – 8 ene 2027"


def test_letra_chica():
    assert LETRA_CHICA_VENTA == "Leg. 19725 · Precios sujetos a disponibilidad y cambio"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python -m pytest tests/test_formato.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'veg.formato'`

- [ ] **Step 3: Write minimal implementation**

`veg/formato.py`:
```python
from datetime import date

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
LETRA_CHICA_VENTA = "Leg. 19725 · Precios sujetos a disponibilidad y cambio"


def formatear_precio(monto: float | None, moneda: str = "USD") -> str:
    if monto is None:
        return "CONSULTÁ CUPOS"
    return f"{moneda} {round(monto):,}".replace(",", ".")


def rango_fechas(desde: date, hasta: date) -> str:
    if desde.year != hasta.year:
        return f"{desde.day} {MESES[desde.month - 1]} {desde.year} – {hasta.day} {MESES[hasta.month - 1]} {hasta.year}"
    if desde.month != hasta.month:
        return f"{desde.day} {MESES[desde.month - 1]} – {hasta.day} {MESES[hasta.month - 1]} {hasta.year}"
    return f"{desde.day} – {hasta.day} {MESES[hasta.month - 1]} {hasta.year}"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python -m pytest tests/test_formato.py -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add veg/formato.py tests/test_formato.py
git commit -m "feat: formato de precios y rangos de fechas"
```

---

### Task 3: Calendario mensual

**Files:**
- Create: `veg/calendario.py`
- Test: `tests/test_calendario.py`

**Interfaces:**
- Consumes: `Salida`, `Pieza` (Task 1)
- Produces: `armar_calendario(anio: int, mes: int, salidas: list[Salida], hoy: date) -> list[Pieza]` (ordenadas por fecha y hora; `tema` vacío salvo historias, lo completa el estratega), `salidas_vendibles(salidas, anio, mes, hoy) -> list[Salida]`, `TEMA_HISTORIAS: dict[int, str]`

- [ ] **Step 1: Write the failing test**

`tests/test_calendario.py`:
```python
from datetime import date
from veg.calendario import armar_calendario, salidas_vendibles
from veg.modelos import Salida

HOY = date(2026, 10, 18)


def s(id, salida, cupo="disponible", verificado=HOY, especial=False):
    return Salida(id=id, destino=id, fecha_salida=salida, duracion="10 días", operador="Op", url="https://x",
                  cupo=cupo, verificado_en=verificado, especial=especial)


ESPECIAL = s("norte-espana-2027", date(2027, 5, 24), especial=True)
PERU = s("peru", date(2027, 3, 1))
MERCADILLOS = s("mercadillos", date(2026, 12, 2))
COREA = s("corea", date(2026, 11, 4))            # parte dentro del mes: no se vende
AGOTADA = s("agotada", date(2027, 1, 10), cupo="agotado")
VIEJA = s("vieja", date(2027, 2, 1), verificado=date(2026, 10, 1))
TODAS = [ESPECIAL, PERU, MERCADILLOS, COREA, AGOTADA, VIEJA]


def test_cantidad_de_piezas_noviembre_2026():
    piezas = armar_calendario(2026, 11, TODAS, HOY)
    por_formato = {}
    for p in piezas:
        por_formato[p.formato] = por_formato.get(p.formato, 0) + 1
    # 5 lunes (2,9,16,23,30), 4 miércoles, 4 viernes, 21 días hábiles
    assert por_formato["reel"] == 4
    assert por_formato["historias"] == 21
    assert por_formato.get("post", 0) + por_formato.get("carrusel", 0) == 9


def test_rotacion_de_reels():
    reels = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.formato == "reel"]
    assert [p.pilar for p in reels] == ["especial", "paquete", "destino", "agencia"]
    assert [p.fecha.day for p in reels] == [4, 11, 18, 25]
    assert all(p.hora == "20:00" for p in reels)


def test_quinto_lunes_repite_semana_uno():
    lunes = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.fecha.weekday() == 0 and p.formato != "historias"]
    assert [p.pilar for p in lunes] == ["educativo", "destino", "educativo", "agencia", "educativo"]
    assert all(p.formato == "carrusel" for p in lunes if p.pilar in ("educativo", "destino"))


def test_viernes_de_venta():
    viernes = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.fecha.weekday() == 4 and p.formato != "historias"]
    assert [p.pilar for p in viernes] == ["especial", "paquete", "especial", "paquete"]
    assert all(p.hora == "13:00" and p.formato == "post" for p in viernes)


def test_especial_va_con_la_salida_propia():
    piezas = armar_calendario(2026, 11, TODAS, HOY)
    assert {p.salida_id for p in piezas if p.pilar == "especial"} == {"norte-espana-2027"}


def test_paquetes_por_fecha_de_salida_y_sin_excluidas():
    paquetes = [p for p in armar_calendario(2026, 11, TODAS, HOY) if p.pilar == "paquete"]
    # en orden cronológico de publicación: mié 11 (reel), vie 13, vie 27
    assert [p.salida_id for p in paquetes] == ["mercadillos", "peru", "mercadillos"]


def test_vendibles_excluye_mes_actual_agotadas_y_no_verificadas():
    assert [x.id for x in salidas_vendibles(TODAS, 2026, 11, HOY)] == ["mercadillos", "peru"]


def test_sin_paquetes_pasa_a_destino():
    piezas = armar_calendario(2026, 11, [ESPECIAL], HOY)
    assert not [p for p in piezas if p.pilar == "paquete"]
    assert all(p.salida_id is None for p in piezas if p.pilar == "destino")


def test_sin_especial_verificado_pasa_a_destino():
    piezas = armar_calendario(2026, 11, [PERU], HOY)
    assert not [p for p in piezas if p.pilar == "especial"]


def test_historias_tema_por_dia_e_ids_unicos():
    piezas = armar_calendario(2026, 11, TODAS, HOY)
    historias = {p.fecha: p for p in piezas if p.formato == "historias"}
    assert historias[date(2026, 11, 3)].tema == "encuesta de destino"
    ids = [p.id for p in piezas]
    assert len(ids) == len(set(ids))
    assert "2026-11-04-reel" in ids
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python -m pytest tests/test_calendario.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'veg.calendario'`

- [ ] **Step 3: Write minimal implementation**

`veg/calendario.py`:
```python
from __future__ import annotations

import calendar
from datetime import date

from .modelos import Pieza, Salida

REEL = ["especial", "paquete", "destino", "agencia"]
VIERNES = ["especial", "paquete", "especial", "paquete"]
LUNES = ["educativo", "destino", "educativo", "agencia"]
TEMA_HISTORIAS = {0: "tip", 1: "encuesta de destino", 2: "reel y cupos", 3: "Bettina / detrás de escena", 4: "próximas salidas"}


def _dias(anio: int, mes: int, dia_semana: int) -> list[date]:
    ultimo = calendar.monthrange(anio, mes)[1]
    return [date(anio, mes, d) for d in range(1, ultimo + 1) if date(anio, mes, d).weekday() == dia_semana]


def salidas_vendibles(salidas: list[Salida], anio: int, mes: int, hoy: date) -> list[Salida]:
    validas = [
        x for x in salidas
        if x.vendible and x.verificado_en == hoy and not x.especial
        and (x.fecha_salida.year, x.fecha_salida.month) > (anio, mes)
    ]
    return sorted(validas, key=lambda x: x.fecha_salida)


def armar_calendario(anio: int, mes: int, salidas: list[Salida], hoy: date) -> list[Pieza]:
    especial = next((x for x in salidas if x.especial and x.vendible and x.verificado_en == hoy), None)
    paquetes = salidas_vendibles(salidas, anio, mes, hoy)

    huecos: list[tuple[date, str, str, str]] = []  # (fecha, hora, formato, pilar)
    for k, d in enumerate(_dias(anio, mes, 0)):
        huecos.append((d, "19:00", "post", LUNES[k % 4]))
    for k, d in enumerate(_dias(anio, mes, 2)):
        huecos.append((d, "20:00", "reel", REEL[k % 4]))
    for k, d in enumerate(_dias(anio, mes, 4)):
        huecos.append((d, "13:00", "post", VIERNES[k % 4]))
    huecos.sort(key=lambda h: (h[0], h[1]))

    piezas: list[Pieza] = []
    i_paquete = 0
    for fecha, hora, formato, pilar in huecos:
        salida_id = None
        if pilar == "especial":
            if especial:
                salida_id = especial.id
            else:
                pilar = "destino"
        elif pilar == "paquete":
            if paquetes:
                salida_id = paquetes[i_paquete % len(paquetes)].id
                i_paquete += 1
            else:
                pilar = "destino"
        if formato == "post" and pilar in ("educativo", "destino") and fecha.weekday() == 0:
            formato = "carrusel"
        piezas.append(Pieza(id=f"{fecha.isoformat()}-{formato}", fecha=fecha, hora=hora, formato=formato,
                            pilar=pilar, tema="", salida_id=salida_id))

    ultimo = calendar.monthrange(anio, mes)[1]
    for d in range(1, ultimo + 1):
        fecha = date(anio, mes, d)
        if fecha.weekday() < 5:
            piezas.append(Pieza(id=f"{fecha.isoformat()}-historias", fecha=fecha, hora="10:00", formato="historias",
                                pilar="agencia", tema=TEMA_HISTORIAS[fecha.weekday()]))

    return sorted(piezas, key=lambda p: (p.fecha, p.hora))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python -m pytest tests/test_calendario.py -v`
Expected: 10 passed

- [ ] **Step 5: Commit**

```bash
git add veg/calendario.py tests/test_calendario.py
git commit -m "feat: calendario mensual con rotación de pilares y selección de salidas"
```

---

### Task 4: Revisor automático

**Files:**
- Create: `veg/revisor.py`
- Test: `tests/test_revisor.py`

**Interfaces:**
- Consumes: `Pieza`, `Salida` (Task 1)
- Produces: `revisar(pieza: Pieza, salida: Salida | None, hoy: date) -> list[str]` (lista vacía = aprobada por el revisor; cada string explica un problema en castellano)

- [ ] **Step 1: Write the failing test**

`tests/test_revisor.py`:
```python
from datetime import date
from veg.modelos import Pieza, Salida
from veg.revisor import revisar

HOY = date(2026, 10, 24)
HASHTAGS = ["#viajarengrupo", "#viajesgrupales", "#agenciadeviajes", "#españa", "#nortedeespaña"]
NORTE = Salida(id="norte", destino="Norte de España", fecha_salida=date(2027, 5, 24), duracion="18 días",
               operador="Viajar en Grupo", url="https://x", cupo="disponible", verificado_en=HOY,
               precio_desde=9680, especial=True)


def pieza(**kw):
    base = dict(id="2026-11-06-post", fecha=date(2026, 11, 6), hora="13:00", formato="post", pilar="especial",
                tema="Norte de España", salida_id="norte", titulo="Norte de España",
                texto="Del 24 de mayo al 10 de junio de 2027. Desde USD 9.680. ¿Nos acompañás? Escribinos por WhatsApp al +54 9 11 5944-4920 ✈️",
                hashtags=HASHTAGS)
    base.update(kw)
    return Pieza(**base)


def test_pieza_correcta_sin_problemas():
    assert revisar(pieza(), NORTE, HOY) == []


def test_titular_largo():
    assert "El titular tiene más de 5 palabras" in revisar(pieza(titulo="El norte de España con los cinco sentidos"), NORTE, HOY)


def test_hashtags():
    problemas = revisar(pieza(hashtags=["#viajes", "#viajarengrupo"]), NORTE, HOY)
    assert "Debe tener entre 5 y 8 hashtags" in problemas
    assert "El primer hashtag debe ser #viajarengrupo" in problemas


def test_sin_cta():
    assert "Falta un llamado a la acción" in revisar(pieza(texto="Un viaje soñado. Desde USD 9.680."), NORTE, HOY)


def test_precio_sin_desde():
    assert 'El precio va con "desde"' in revisar(pieza(texto="USD 9.680. Escribinos por WhatsApp."), NORTE, HOY)


def test_cupo_no_verificado_hoy():
    vieja = Salida(**{**NORTE.__dict__, "verificado_en": date(2026, 10, 18)})
    assert "Cupo de Norte de España no verificado hoy" in revisar(pieza(), vieja, HOY)


def test_especial_con_salida_de_mayorista():
    mayorista = Salida(**{**NORTE.__dict__, "especial": False})
    assert "Solo las salidas propias pueden ir como especial de agencia" in revisar(pieza(), mayorista, HOY)


def test_venta_sin_salida():
    assert "Pieza de venta sin salida asociada" in revisar(pieza(), None, HOY)


def test_mayusculas_sostenidas():
    assert "Mayúsculas sostenidas en el texto" in revisar(pieza(texto="ÚLTIMOS LUGARES DISPONIBLES YA. Escribinos por WhatsApp."), NORTE, HOY)


def test_historias_no_exigen_hashtags_ni_titular():
    h = pieza(formato="historias", pilar="agencia", salida_id=None, titulo="", texto="", hashtags=[])
    assert revisar(h, None, HOY) == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python -m pytest tests/test_revisor.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'veg.revisor'`

- [ ] **Step 3: Write minimal implementation**

`veg/revisor.py`:
```python
from __future__ import annotations

import re
from datetime import date

from .modelos import Pieza, Salida

CTAS = ("whatsapp", "link en bio", "escribinos", "dejanos tu comentario", "sumate", "mensaje privado")
_MAYUSCULAS = re.compile(r"\b[A-ZÁÉÍÓÚÑ]{4,}(?:\s+[A-ZÁÉÍÓÚÑ]{4,}){2,}\b")
_PRECIO = re.compile(r"\bUSD\s?\d[\d.]*")


def revisar(pieza: Pieza, salida: Salida | None, hoy: date) -> list[str]:
    problemas: list[str] = []
    if pieza.formato != "historias":
        if len(pieza.titulo.split()) > 5:
            problemas.append("El titular tiene más de 5 palabras")
        if not 5 <= len(pieza.hashtags) <= 8:
            problemas.append("Debe tener entre 5 y 8 hashtags")
        if not pieza.hashtags or pieza.hashtags[0] != "#viajarengrupo":
            problemas.append("El primer hashtag debe ser #viajarengrupo")
        if not any(c in pieza.texto.lower() for c in CTAS):
            problemas.append("Falta un llamado a la acción")
    if _PRECIO.search(pieza.texto) and "desde" not in pieza.texto.lower():
        problemas.append('El precio va con "desde"')
    if _MAYUSCULAS.search(pieza.texto):
        problemas.append("Mayúsculas sostenidas en el texto")
    if pieza.pilar in ("especial", "paquete"):
        if salida is None:
            problemas.append("Pieza de venta sin salida asociada")
        else:
            if salida.verificado_en != hoy:
                problemas.append(f"Cupo de {salida.destino} no verificado hoy")
            if not salida.vendible:
                problemas.append(f"{salida.destino} sin cupo")
            if pieza.pilar == "especial" and not salida.especial:
                problemas.append("Solo las salidas propias pueden ir como especial de agencia")
    return problemas
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python -m pytest tests/test_revisor.py -v`
Expected: 10 passed

- [ ] **Step 5: Commit**

```bash
git add veg/revisor.py tests/test_revisor.py
git commit -m "feat: revisor automático con la checklist del manual"
```

---

### Task 5: Plantillas y render a PNG

**Files:**
- Create: `plantillas/base.css`, `plantillas/post_paquete.html.j2`, `plantillas/portada_reel.html.j2`, `plantillas/historia.html.j2`, `plantillas/lamina.html.j2`, `plantillas/placa_cierre.html.j2`, `plantillas/subtitulo.html.j2`, `veg/render.py`
- Test: `tests/test_render.py`

**Interfaces:**
- Consumes: `formatear_precio` (Task 2)
- Produces: `html(plantilla: str, datos: dict) -> str`, `render_png(plantilla: str, datos: dict, salida: Path, transparente: bool = False) -> Path`, `TAMANOS: dict[str, tuple[int, int]]`. Datos por plantilla:
  - `post_paquete`: `etiqueta, titulo, subtitulo, precio, letra_chica, foto?`
  - `portada_reel`: `etiqueta, titulo, subtitulo?, foto?`
  - `historia`: `etiqueta, titulo, texto, cta, foto?`
  - `lamina`: `titulo, texto?, numero?, oscuro: bool, etiqueta?`
  - `placa_cierre`: `frase`
  - `subtitulo`: `texto`
  - `foto` acepta `Path` (se convierte a `file://`) o `None` (fondo `bosque`).

- [ ] **Step 1: Write the failing test**

`tests/test_render.py`:
```python
import pytest
from PIL import Image
from veg.render import html, render_png
from veg.formato import formatear_precio

POST = dict(etiqueta="Especial de agencia", titulo="Norte de España", subtitulo="24 may – 10 jun 2027 · 18 días",
            precio=formatear_precio(9680), letra_chica="Por persona en base doble · Leg. 19725")


def test_html_post_contiene_datos_y_desde():
    h = html("post_paquete", POST)
    assert "Norte de España" in h and "USD 9.680" in h and "DESDE" in h


def test_html_precio_a_consultar_sin_desde():
    h = html("post_paquete", {**POST, "precio": formatear_precio(None)})
    assert "CONSULTÁ CUPOS" in h and "DESDE" not in h and "None" not in h


def test_html_escapa_texto():
    assert "<script>" not in html("placa_cierre", {"frase": "<script>x</script>"})


@pytest.mark.lento
@pytest.mark.parametrize("plantilla,datos,tamano", [
    ("post_paquete", POST, (1080, 1350)),
    ("portada_reel", {"etiqueta": "Recap", "titulo": "La Dolce Vita", "subtitulo": "Italia 2026"}, (1080, 1920)),
    ("historia", {"etiqueta": "Charla informativa", "titulo": "Norte de España", "texto": "Martes 18 h", "cta": "Escribinos por WhatsApp"}, (1080, 1920)),
    ("lamina", {"titulo": "5 mitos de viajar en grupo", "oscuro": True, "etiqueta": "Tips de viaje"}, (1080, 1350)),
    ("placa_cierre", {"frase": "¿Nos acompañás?"}, (1080, 1920)),
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python -m pytest tests/test_render.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'veg.render'`

- [ ] **Step 3: Write the stylesheet and templates**

`plantillas/base.css`:
```css
@font-face{font-family:"Unica One";src:url("fuentes/UnicaOne-Regular.ttf") format("truetype")}
@font-face{font-family:"Raleway";src:url("fuentes/Raleway.ttf") format("truetype");font-weight:100 900}
:root{--selva:#1F2B20;--bosque:#2A3C2E;--turquesa:#28AAA3;--turquesa-profundo:#0E7A75;--dorado:#C3A065;--dorado-profundo:#AB844A;--salvia:#7A9F85;--crema:#FAF6EF;--crema-profunda:#F0EBE4;--blanco:#FFFFFF;--tinta-suave:#595959;--whatsapp:#13824A;--font-display:"Unica One","Arial Narrow",sans-serif;--font-texto:"Raleway",Arial,sans-serif}
html,body{margin:0;background:transparent}
.lienzo{position:relative;overflow:hidden;font-family:var(--font-texto)}
.v{width:1080px;height:1920px}.p{width:1080px;height:1350px}
.disp{font-family:var(--font-display);text-transform:uppercase;letter-spacing:.02em;margin:0;font-weight:400}
.eti{font-family:var(--font-display);text-transform:uppercase;letter-spacing:.18em;font-size:30px}
.foto{position:absolute;inset:0;background:var(--bosque) center/cover no-repeat}
.velo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(42,60,46,0) 35%,rgba(31,43,32,.85) 100%)}
.chica{font-size:22px;line-height:1.3;font-weight:500}
```

`plantillas/post_paquete.html.j2`:
```html
<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{{ raiz }}/base.css"><style>
.foto{bottom:520px}
.logo{position:absolute;top:56px;right:56px;width:140px;height:140px;border-radius:50%}
.pie{position:absolute;left:0;right:0;bottom:0;height:520px;background:var(--crema);padding:56px 72px 0;box-sizing:border-box}
.pie .eti{color:var(--turquesa-profundo)}
.pie h1{font-size:88px;line-height:.95;color:var(--selva);margin:16px 0 0}
.pie .sub{font-size:40px;font-weight:600;color:var(--selva);margin:20px 0 0}
.precio{position:absolute;right:72px;top:-70px;background:var(--turquesa-profundo);color:var(--blanco);padding:22px 40px;border-radius:999px;font-family:var(--font-display);font-size:60px;letter-spacing:.01em}
.precio small{font-size:28px;letter-spacing:.12em;margin-right:12px}
.pie .chica{position:absolute;left:72px;right:72px;bottom:44px;color:var(--tinta-suave);margin:0}
</style></head><body><div class="lienzo p">
<div class="foto"{% if foto %} style="background-image:url('{{ foto }}')"{% endif %}></div>
<img class="logo" src="{{ raiz }}/logo-circular.png" alt="">
<div class="pie">
<div class="precio">{% if precio != "CONSULTÁ CUPOS" %}<small>DESDE</small>{% endif %}{{ precio }}</div>
<span class="eti">{{ etiqueta }}</span>
<h1 class="disp">{{ titulo }}</h1>
<p class="sub">{{ subtitulo }}</p>
<p class="chica">{{ letra_chica }}</p>
</div></div></body></html>
```

`plantillas/portada_reel.html.j2`:
```html
<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{{ raiz }}/base.css"><style>
.txt{position:absolute;left:72px;right:72px;top:760px}
.txt .eti{color:var(--turquesa);display:block;margin-bottom:16px}
.txt h1{font-size:120px;line-height:.95;color:var(--blanco)}
.txt p{font-size:44px;line-height:1.2;font-weight:600;color:var(--crema);margin:24px 0 0}
</style></head><body><div class="lienzo v">
<div class="foto"{% if foto %} style="background-image:url('{{ foto }}')"{% endif %}></div><div class="velo"></div>
<div class="txt"><span class="eti">{{ etiqueta }}</span><h1 class="disp">{{ titulo }}</h1>{% if subtitulo %}<p>{{ subtitulo }}</p>{% endif %}</div>
</div></body></html>
```

`plantillas/historia.html.j2`:
```html
<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{{ raiz }}/base.css"><style>
.lienzo{background:var(--crema)}
.foto{top:250px;bottom:auto;height:740px;left:72px;right:72px}
.pill{position:absolute;left:72px;top:1040px;background:var(--turquesa);color:var(--selva);border-radius:999px;padding:18px 36px}
.t{position:absolute;left:72px;right:72px;top:1150px}
.t h1{font-size:76px;line-height:1;color:var(--selva)}
.t p{font-size:34px;line-height:1.35;font-weight:500;color:var(--selva);margin:24px 0 0}
.cta{position:absolute;left:72px;right:72px;top:1460px;background:var(--whatsapp);color:var(--blanco);border-radius:999px;text-align:center;padding:30px 0;font-size:38px;font-weight:700}
</style></head><body><div class="lienzo v">
<div class="foto"{% if foto %} style="background-image:url('{{ foto }}')"{% endif %}></div>
<span class="pill eti">{{ etiqueta }}</span>
<div class="t"><h1 class="disp">{{ titulo }}</h1><p>{{ texto }}</p></div>
<div class="cta">{{ cta }}</div>
</div></body></html>
```

`plantillas/lamina.html.j2`:
```html
<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{{ raiz }}/base.css"><style>
.claro{background:var(--crema)}.oscuro{background:var(--selva)}
.n{position:absolute;left:72px;top:110px;font-family:var(--font-display);font-size:200px;line-height:1;color:var(--dorado-profundo)}
.oscuro .n{color:var(--dorado)}
.filete{position:absolute;left:72px;width:120px;height:6px;background:var(--turquesa);top:360px}
.c{position:absolute;left:72px;right:72px;top:400px}
.c .eti{color:var(--turquesa-profundo)}.oscuro .c .eti{color:var(--turquesa)}
.c h1{font-size:88px;line-height:.95;color:var(--selva)}
.oscuro .c h1{color:var(--crema)}
.c p{font-size:34px;line-height:1.35;font-weight:500;color:var(--selva);margin:32px 0 0;max-width:820px}
.oscuro .c p{color:var(--crema)}
.portada .c{top:300px}.portada .c h1{font-size:110px;margin-top:24px}
.pie{position:absolute;left:72px;bottom:56px;font-family:var(--font-display);letter-spacing:.18em;font-size:26px;color:var(--turquesa-profundo)}
.oscuro .pie{color:var(--turquesa)}
</style></head><body><div class="lienzo p {{ 'oscuro' if oscuro else 'claro' }}{{ '' if numero else ' portada' }}">
{% if numero %}<div class="n">{{ '%02d' % numero }}</div><div class="filete"></div>{% endif %}
<div class="c">{% if etiqueta %}<span class="eti">{{ etiqueta }}</span>{% endif %}<h1 class="disp">{{ titulo }}</h1>{% if texto %}<p>{{ texto }}</p>{% endif %}</div>
<div class="pie">@viajar.en.grupo</div>
</div></body></html>
```

`plantillas/placa_cierre.html.j2`:
```html
<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{{ raiz }}/base.css"><style>
.lienzo{background:var(--selva)}
.logo{position:absolute;left:340px;top:420px;width:400px;height:400px;border-radius:50%}
.t{position:absolute;left:72px;right:72px;top:900px;text-align:center}
.t h1{font-size:110px;line-height:.95;color:var(--crema)}
.t p{font-size:40px;font-weight:600;color:var(--turquesa);margin:28px 0 0}
.t p.chica{color:var(--crema);margin-top:60px;font-size:26px;font-weight:500}
</style></head><body><div class="lienzo v">
<img class="logo" src="{{ raiz }}/logo-circular.png" alt="">
<div class="t"><h1 class="disp">{{ frase }}</h1><p>WhatsApp +54 9 11 5944-4920</p><p class="chica">viajarengrupo.tur.ar · Leg. 19725</p></div>
</div></body></html>
```

`plantillas/subtitulo.html.j2`:
```html
<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{{ raiz }}/base.css"><style>
.s{position:absolute;left:72px;right:72px;bottom:440px;text-align:center}
.s span{display:inline;background:var(--selva);color:var(--blanco);font-size:48px;line-height:1.5;font-weight:700;padding:6px 18px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
</style></head><body><div class="lienzo v"><div class="s"><span>{{ texto }}</span></div></div></body></html>
```

- [ ] **Step 4: Write the renderer**

`veg/render.py`:
```python
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
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


def render_png(plantilla: str, datos: dict, salida: Path, transparente: bool = False) -> Path:
    ancho, alto = TAMANOS[plantilla]
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    temporal = salida.with_suffix(".tmp.html")
    temporal.write_text(html(plantilla, datos), encoding="utf-8")
    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": ancho, "height": alto})
            pagina.goto(temporal.resolve().as_uri())
            pagina.evaluate("document.fonts.ready.then(() => true)")
            pagina.screenshot(path=str(salida), omit_background=transparente)
            navegador.close()
    finally:
        temporal.unlink(missing_ok=True)
    return salida
```

- [ ] **Step 5: Run test to verify it passes**

Run: `.venv/Scripts/python -m pytest tests/test_render.py -v`
Expected: 9 passed

- [ ] **Step 6: Inspección visual**

Run:
```bash
.venv/Scripts/python -c "from pathlib import Path; from veg.render import render_png; from veg.formato import formatear_precio; render_png('post_paquete', dict(etiqueta='Especial de agencia · Salida acompañada', titulo='Norte de España', subtitulo='24 may – 10 jun 2027 · 18 días', precio=formatear_precio(9680), letra_chica='Por persona en base doble · Suplemento single USD 2.290 · Leg. 19725 · Precios sujetos a disponibilidad y cambio'), Path('meses/_muestras/post.png'))"
```
Abrir `meses/_muestras/post.png` con Read y comparar contra la plantilla "Post de paquete" del manual: tipografías (no Arial), acentos, ñ y ¿ visibles, cápsula de precio sobre el corte, logo arriba a la derecha.

- [ ] **Step 7: Commit**

```bash
git add plantillas veg/render.py tests/test_render.py
git commit -m "feat: plantillas de marca y render a PNG"
```

---

### Task 6: Armado de reels

**Files:**
- Create: `veg/sonda.py`, `veg/reel.py`
- Test: `tests/conftest.py`, `tests/test_reel.py`

**Interfaces:**
- Consumes: `render_png` (Task 5)
- Produces: `info(path) -> tuple[int, int, float]` (ancho, alto, segundos); `Toma(archivo: Path, inicio: float, fin: float, subtitulo: str = "")`; `recortar_tomas(tomas, maximo=86.0) -> list[Toma]`; `armar_reel(tomas, portada_png, placa_png, carpeta, nombre) -> tuple[Path, Path]` (final, preview); `hacer_preview(final, preview, limite=18 MiB) -> Path`

- [ ] **Step 1: Write the failing test**

`tests/conftest.py`:
```python
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
```

`tests/test_reel.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python -m pytest tests/test_reel.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'veg.reel'`

- [ ] **Step 3: Write minimal implementation**

`veg/sonda.py`:
```python
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
```

`veg/reel.py`:
```python
from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from imageio_ffmpeg import get_ffmpeg_exe

from .render import render_png
from .sonda import info

ANCHO, ALTO, FPS = 1080, 1920, 30
MAX_TOTAL, PORTADA_S, PLACA_S = 90.0, 1.0, 3.0
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

    @property
    def duracion(self) -> float:
        return self.fin - self.inicio


def _ff(*args) -> None:
    subprocess.run([get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


def recortar_tomas(tomas: list[Toma], maximo: float = MAX_TOTAL - PORTADA_S - PLACA_S) -> list[Toma]:
    resultado, total = [], 0.0
    for t in tomas:
        if total >= maximo:
            break
        dur = min(t.duracion, maximo - total)
        resultado.append(Toma(t.archivo, t.inicio, t.inicio + dur, t.subtitulo))
        total += dur
    return resultado


def _segmento_toma(t: Toma, subtitulo_png: Path | None, destino: Path) -> None:
    entradas = ["-ss", t.inicio, "-t", t.duracion, "-i", t.archivo]
    if subtitulo_png:
        entradas += ["-i", subtitulo_png]
        filtro, audio = f"[0:v]{ENCUADRE}[b];[b][1:v]overlay=0:0[v]", 2
    else:
        filtro, audio = f"[0:v]{ENCUADRE}[v]", 1
    _ff(*entradas, *SILENCIO, "-filter_complex", filtro, "-map", "[v]", "-map", f"{audio}:a",
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
        _ff("-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", "-movflags", "+faststart", final)
    preview = hacer_preview(final, carpeta / f"{nombre}-preview.mp4")
    return final, preview
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/Scripts/python -m pytest tests/test_reel.py -v`
Expected: 4 passed (los marcados `lento` pueden tardar de 1 a 3 minutos)

- [ ] **Step 5: Commit**

```bash
git add veg/sonda.py veg/reel.py tests/conftest.py tests/test_reel.py
git commit -m "feat: armado de reels verticales con portada, subtítulos, placa y preview liviana"
```

---

### Task 7: Tablero de aprobación

**Files:**
- Create: `tablero/index.html`, `veg/tablero.py`
- Test: `tests/test_tablero.py`

**Interfaces:**
- Consumes: `Pieza`, `Salida` (Task 1)
- Produces: `fila(pieza: Pieza, assets: list[dict], salida: Salida | None) -> dict` con forma `{"doc_id": str, "data": dict}`; `escribir_filas(piezas, assets_por_pieza: dict[str, list[dict]], salidas: list[Salida], ruta: Path) -> Path`; `preparar_pagina(anio: int, mes: int, destino: Path) -> Path`. Cada asset es `{"id": "<32 hex>", "tipo": "imagen" | "video", "nombre": "archivo.png"}`. Colección de la base: `piezas`.

- [ ] **Step 1: Write the failing test**

`tests/test_tablero.py`:
```python
import json
from datetime import date
from veg.modelos import Pieza, Salida
from veg.tablero import escribir_filas, fila, preparar_pagina

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/Scripts/python -m pytest tests/test_tablero.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'veg.tablero'`

- [ ] **Step 3: Write `veg/tablero.py`**

```python
from __future__ import annotations

import json
from pathlib import Path

from .modelos import Pieza, Salida

RAIZ = Path(__file__).resolve().parent.parent
NOMBRES_MES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
               "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def fila(pieza: Pieza, assets: list[dict], salida: Salida | None) -> dict:
    return {"doc_id": pieza.id, "data": {
        "id": pieza.id, "fecha": pieza.fecha.isoformat(), "hora": pieza.hora, "formato": pieza.formato,
        "pilar": pieza.pilar, "tema": pieza.tema, "titulo": pieza.titulo, "texto": pieza.texto,
        "hashtags": pieza.hashtags, "assets": assets, "version": pieza.version, "estado": pieza.estado,
        "comentario": pieza.comentario,
        "verificacion": {"fuente": salida.operador, "fecha": salida.verificado_en.isoformat()} if salida else None,
    }}


def escribir_filas(piezas: list[Pieza], assets_por_pieza: dict[str, list[dict]], salidas: list[Salida], ruta: Path) -> Path:
    por_id = {s.id: s for s in salidas}
    filas = [fila(p, assets_por_pieza.get(p.id, []), por_id.get(p.salida_id)) for p in piezas]
    ruta = Path(ruta)
    ruta.write_text(json.dumps(filas, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta


def preparar_pagina(anio: int, mes: int, destino: Path) -> Path:
    plantilla = (RAIZ / "tablero" / "index.html").read_text(encoding="utf-8")
    pagina = (plantilla.replace("__TITULO__", f"{NOMBRES_MES[mes - 1]} {anio}")
                        .replace("__MES__", f"{anio}-{mes:02d}"))
    destino = Path(destino)
    destino.write_text(pagina, encoding="utf-8")
    return destino
```

- [ ] **Step 4: Write `tablero/index.html`**

```html
<title>Tablero __TITULO__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unica+One&family=Raleway:wght@500;600;700&display=swap">
<style>
/* Tablero de aprobación: resumen arriba, vista Calendario o Grilla, detalle en hoja. Paleta fija de marca (tema único claro, deliberado). */
:root{--selva:#1F2B20;--bosque:#2A3C2E;--turquesa:#28AAA3;--turquesa-profundo:#0E7A75;--dorado:#C3A065;--dorado-profundo:#AB844A;--salvia:#7A9F85;--crema:#FAF6EF;--crema-profunda:#F0EBE4;--blanco:#FFFFFF;--tinta-suave:#595959;--linea:rgba(31,43,32,.14);--ok:#13824A;--cambios:#9A5B00;--descartada:#595959;
--display:"Unica One","Arial Narrow",sans-serif;--texto:"Raleway",Arial,sans-serif;color-scheme:light}
body{background:var(--crema);color:var(--selva);font-family:var(--texto);font-size:15px;line-height:1.45;padding:16px 16px 48px}
.envoltura{max-width:1100px;margin:0 auto;display:grid;gap:20px}
.eti{font-family:var(--display);text-transform:uppercase;letter-spacing:.16em;font-size:12px;color:var(--turquesa-profundo);margin:0}
h1{font-family:var(--display);text-transform:uppercase;font-weight:400;font-size:clamp(32px,7vw,56px);line-height:.95;margin:4px 0 0;text-wrap:balance}
.resumen{display:flex;flex-wrap:wrap;gap:8px 20px;font-variant-numeric:tabular-nums}
.resumen b{font-family:var(--display);font-size:22px;font-weight:400;margin-right:4px}
.barra{height:6px;background:var(--crema-profunda)}.barra span{display:block;height:100%;background:var(--turquesa-profundo);width:0}
.vistas{display:flex;gap:8px}
.vistas button,.acciones button,.copiar{font:600 14px var(--texto);border:1px solid var(--selva);background:transparent;color:var(--selva);padding:8px 14px;cursor:pointer;border-radius:999px}
.vistas button[aria-pressed=true]{background:var(--selva);color:var(--crema)}
button:focus-visible{outline:3px solid var(--turquesa-profundo);outline-offset:2px}
button:disabled{opacity:.5;cursor:not-allowed}
.semana{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-bottom:16px}
.dia{background:var(--blanco);border:1px solid var(--linea);padding:8px;min-width:0;display:grid;gap:6px;align-content:start}
.dia h3{margin:0;font:600 12px var(--texto);color:var(--tinta-suave)}
.chip{display:grid;grid-template-columns:44px minmax(0,1fr);gap:8px;align-items:center;text-align:left;background:none;border:0;border-left:4px solid var(--c);padding:4px 6px;cursor:pointer;font:500 12px var(--texto);color:var(--selva);min-width:0}
.chip img,.chip .sin{width:44px;height:55px;object-fit:cover;background:var(--crema-profunda)}
.chip span{overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.estado{font-size:11px;font-weight:700}
.grilla{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3px;max-width:540px}
.grilla button{padding:0;border:0;cursor:pointer;aspect-ratio:4/5;background:var(--crema-profunda);position:relative;max-width:100%}
.grilla img,.grilla .sin{width:100%;height:100%;object-fit:cover;display:block}
.grilla .marca{position:absolute;top:6px;right:6px;background:var(--selva);color:var(--crema);font-size:11px;padding:2px 6px}
dialog{border:0;padding:0;width:min(720px,100%);max-height:92vh;background:var(--crema);color:var(--selva)}
dialog::backdrop{background:rgba(31,43,32,.6)}
.hoja{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;padding:16px}
@media (max-width:640px){.hoja{grid-template-columns:1fr}.semana{grid-template-columns:1fr}}
.vista-previa{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory}
.vista-previa img,.vista-previa video{width:100%;flex:none;scroll-snap-align:start;background:var(--selva);max-height:70vh;object-fit:contain}
.ficha{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 12px;font-size:13px;margin:0}.ficha dt{color:var(--tinta-suave)}.ficha dd{margin:0}
.texto{white-space:pre-wrap;background:var(--blanco);border:1px solid var(--linea);padding:10px;font-size:14px;max-height:220px;overflow:auto}
textarea{width:100%;box-sizing:border-box;font:14px var(--texto);border:1px solid var(--selva);padding:8px;min-height:80px;background:var(--blanco);color:var(--selva)}
.acciones{display:flex;flex-wrap:wrap;gap:8px}
.acciones .aprobar{background:var(--ok);border-color:var(--ok);color:var(--blanco)}
.aviso{font-size:13px;color:var(--tinta-suave)}
.cerrar{justify-self:end;background:none;border:0;font:600 14px var(--texto);cursor:pointer;color:var(--selva);padding:12px 16px 0}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style>

<div class="envoltura">
  <header>
    <p class="eti">Viajar en Grupo · Tablero de aprobación</p>
    <h1>__TITULO__</h1>
  </header>
  <section aria-label="Resumen" class="resumen" id="resumen"><span>Cargando piezas…</span></section>
  <div class="barra" aria-hidden="true"><span id="avance"></span></div>
  <div class="vistas" role="group" aria-label="Vista">
    <button id="v-cal" aria-pressed="true">Calendario</button>
    <button id="v-grilla" aria-pressed="false">Grilla de Instagram</button>
  </div>
  <main id="vista"><p class="aviso">Las piezas del mes aparecen acá cuando Claude las sube al tablero.</p></main>
</div>

<dialog id="detalle" aria-label="Detalle de la pieza">
  <div style="display:grid">
    <button class="cerrar" id="cerrar">Cerrar ✕</button>
    <div class="hoja">
      <div class="vista-previa" id="d-previa"></div>
      <div style="display:grid;gap:12px;align-content:start;min-width:0">
        <p class="eti" id="d-pilar"></p>
        <h2 id="d-titulo" style="font:400 28px var(--display);text-transform:uppercase;margin:0"></h2>
        <dl class="ficha" id="d-ficha"></dl>
        <div class="texto" id="d-texto"></div>
        <button class="copiar" id="d-copiar">Copiar texto</button>
        <label for="d-comentario" class="aviso">Qué querés cambiar</label>
        <textarea id="d-comentario" placeholder="Ej.: cambiar la foto de portada por una del grupo en Verona"></textarea>
        <div class="acciones">
          <button class="aprobar" id="d-aprobar">✅ Aprobar</button>
          <button id="d-cambios">✏️ Pedir cambio</button>
          <button id="d-descartar">⏸ Descartar</button>
          <button id="d-descargar" hidden>Descargar</button>
        </div>
        <p class="aviso" id="d-aviso" role="status"></p>
      </div>
    </div>
  </div>
</dialog>

<script>
const MES = "__MES__";
const COLOR = {especial:"var(--dorado-profundo)", paquete:"var(--turquesa-profundo)", destino:"var(--salvia)", educativo:"var(--selva)", agencia:"var(--turquesa)"};
const ESTADO = {pendiente:"Pendiente", aprobada:"Aprobada", cambios:"Con cambios", descartada:"Descartada"};
const COLOR_ESTADO = {pendiente:"var(--tinta-suave)", aprobada:"var(--ok)", cambios:"var(--cambios)", descartada:"var(--descartada)"};
const DIAS = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"];
let piezas = [], vista = "cal", abierta = null, db = null, user = null, downloads = null;

const $ = (id) => document.getElementById(id);
const url = (a) => "/_blob/" + a.id;
const portada = (p) => (p.assets || []).find(a => a.tipo === "imagen");
const fechaTxt = (iso) => { const d = new Date(iso + "T12:00:00"); return `${DIAS[(d.getDay()+6)%7]} ${d.getDate()}`; };
const isoLocal = (d) => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;

function resumen() {
  const c = {pendiente:0, aprobada:0, cambios:0, descartada:0};
  piezas.forEach(p => c[p.estado] = (c[p.estado] || 0) + 1);
  const decididas = c.aprobada + c.descartada;
  $("resumen").replaceChildren(...[["Total", piezas.length], ["Aprobadas", c.aprobada], ["Con cambios", c.cambios], ["Pendientes", c.pendiente]]
    .map(([t, n]) => { const s = document.createElement("span"); const b = document.createElement("b"); b.textContent = n; s.append(b, t); return s; }));
  $("avance").style.width = piezas.length ? `${Math.round(decididas / piezas.length * 100)}%` : "0";
}

function miniatura(p) {
  const a = portada(p);
  if (!a) { const d = document.createElement("div"); d.className = "sin"; return d; }
  const i = document.createElement("img"); i.src = url(a); i.alt = ""; i.loading = "lazy"; return i;
}

function chip(p) {
  const b = document.createElement("button"); b.className = "chip"; b.style.setProperty("--c", COLOR[p.pilar] || "var(--selva)");
  const t = document.createElement("span"); t.textContent = `${p.hora} · ${p.formato} · ${p.titulo || p.tema}`;
  const e = document.createElement("div"); e.className = "estado"; e.style.color = COLOR_ESTADO[p.estado];
  e.textContent = ESTADO[p.estado] + (p.version > 1 ? ` · v${p.version}` : "");
  const col = document.createElement("div"); col.style.minWidth = "0"; col.append(t, e);
  b.append(miniatura(p), col); b.onclick = () => abrir(p.id); return b;
}

function calendario() {
  const porSemana = new Map();
  piezas.forEach(p => {
    const d = new Date(p.fecha + "T12:00:00"); const lunes = new Date(d); lunes.setDate(d.getDate() - ((d.getDay()+6)%7));
    const k = isoLocal(lunes);
    if (!porSemana.has(k)) porSemana.set(k, new Map());
    const dias = porSemana.get(k); if (!dias.has(p.fecha)) dias.set(p.fecha, []); dias.get(p.fecha).push(p);
  });
  const cont = document.createDocumentFragment();
  [...porSemana.keys()].sort().forEach(k => {
    const fila = document.createElement("div"); fila.className = "semana";
    for (let i = 0; i < 5; i++) {
      const d = new Date(k + "T12:00:00"); d.setDate(d.getDate() + i); const iso = isoLocal(d);
      const caja = document.createElement("div"); caja.className = "dia";
      const h = document.createElement("h3"); h.textContent = fechaTxt(iso); caja.append(h);
      (porSemana.get(k).get(iso) || []).sort((a,b) => a.hora.localeCompare(b.hora)).forEach(p => caja.append(chip(p)));
      fila.append(caja);
    }
    cont.append(fila);
  });
  return cont;
}

function grilla() {
  const g = document.createElement("div"); g.className = "grilla";
  piezas.filter(p => p.formato !== "historias" && p.estado !== "descartada")
    .sort((a,b) => (b.fecha + b.hora).localeCompare(a.fecha + a.hora))
    .forEach(p => { const b = document.createElement("button"); b.setAttribute("aria-label", p.titulo || p.tema);
      b.append(miniatura(p)); if (p.formato !== "post") { const m = document.createElement("span"); m.className = "marca"; m.textContent = p.formato; b.append(m); }
      b.onclick = () => abrir(p.id); g.append(b); });
  return g;
}

function pintar() {
  resumen();
  if (!piezas.length) return;
  $("vista").replaceChildren(vista === "cal" ? calendario() : grilla());
  if (abierta) llenar(piezas.find(p => p.id === abierta));
}

function llenar(p) {
  if (!p) return;
  $("d-pilar").textContent = `${p.pilar} · ${p.formato}`;
  $("d-titulo").textContent = p.titulo || p.tema;
  $("d-previa").replaceChildren(...(p.assets || []).map(a => {
    if (a.tipo === "video") { const v = document.createElement("video"); v.src = url(a); v.controls = true; v.playsInline = true; v.preload = "metadata"; return v; }
    const i = document.createElement("img"); i.src = url(a); i.alt = a.nombre; return i;
  }));
  const ficha = [["Publica", `${fechaTxt(p.fecha)} · ${p.hora}`], ["Estado", ESTADO[p.estado] + (p.version > 1 ? ` (versión ${p.version})` : "")]];
  if (p.verificacion) ficha.push(["Verificado", `${p.verificacion.fuente}, ${p.verificacion.fecha}`]);
  if (p.comentario) ficha.push(["Tu pedido", p.comentario]);
  $("d-ficha").replaceChildren(...ficha.flatMap(([k, v]) => { const dt = document.createElement("dt"); dt.textContent = k; const dd = document.createElement("dd"); dd.textContent = v; return [dt, dd]; }));
  $("d-texto").textContent = [p.texto, (p.hashtags || []).join(" ")].filter(Boolean).join("\n\n") || "Esta pieza no lleva texto de posteo.";
  $("d-descargar").hidden = !(downloads && p.estado === "aprobada" && (p.assets || []).length);
  ["d-aprobar","d-cambios","d-descartar"].forEach(id => $(id).disabled = !db);
}

function abrir(id) { abierta = id; $("d-comentario").value = ""; $("d-aviso").textContent = ""; llenar(piezas.find(p => p.id === id)); $("detalle").showModal(); }

async function decidir(estado) {
  const comentario = $("d-comentario").value.trim();
  if (estado === "cambios" && !comentario) { $("d-aviso").textContent = "Escribí qué querés cambiar antes de pedir el cambio."; $("d-comentario").focus(); return; }
  try {
    const quien = user ? await user.id() : null;
    await db.doc("piezas/" + abierta).update({ estado, comentario: estado === "cambios" ? comentario : "", decididoPor: quien, decididoEn: new Date().toISOString() });
    $("d-aviso").textContent = estado === "aprobada" ? "Aprobada." : estado === "cambios" ? "Pedido de cambio guardado." : "Descartada.";
  } catch (e) {
    $("d-aviso").textContent = "No se pudo guardar. Probá de nuevo en unos segundos.";
  }
}

async function descargar() {
  const p = piezas.find(x => x.id === abierta);
  for (const a of p.assets) {
    try {
      const blob = await (await fetch(url(a))).blob();
      await downloads.save({ filename: `${p.id}-${a.nombre}`, data: blob });
    } catch (e) {
      if (e && e.code === "declined") break;
      $("d-aviso").textContent = "No se pudo descargar " + a.nombre + ".";
    }
  }
}

async function copiar() {
  try { await navigator.clipboard.writeText($("d-texto").textContent); $("d-aviso").textContent = "Texto copiado."; }
  catch { const r = document.createRange(); r.selectNodeContents($("d-texto")); const s = getSelection(); s.removeAllRanges(); s.addRange(r); $("d-aviso").textContent = "Texto seleccionado: copialo con Ctrl+C."; }
}

$("v-cal").onclick = () => { vista = "cal"; $("v-cal").setAttribute("aria-pressed","true"); $("v-grilla").setAttribute("aria-pressed","false"); pintar(); };
$("v-grilla").onclick = () => { vista = "grilla"; $("v-grilla").setAttribute("aria-pressed","true"); $("v-cal").setAttribute("aria-pressed","false"); pintar(); };
$("cerrar").onclick = () => { abierta = null; $("detalle").close(); };
$("d-aprobar").onclick = () => decidir("aprobada");
$("d-cambios").onclick = () => decidir("cambios");
$("d-descartar").onclick = () => decidir("descartada");
$("d-descargar").onclick = descargar;
$("d-copiar").onclick = copiar;

(async () => {
  [db, user, downloads] = await Promise.all([claude.use("db"), claude.use("user"), claude.use("downloads")]);
  if (!db) { $("vista").innerHTML = '<p class="aviso">No se pudo conectar con la base del tablero en esta vista.</p>'; return; }
  db.collection("piezas").orderBy("fecha").onSnapshot(
    snap => { piezas = snap.docs.map(d => d.data()); pintar(); },
    () => { $("vista").innerHTML = '<p class="aviso">Se cortó la conexión con el tablero. Recargá la página.</p>'; }
  );
})();
</script>
```

- [ ] **Step 5: Run test to verify it passes**

Run: `.venv/Scripts/python -m pytest tests/test_tablero.py -v`
Expected: 4 passed

- [ ] **Step 6: Publicar un tablero de prueba y verificar**

1. `.venv/Scripts/python -c "from veg.tablero import preparar_pagina; from pathlib import Path; Path('meses/_prueba').mkdir(parents=True, exist_ok=True); preparar_pagina(2026, 11, Path('meses/_prueba/tablero.html'))"`
2. Publicar con la herramienta Artifact: `file_path` = `meses/_prueba/tablero.html`, `icon` = "calendar", `capabilities` = `{"db": {}, "downloads": true, "user": {}}` (cargar antes la skill `artifact-capabilities`).
3. Subir 2 PNG de `meses/_muestras/` como assets del tablero (`asset: true`, `file_paths`) y anotar los ids.
4. Con `ArtifactData` `batch`, escribir 2 documentos `set` en la colección `piezas` usando la salida de `escribir_filas`.
5. `ArtifactData` `list` de `piezas`: deben volver 2 documentos con `estado: "pendiente"`.
6. Abrir la página: deben verse las dos miniaturas en el calendario. Aprobar una y pedir cambio en la otra, y volver a hacer `list`: los estados deben ser `aprobada` y `cambios`.

- [ ] **Step 7: Commit**

```bash
git add tablero/index.html veg/tablero.py tests/test_tablero.py
git commit -m "feat: tablero de aprobación con base de datos, descargas y vista de grilla"
```

---

### Task 8: Agentes y orquestación "armá <mes>"

**Files:**
- Create: `CLAUDE.md`, `agentes/investigador.md`, `agentes/estratega.md`, `agentes/copywriter.md`, `agentes/disenador.md`, `agentes/editor-video.md`, `agentes/revisor.md`, `.claude/skills/arma-mes/SKILL.md`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: el comando de trabajo "armá <mes>" y los archivos `meses/AAAA-MM/{salidas.json, calendario.json, material.md, piezas.json, piezas/, finales/, assets.json, filas.json, tablero.html, revision.md}`.

- [ ] **Step 1: Escribir `CLAUDE.md`**

```markdown
# Community Manager VEG

Sistema de contenido de Instagram para Viajar en Grupo (@viajar.en.grupo).

- Manual de marca: https://claude.ai/artifact/PtTQiusa72f1hrbhu3Jy7J. Leé su `project/README.md` antes de escribir o diseñar.
- Especificación: docs/specs/2026-10-15-community-manager-veg-design.md
- Comando de trabajo: "armá <mes>" (skill `arma-mes`). "revisá el tablero" aplica los pedidos de cambio.
- Python: `.venv/Scripts/python`. Tests: `.venv/Scripts/python -m pytest -m "not lento"` (rápidos) y `-m lento` (render y video).
- Nunca publicar en Instagram. Nunca inventar precios, fechas ni cupos: si no están verificados hoy, la pieza no es de venta.
```

- [ ] **Step 2: Escribir los agentes**

`agentes/investigador.md`:
```markdown
# Investigador

Tu tarea: producir `meses/<AAAA-MM>/salidas.json` (lista de `Salida`, ver `veg/modelos.py`) con TODAS las salidas publicadas hoy.

1. Leé https://www.viajarengrupo.tur.ar/ y https://www.viajarengrupo.tur.ar/salidas. Por cada salida tomá: destino, fecha de salida (y regreso si está), duración, precio desde, base, suplemento single, operador y URL.
2. Por cada salida de operador, abrí la web pública del mayorista y confirmá fecha, precio y cupo. Valores de `cupo`: `disponible`, `ultimos` (si dice "últimos lugares" o similar), `agotado`, `sin_verificar` (no se pudo confirmar).
3. `verificado_en` = la fecha de hoy solo si confirmaste el cupo hoy.
4. `especial: true` solo para salidas propias acompañadas por Bettina (hoy: Norte de España 24/05–10/06/2027). Nunca para paquetes de mayorista.
5. Precio "a consultar" → `precio_desde: null`. Nunca estimes un precio.
6. Guardá con `veg.modelos.guardar`. Al final, informá en 5 líneas qué salidas quedaron vendibles y cuáles no se pudieron verificar y por qué.
```

`agentes/estratega.md`:
```markdown
# Estratega

Entrada: `meses/<AAAA-MM>/salidas.json`. Salida: `meses/<AAAA-MM>/calendario.json` y `meses/<AAAA-MM>/material.md`.

1. Generá la base: `armar_calendario(anio, mes, cargar_salidas(...), hoy)` y guardala con `guardar`.
2. Completá `tema` de cada pieza:
   - especial/paquete: el ángulo concreto de la salida (ej. "Bodegas de La Rioja", "Cupos para Mercadillos").
   - destino: un destino que vendemos, sin repetir en el mes.
   - educativo: un tema útil (documentación, seguro, valija, mitos de viajar en grupo, cómo es una charla informativa).
   - agencia: Bettina, la oficina, un testimonio o el recap de un viaje reciente.
   - historias: mantené el tema del día y agregá el detalle (qué encuesta, qué tip).
   - Salidas que parten dentro del mes: usá historias de "¡salimos!" y dejá anotado un recap para el mes siguiente.
3. Escribí `material.md` para Manuel: por pieza, qué fotos o clips hacen falta, en lenguaje simple ("8 a 12 clips del grupo en Verona, de 3 a 10 segundos cada uno"). Al final, la lista de guiones de 3 líneas para las historias de los jueves.
```

`agentes/copywriter.md`:
```markdown
# Copywriter

Entrada: `calendario.json`, `salidas.json`, el README del manual. Salida: `meses/<AAAA-MM>/piezas.json` (mismas piezas con `titulo`, `texto`, `hashtags`).

- Voz de Bettina, voseo, apertura emotiva y después lo concreto (ver "Voz y tono" del manual).
- `titulo`: 5 palabras o menos, va en la imagen.
- `texto`: entre 400 y 1200 caracteres, de 1 a 3 emojis, un solo llamado a la acción (WhatsApp +54 9 11 5944-4920, "link en bio" o "dejanos tu comentario").
- Venta: fechas con `rango_fechas`, precio con `formatear_precio` y la palabra "desde" + la base. Si el precio es null, "Consultanos por cupos y precio".
- `hashtags`: de 5 a 8, `#viajarengrupo` primero, después `#viajesgrupales #agenciadeviajes` y de 2 a 4 del destino.
- Historias: `texto` = una línea por placa (de 3 a 5 líneas), sin hashtags.
- Corré `revisar()` en cada pieza y corregí hasta que devuelva [].
```

`agentes/disenador.md`:
```markdown
# Diseñador

Entrada: `piezas.json`, `material/`. Salida: PNG en `meses/<AAAA-MM>/piezas/<id>/`.

- Post de venta (especial, paquete) → `post_paquete` con `letra_chica` = base + suplemento + `LETRA_CHICA_VENTA`.
- Post de agencia → `lamina` con `oscuro: true`, `etiqueta` "Viajar en Grupo" y el titular.
- Carrusel → `lamina`: portada (`numero` vacío, `oscuro: true`) + de 4 a 7 láminas (`numero` 1..n, `oscuro: false`) + lámina final con CTA.
- Historias → `historia`, una por línea del texto.
- Reel → `portada_reel` y `placa_cierre` (frase según el pilar: "¿Nos acompañás?", "Sumate a la charla", "Reservá tu lugar").
- Fotos: elegí de `material/` la mejor según el orden del manual (grupo real > Bettina > paisaje > detalle). Sin foto propia: stock libre de derechos (anotá la fuente en `piezas/<id>/fuentes.txt`) o fondo liso.
- Mirá cada PNG con Read antes de darlo por terminado: texto dentro de los márgenes, nada tapado.
```

`agentes/editor-video.md`:
```markdown
# Editor de video

Entrada: la pieza `reel` de `piezas.json`, `material/`, la portada y la placa del diseñador. Salida: `meses/<AAAA-MM>/finales/<id>.mp4` y `meses/<AAAA-MM>/piezas/<id>/<id>-preview.mp4`.

1. Elegí de 10 a 25 tomas de `material/` para contar: gancho (lo más fuerte primero), desarrollo y dato concreto. Cada toma dura de 1,5 a 3 s (máximo 6 s si es Bettina hablando).
2. Subtítulos: de 4 a 8 en todo el reel, 2 líneas como máximo, que digan el dato o la emoción ("Ópera en la Arena de Verona", "Desde USD 9.680").
3. `armar_reel(tomas, portada, placa, carpeta=meses/<AAAA-MM>/finales, nombre=<id>)`; mové la preview a `piezas/<id>/`.
4. En `piezas/<id>/musica.txt` sugerí 2 temas de la biblioteca de Instagram por estilo (no se agrega música al MP4).
5. Extraé 3 fotogramas (segundo 2, mitad, final) con ffmpeg y miralos con Read: encuadre correcto y subtítulos legibles.
```

`agentes/revisor.md`:
```markdown
# Revisor

Entrada: todo `meses/<AAAA-MM>/`. Salida: `meses/<AAAA-MM>/revision.md`.

1. Re-verificá hoy, en la web del mayorista, el cupo y el precio de cada salida usada en piezas de venta. Actualizá `salidas.json` (`verificado_en`, `cupo`, `precio_desde`).
2. Corré `revisar(pieza, salida, hoy)` en todas las piezas.
3. Mirá cada PNG y cada preview contra la checklist "Revisión antes de enviar a aprobación" del manual.
4. Las piezas con problemas vuelven al agente que las hizo, con el problema escrito. Repetí hasta que no queden problemas (máximo 2 vueltas; lo que siga mal se lista en `revision.md` como "a decidir por Manuel").
```

- [ ] **Step 3: Escribir la skill `.claude/skills/arma-mes/SKILL.md`**

```markdown
---
name: arma-mes
description: Usar cuando Manuel pida "armá <mes>" o "revisá el tablero" para el contenido de Instagram de Viajar en Grupo.
---

# Armá <mes>

Mes objetivo = el que nombra Manuel (si dice "el próximo", el mes siguiente a hoy). Carpeta: `meses/AAAA-MM/`.

1. **Investigador**: lanzá un subagente con `agentes/investigador.md`. Esperá `salidas.json`.
2. **Estratega**: subagente con `agentes/estratega.md`. Esperá `calendario.json` y `material.md`.
3. **Material**: mostrale a Manuel el contenido de `material.md` y pedile que deje los archivos en `material/` (o que confirme que ya están en Drive). Si falta material para una pieza, se usa el plan B del manual (stock o fotos + texto) y se anota.
4. **Producción**: primero un subagente con `agentes/copywriter.md`; cuando termina, en paralelo, un subagente con `agentes/disenador.md` y uno con `agentes/editor-video.md` por reel (el editor espera la portada y la placa del diseñador).
5. **Revisor**: subagente con `agentes/revisor.md`. Seguí hasta que `revision.md` no tenga problemas abiertos, salvo los marcados "a decidir por Manuel".
6. **Tablero**:
   a. `preparar_pagina(anio, mes, meses/AAAA-MM/tablero.html)` y publicarlo con Artifact (`icon: "calendar"`, `capabilities: {"db": {}, "downloads": true, "user": {}}`).
   b. Subir los PNG y las previews como assets (`asset: true`, `file_paths`, hasta 25 por llamada) y guardar `assets.json` = `{pieza_id: [{id, tipo, nombre}]}`.
   c. `escribir_filas(...)` → `filas.json`; cargarlo con `ArtifactData` `batch` (`set` por documento en `piezas`).
   d. `ArtifactData` `list` de `piezas`: debe haber tantos documentos como piezas.
7. Avisale a Manuel con el link del tablero y 3 líneas: cantidad de piezas, salidas vendidas y lo que quedó "a decidir".

# Revisá el tablero

1. `ArtifactData` `query` en `piezas` con `estado == "cambios"`.
2. Para cada una, aplicá el `comentario` con el agente que corresponda, regenerá los archivos, subí los assets nuevos y hacé `update` con `assets`, `texto`/`titulo` si cambiaron, `version + 1`, `estado: "pendiente"` y `comentario: ""`.
3. Si todo está `aprobada` o `descartada`, avisale a Manuel que puede descargar y programar en Meta Business Suite, y recordale que el MP4 final de cada reel está en `meses/AAAA-MM/finales/`.
```

- [ ] **Step 4: Verificación estática**

Run: `.venv/Scripts/python -m pytest -m "not lento" -v`
Expected: todos los tests rápidos pasan.
Run: `grep -ohE "armar_calendario|cargar_salidas|guardar|revisar|rango_fechas|formatear_precio|LETRA_CHICA_VENTA|armar_reel|preparar_pagina|escribir_filas" agentes/*.md .claude/skills/arma-mes/SKILL.md | sort -u`
y confirmar que cada nombre listado existe en `veg/` (`grep -n "def <nombre>\|<nombre> =" veg/*.py`).

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md agentes .claude/skills/arma-mes
git commit -m "feat: agentes y skill de orquestación arma-mes"
```

---

### Task 9: Prueba de punta a punta (mini-mes)

**Files:**
- Create: `meses/2026-11-prueba/*` (no se versiona)
- Modify: lo que falle en cualquier tarea anterior

- [ ] **Step 1: Correr el flujo reducido**

Ejecutar la skill `arma-mes` para la semana del 2 al 6 de noviembre de 2026 únicamente: 1 reel (mié 4), 2 posts (lun 2 y vie 6) e historias de lunes a viernes, en `meses/2026-11-prueba/`. Para el reel, si todavía no hay material propio, usar 6 clips de stock libre de derechos y anotar la fuente.

- [ ] **Step 2: Verificar archivos**

Run: `.venv/Scripts/python -c "from veg.sonda import info; import glob, os; [print(f, info(f), os.path.getsize(f)//1048576, 'MB') for f in glob.glob('meses/2026-11-prueba/**/*.mp4', recursive=True)]"`
Expected: el final es `(1080, 1920, ≤90)` y la preview `(720, 1280, …)`, con un peso ≤ 18 MB.

- [ ] **Step 3: Ciclo con Manuel**

Publicar el tablero de prueba y pedirle a Manuel que apruebe una pieza y pida un cambio en otra. Correr "revisá el tablero" y confirmar con `ArtifactData` `list` que la pieza cambiada quedó en `version: 2`, `estado: "pendiente"`.

- [ ] **Step 4: Corregir y commitear**

Cualquier falla encontrada se corrige en la tarea dueña del código (con su test) y se commitea:
```bash
git add -A
git commit -m "fix: ajustes de la prueba de punta a punta"
```

- [ ] **Step 5: Mes real**

Con la prueba aprobada por Manuel, correr "armá noviembre" y entregar el tablero de noviembre 2026 a más tardar el 25/10/2026.
