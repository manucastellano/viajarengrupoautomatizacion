"""LinkedIn nov–ene: renderiza los 4 carruseles PDF y las 3 placas de reseñas del calendario.

Uso: .venv/Scripts/python meses/linkedin/generar_laminas.py
Deja en meses/linkedin/piezas/<id>/ las láminas PNG (para el tablero) y <id>.pdf (para publicar en LinkedIn).
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from veg.render import render_pdf, render_png  # noqa: E402

PIEZAS = RAIZ / "meses" / "linkedin" / "piezas"
FIRMA_BETTINA = "Bettina Schwartz · Viajar en Grupo · Leg. 19725"
FIRMA_PAGINA = "Viajar en Grupo · viajarengrupo.tur.ar"

# Cada lámina: (título, etiqueta, texto). La primera es la portada y la última el cierre (fondo verde);
# las del medio llevan numeral. Máximo 6 palabras de título y 35 de texto (manual de marca).
CARRUSELES = {
    "2026-11-26-linkedin-bettina": (FIRMA_BETTINA, [
        ("7 preguntas antes de pagar", "Antes de contratar un viaje grupal",
         "No son para desconfiar: son para viajar con tranquilidad."),
        ("¿Cuál es su legajo habilitado?", None,
         "Una agencia habilitada tiene número de legajo y lo comparte sin problema. El nuestro es el 19725."),
        ("¿Quién acompaña el grupo?", None,
         "Preguntá si viaja un coordinador con el grupo y quién responde si surge algo durante el viaje."),
        ("¿Y si no se llega al mínimo?", None,
         "Muchas salidas necesitan un mínimo de pasajeros. Preguntá qué pasa si no se completa antes de pagar."),
        ("¿Qué asistencia al viajero corresponde?", None,
         "Confirmá qué cobertura incluye, si tiene límite de edad y cómo contempla las preexistencias."),
        ("¿Qué incluye realmente el precio?", None,
         "Aéreos, impuestos, traslados, comidas, excursiones. Pedí el detalle por escrito y fijate qué queda aparte."),
        ("¿Cómo y cuándo se paga?", None,
         "Moneda, plazos, cuotas y condiciones de cancelación. Que todo quede claro antes de transferir."),
        ("¿Con quién voy a viajar?", None,
         "Cuántos pasajeros son y cómo es el grupo. Saberlo te ayuda a imaginar el viaje y a elegir mejor."),
        ("Una buena agencia te responde", None,
         "Con claridad, sin incomodarse y sin apurarte. Guardá este carrusel para tu próxima decisión de viaje."),
    ]),
    "2026-12-02-linkedin-pagina": (FIRMA_PAGINA, [
        ("Viajar en grupo puede ser simple", "Cómo trabajamos",
         "La clave es saber con quién organizás cada paso."),
        ("Consultás", "Paso 1",
         "Nos contás qué viaje te interesa, si viajás sola o acompañada y qué necesitás tener claro antes de decidir."),
        ("Armamos tu viaje", "Paso 2",
         "Te compartimos opciones, condiciones, qué incluye cada salida y qué conviene revisar antes de reservar."),
        ("Viajás tranquila", "Paso 3",
         "Con documentación, asistencia y seguimiento, para que no tengas que resolver todo sola."),
        ("Próximas salidas grupales", None,
         "Mirá el catálogo actualizado en viajarengrupo.tur.ar"),
    ]),
    "2026-12-10-linkedin-bettina": (FIRMA_BETTINA, [
        ("Tu seguro, más allá del precio", "Antes de contratar",
         "Lo que conviene leer antes de viajar, no cuando ya apareció un problema."),
        ("Revisá el límite de edad", None,
         "No todas las coberturas funcionan igual para todas las edades. Confirmalo antes de contratar."),
        ("Consultá por preexistencias", None,
         "Si tenés una condición médica previa, revisá cómo la contempla la cobertura y qué documentación puede pedir la asistencia."),
        ("Cobertura según el destino", None,
         "No es lo mismo viajar cerca que un viaje largo, con traslados, climas o actividades distintas."),
        ("Entendé cómo se usa", None,
         "A qué número llamar, qué pasos seguir y qué gastos necesitan autorización previa."),
        ("No guardes el voucher sin leerlo", None,
         "Si querés revisarlo antes de decidir, escribime por WhatsApp al +54\u00a09\u00a011\u00a04434\u20110161."),
    ]),
    "2027-01-07-linkedin-bettina": (FIRMA_BETTINA, [
        ("5 mitos de viajar en grupo", "Más de 30 años de oficio",
         "Dudas muy razonables, y mi mirada sobre cada una."),
        ("Todo el día arriba del micro", "Mito 1",
         "Un buen circuito alterna traslados con pausas. Por eso prefiero más noches por ciudad: menos valija y más tiempo para disfrutar."),
        ("No tenés tiempo libre", "Mito 2",
         "Una salida bien pensada combina actividades en grupo con tiempo propio. Antes de reservar, mirá en el itinerario cuánto tenés."),
        ("Es para gente mayor", "Mito 3",
         "Viajan personas de distintas edades con algo en común: ganas de conocer el mundo con compañía. Importa más el ritmo del viaje."),
        ("No vas a congeniar con nadie", "Mito 4",
         "Los grupos chicos y una coordinación atenta ayudan a que cada pasajero se sienta parte, a su ritmo."),
        ("Es más caro", "Mito 5",
         "Compará lo que incluye cada propuesta: traslados, asistencia, coordinación. Lo que parece barato a veces suma gastos que no estaban a la vista."),
        ("Viajar en grupo, a tu manera", None,
         "Guardá este carrusel para cuando estés evaluando tu próximo viaje."),
    ]),
}

# Citas textuales de reseñas de Google, copiadas tal cual del texto de cada post (no se corrigen).
RESENAS = {
    "2026-11-25-linkedin-pagina": ("Cada viaje que contratamos superan ampliamente nuestras expectativas.", "Victoria F."),
    "2026-12-16-linkedin-pagina": ("Lindisimo viaje por España.", "Susan F."),
    "2027-01-20-linkedin-pagina": ("Desde hace casi 30 años que viajo con Bettina y siempre fue excelente en todo...", "Alicia V."),
}


def laminas(firma: str, filas: list[tuple]) -> list[dict]:
    total = len(filas)
    datos = []
    for i, (titulo, etiqueta, texto) in enumerate(filas):
        extremo = i in (0, total - 1)
        # "Paso 1" o "Mito 1" ya numeran la lámina; las demás del medio llevan numeral turquesa.
        numero = None if extremo or etiqueta else str(i)
        datos.append({"titulo": titulo, "etiqueta": etiqueta, "texto": texto, "firma": firma,
                      "oscuro": extremo, "numero": numero, "pagina": f"{i + 1} / {total}"})
    return datos


def main() -> None:
    for pieza_id, (firma, filas) in CARRUSELES.items():
        pngs = [render_png("lamina_linkedin", d, PIEZAS / pieza_id / f"{n:02d}.png")
                for n, d in enumerate(laminas(firma, filas), start=1)]
        print(render_pdf(pngs, PIEZAS / pieza_id / f"{pieza_id}.pdf"))
    for pieza_id, (cita, autor) in RESENAS.items():
        datos = {"cita": cita, "autor": autor, "fuente": "reseña en Google", "firma": FIRMA_PAGINA,
                 "tam": 92 if len(cita) < 80 else 80}
        print(render_png("placa_resena", datos, PIEZAS / pieza_id / "01.png"))


if __name__ == "__main__":
    main()
