"""Programas del canal (manual de marca, sección Programas): nombre visible y color propio."""

PROGRAMAS = {
    "espana": {"nombre": "Norte de España", "color": "#a63d2a"},        # rojo teja
    "beatles": {"nombre": "The Beatle Experience", "color": "#1c1c1a"},  # negro
    "salidas": {"nombre": "La salida de la semana", "color": "#5e3f6e"},  # ciruela
    "destinos": {"nombre": "Destinos", "color": "#396c59"},              # verde de marca
}


def color(programa: str | None) -> str | None:
    if programa is None:
        return None
    if programa not in PROGRAMAS:
        raise ValueError(f"programa inválido: {programa}")
    return PROGRAMAS[programa]["color"]
