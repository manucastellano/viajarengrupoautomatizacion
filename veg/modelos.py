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
