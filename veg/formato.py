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
