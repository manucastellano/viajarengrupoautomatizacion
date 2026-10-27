"""Semana 1 de noviembre 2026: arma las piezas, las revisa y las renderiza.

Uso: .venv/Scripts/python meses/2026-11/generar_semana1.py
"""
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from veg.formato import LETRA_CHICA_VENTA, formatear_precio, rango_fechas  # noqa: E402
from veg.modelos import Pieza, Salida, guardar  # noqa: E402
from veg.render import render_png  # noqa: E402
from veg.revisor import revisar  # noqa: E402

HOY = date(2026, 10, 20)
MES = RAIZ / "meses" / "2026-11"
PIEZAS = MES / "piezas"
WA = "WhatsApp +54 9 11 4434-0161"

NORTE = Salida(
    id="norte-espana-2027", destino="Norte de España", fecha_salida=date(2027, 5, 24), fecha_regreso=date(2027, 6, 10),
    duracion="18 días / 15 noches", operador="Viajar en Grupo (web propia)",
    url="https://www.viajarengrupo.tur.ar/norte-espana-2027", cupo="disponible", verificado_en=HOY,
    precio_desde=9680, suplemento_single=2290, especial=True,
)
guardar(MES / "salidas.json", [NORTE])
FECHAS_NORTE = rango_fechas(NORTE.fecha_salida, NORTE.fecha_regreso)
PRECIO_NORTE = formatear_precio(NORTE.precio_desde)

HT_BASE = ["#viajarengrupo", "#viajesgrupales", "#agenciadeviajes"]
STOCK = RAIZ / "material" / "stock"  # fotos libres de Pexels; fuentes en material/stock/fuentes.txt
PROPIAS = RAIZ / "material" / "propias" / "MIX"  # viaje grupal al sur de Francia, septiembre 2025
NOTA = "\n\n———\nNota de producción (no copiar en Instagram):\n"

piezas: list[Pieza] = []
renders: dict[str, list[tuple[str, dict, str]]] = {}


def pieza(p: Pieza, laminas: list[tuple[str, dict]]):
    piezas.append(p)
    renders[p.id] = [(plantilla, datos, f"{i:02d}-{plantilla}.png") for i, (plantilla, datos) in enumerate(laminas, 1)]


# --- Lunes 2: carrusel educativo -------------------------------------------------------------
MITOS = [
    ("\"Voy a estar con gente que no conozco\"", "La mayoría llega sin conocer a nadie. Desde el primer día viajás acompañada y el grupo se arma solo, entre cenas y recorridos."),
    ("\"No voy a tener tiempo libre\"", "Armamos más noches por ciudad y dejamos tiempo libre para que recorras a tu ritmo."),
    ("\"Los hoteles quedan lejos de todo\"", "Elegimos hoteles bien ubicados, para que salgas caminando a conocer la ciudad."),
    ("\"Si viajo sola pago el doble\"", "Podés pagar el suplemento single o, si preferís, te buscamos con quién compartir habitación (sujeto a disponibilidad)."),
    ("\"Es un tour apurado en bus\"", "Viajamos en grupos chicos, con bases de varias noches y experiencias como catas, clases de cocina y cenas locales."),
]
pieza(
    Pieza(id="2026-11-02-carrusel", fecha=date(2026, 11, 2), hora="19:00", formato="carrusel", pilar="educativo",
          tema="5 mitos del viaje grupal", titulo="5 mitos del viaje grupal",
          texto=("¿Te dan ganas de viajar pero te frena ir con un grupo? 💭\n\n"
                 "Después de más de 30 años acompañando viajeros, estos son los cinco miedos que más escucho, y lo que pasa de verdad en el viaje. Deslizá 👉\n\n"
                 "¿Tenés otra duda? Dejanos tu comentario y te contamos.\n\n"
                 "Guardá este posteo para tu próximo viaje ✈️"),
          hashtags=HT_BASE + ["#viajarsola", "#tipsdeviaje", "#viajesacompañados"]),
    [("lamina", {"titulo": "5 mitos del viaje grupal", "etiqueta": "Tips de viaje", "oscuro": True, "foto": PROPIAS / "10-1szybzRnCItUPFb7Q7-_dhUD1VPPCqWJc.jpg"})]
    + [("lamina", {"numero": i, "titulo": t, "texto": x, "oscuro": False}) for i, (t, x) in enumerate(MITOS, 1)]
    + [("lamina", {"titulo": "¿Tenés otra duda?", "etiqueta": "Escribinos", "texto": f"{WA} · Guardá este posteo para tu próximo viaje.", "oscuro": True})],
)

# --- Martes 3: presentación de Bettina, para fijar -------------------------------------------
pieza(
    Pieza(id="2026-11-03-post", fecha=date(2026, 11, 3), hora="13:00", formato="carrusel", pilar="agencia",
          tema="Presentación de Bettina (para fijar arriba del perfil)", titulo="Hola, soy Bettina",
          texto=("Si llegaste hace poco a la cuenta, te cuento quién está detrás de cada viaje 🌍\n\n"
                 "Soy Bettina Schwartz, Licenciada en Turismo. Hace más de 30 años que armo viajes, y en 2009, con un viaje a Grecia, empezó Viajar en Grupo.\n\n"
                 "Diseño cada itinerario y acompaño a los grupos: más noches por ciudad, hoteles bien ubicados y tiempo para disfrutar.\n\n"
                 "¿Querés saber cuál es la próxima salida? Escribinos por WhatsApp al +54 9 11 4434-0161 ✈️"
                 + NOTA + "Después de publicarlo, fijalo arriba del perfil (los tres puntitos → Fijar en tu perfil)."),
          hashtags=HT_BASE + ["#bettinaschwartz", "#viajesacompañados"]),
    [("lamina", {"titulo": "Hola, soy Bettina", "etiqueta": "Viajar en Grupo", "oscuro": True}),
     ("lamina", {"numero": 1, "titulo": "30 años armando viajes", "texto": "Soy Licenciada en Turismo. En 2009, con un viaje a Grecia, empezó Viajar en Grupo.", "oscuro": False}),
     ("lamina", {"numero": 2, "titulo": "Viajo con el grupo", "texto": "Diseño cada itinerario y acompaño la salida, de principio a fin.", "oscuro": False}),
     ("lamina", {"numero": 3, "titulo": "Viajes sin apuro", "texto": "Más noches por ciudad, hoteles bien ubicados y tiempo libre para disfrutar.", "oscuro": False}),
     ("lamina", {"titulo": "¿Viajamos juntas?", "etiqueta": "Escribinos", "texto": WA, "oscuro": True})],
)

# --- Miércoles 4: reel de Bettina a cámara ---------------------------------------------------
GUION = ("Guion para grabar con Bettina a cámara (vertical, 35 a 45 s, luz natural, celular a la altura de los ojos):\n"
         "0–3 s: \"¿Te dan ganas de viajar pero no tenés con quién?\"\n"
         "3–15 s: \"Es lo que más me preguntan. Y te cuento algo: la mayoría de las personas que viajan conmigo llegan sin conocer a nadie.\"\n"
         "15–28 s: \"Yo viajo con el grupo, de principio a fin. Compartimos cenas, recorridos, y al tercer día ya son amigas.\"\n"
         "28–38 s: \"En mayo nos vamos al Norte de España, con los cinco sentidos. Si querés el itinerario, comentá NORTE.\"\n"
         "Tomas de apoyo (material propio): grupo brindando, grupo caminando en Italia, Bettina con viajeras.\n"
         "Con subtítulos y la placa de cierre \"¿Nos acompañás?\". En cuanto llegue el video, lo edito.")
pieza(
    Pieza(id="2026-11-04-reel", fecha=date(2026, 11, 4), hora="20:00", formato="reel", pilar="especial",
          tema="Bettina responde: ¿y si viajo sola?", salida_id=NORTE.id, titulo="¿Y si viajo sola?",
          texto=("¿Te dan ganas de viajar pero no tenés con quién? 💭\n\n"
                 "Es lo que más me preguntan. La mayoría de quienes viajan conmigo llegan sin conocer a nadie, y vuelven con amigas.\n\n"
                 f"La próxima: Norte de España con los 5 sentidos, del 24 de mayo al 10 de junio de 2027, desde {PRECIO_NORTE} por persona en base doble 🇪🇸\n\n"
                 "Comentá NORTE y te mando el itinerario por privado ✈️" + NOTA + GUION),
          hashtags=HT_BASE + ["#viajarsola", "#nortedeespaña", "#españa"]),
    [("portada_reel", {"etiqueta": "Bettina responde", "titulo": "¿Y si viajo sola?", "subtitulo": "Lo que más me preguntan"}),
     ("placa_cierre", {"frase": "¿Nos acompañás?"})],
)

# --- Viernes 6: post de venta del especial ---------------------------------------------------
pieza(
    Pieza(id="2026-11-06-post", fecha=date(2026, 11, 6), hora="13:00", formato="post", pilar="especial",
          tema="Norte de España con los 5 sentidos", salida_id=NORTE.id, titulo="Norte de España",
          texto=("Hay viajes que se viven con los cinco sentidos 🌿\n\n"
                 "Galicia, Asturias, Cantabria, País Vasco, Navarra y La Rioja, con cinco bases de tres noches para recorrer sin apuro.\n\n"
                 "🍷 Cuatro bodegas y dos catas con degustación\n"
                 "🍽️ Ocho comidas con bebidas, un tour de pintxos en Bilbao y la Noche de Blanco en Navarrete\n"
                 "👩🏻 Acompañamiento de Bettina y Eugenia, con guía acompañante y guías locales\n\n"
                 "📅 Del 24 de mayo al 10 de junio de 2027 · 18 días\n"
                 f"Desde {PRECIO_NORTE} por persona en base doble. Suplemento single {formatear_precio(NORTE.suplemento_single)}. Cupos limitados.\n\n"
                 "Comentá NORTE y te mando el itinerario completo por privado ✈️"
                 + NOTA + "La imagen tiene fondo liso: cuando tenga una foto propia del norte de España (o del grupo), la reemplazo."),
          hashtags=HT_BASE + ["#nortedeespaña", "#españa", "#larioja", "#paisvasco"]),
    [("post_paquete", {"etiqueta": "Especial de agencia · Salida acompañada", "titulo": "Norte de España",
                       "subtitulo": f"{FECHAS_NORTE} · 18 días", "precio": NORTE.precio_desde,
                       "letra_chica": f"Por persona en base doble · Suplemento single {formatear_precio(NORTE.suplemento_single)} · {LETRA_CHICA_VENTA}",
                       "foto": STOCK / "gaztelugatxe-escaleras.jpg"})],
)

# --- Historias de lunes a viernes ------------------------------------------------------------
HISTORIAS = [
    (date(2026, 11, 2), "tip", None, "Tip de viaje", "Una muda en el carry-on",
     "Si la valija se demora, tenés lo básico para el primer día.", "Guardalo para tu próximo viaje",
     "Placa 1: el tip. Placa 2: compartir el carrusel de los 5 mitos."),
    (date(2026, 11, 3), "encuesta de destino", None, "Encuesta", "¿Qué te frena para viajar?",
     "Respondé en la encuesta de abajo.", "Votá acá abajo",
     "Agregar el sticker de encuesta: No conocer a nadie / El idioma / El precio / Nada, ¡vamos!"),
    (date(2026, 11, 4), "reel y cupos", NORTE.id, "Nuevo reel", "¿Y si viajo sola?",
     f"Norte de España 2027 · Desde {PRECIO_NORTE} · Cupos limitados", "Mirá el reel",
     "Placa 1: compartir el reel del día. Placa 2: esta placa con sticker de enlace a la web."),
    (date(2026, 11, 5), "Bettina / detrás de escena", None, "Detrás de escena", "Un día en la oficina",
     "Así armamos cada itinerario.", "Escribinos",
     "Guion para Bettina (15 s, celular): \"Hola, les muestro dónde nace cada viaje. Hoy estoy terminando el itinerario del Norte de España. ¿Qué destino les gustaría para 2028? Contestame acá.\" + sticker de pregunta."),
    (date(2026, 11, 6), "próximas salidas", NORTE.id, "Próxima salida", "Norte de España",
     f"24/05 al 10/06/2027 · Desde {PRECIO_NORTE} · Cupos limitados", "Comentá NORTE",
     "Placa 1: esta placa. Placa 2: compartir el post del día. Sticker de enlace a la web."),
]
FOTO_HISTORIA = {2: STOCK / "maleta-terminal.jpg", 3: PROPIAS / "11-120tP8gZm3n8rJzEyW525aQy6ZFcGcGPf.jpg",
                 4: STOCK / "san-sebastian-playa-aerea.jpg", 5: None,
                 6: STOCK / "gaztelugatxe-escaleras.jpg"}  # el jueves va la foto propia de Bettina en la oficina
for fecha, tema, salida_id, etiqueta, titulo, linea, cta, nota in HISTORIAS:
    foto = FOTO_HISTORIA[fecha.day]
    pieza(
        Pieza(id=f"{fecha.isoformat()}-historias", fecha=fecha, hora="10:00", formato="historias", pilar="agencia",
              tema=tema, salida_id=salida_id, titulo=titulo, texto=linea + NOTA + nota),
        [("historia", {"etiqueta": etiqueta, "titulo": titulo, "texto": linea, "cta": cta,
                       "foto": foto, "top": 290 if fecha.day == 3 else 590})],  # el martes, arriba para no tapar caras
    )

LINEA_CONTACTO = "📲 El WhatsApp de Bettina está en el link de nuestro perfil."
for p in piezas:
    if p.formato != "historias":
        cuerpo, sep, resto = p.texto.partition(NOTA)
        p.texto = cuerpo.rstrip() + "\n\n" + LINEA_CONTACTO + (sep + resto if sep else "")
# --- Revisión y render -----------------------------------------------------------------------
salidas = {NORTE.id: NORTE}
problemas = {p.id: revisar(p, salidas.get(p.salida_id), HOY) for p in piezas}
problemas = {k: v for k, v in problemas.items() if v}
if problemas:
    print(json.dumps(problemas, ensure_ascii=False, indent=2))
    raise SystemExit("Hay piezas con problemas: no se renderiza nada.")

guardar(MES / "piezas.json", sorted(piezas, key=lambda p: (p.fecha, p.hora)))
for pid, laminas in renders.items():
    for plantilla, datos, nombre in laminas:
        render_png(plantilla, datos, PIEZAS / pid / nombre)
    print("render", pid, len(laminas))
print("listo:", len(piezas), "piezas")
