"""Semanas 2 a 4 de noviembre 2026 (9 al 30): arma las piezas con fotos propias, las revisa y las renderiza.

Uso: .venv/Scripts/python meses/2026-11/generar_semanas2a4.py
Las fotos salen de la selección de Gemini en meses/2026-11/seleccion/<destino>.txt (número → archivo).
"""
import json
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from veg.formato import LETRA_CHICA_VENTA, formatear_precio, rango_fechas  # noqa: E402
from veg.modelos import Pieza, Salida, cargar_piezas, guardar  # noqa: E402
from veg.render import render_png  # noqa: E402
from veg.revisor import revisar  # noqa: E402

HOY = date(2026, 10, 21)
MES = RAIZ / "meses" / "2026-11"
SEL = MES / "seleccion"
STOCK = RAIZ / "material" / "stock"
CARPETAS = {
    "como": "DOLCE-VITA/Como/Fotos en iCloud", "arena": "DOLCE-VITA/vERONA arena/Fotos en iCloud",
    "sirmione": "DOLCE-VITA/Sirmione/Fotos en iCloud", "tartufo": "DOLCE-VITA/Tartuffo/Fotos en iCloud",
    "blanco-it": "DOLCE-VITA/Noche de blanco/Fotos en iCloud", "alhambra": "ESPANA/DÍA 2 - La Alhambra (granada)",
    "sevilla": "ESPANA/DIA 7 - Sevilla", "porto": "ESPANA/Dia 13 - PORTO",
    "blanco-es": "ESPANA/Día 11 - MARBELLA y Noche de blanco/NOCHE BLANCO", "aeropuerto": "ESPANA/Aeropuerto",
}


def foto(destino: str, n: int) -> Path:
    for linea in (SEL / f"{destino}.txt").read_text(encoding="utf-8-sig").splitlines():
        num, nombre = linea.split("\t")
        if int(num) == n:
            return RAIZ / "material" / "propias" / CARPETAS[destino] / nombre
    raise KeyError(f"{destino} #{n}")


NORTE = Salida(id="norte-espana-2027", destino="Norte de España", fecha_salida=date(2027, 5, 24), fecha_regreso=date(2027, 6, 10),
               duracion="18 días / 15 noches", operador="Viajar en Grupo (web propia)",
               url="https://www.viajarengrupo.tur.ar/norte-espana-2027", cupo="disponible", verificado_en=HOY,
               precio_desde=9680, suplemento_single=2290, especial=True)
PRECIO = formatear_precio(NORTE.precio_desde)
HT = ["#viajarengrupo", "#viajesgrupales", "#agenciadeviajes"]
NOTA = "\n\n———\nNota de producción (no copiar en Instagram):\n"
WA = "WhatsApp +54 9 11 4434-0161"

piezas: list[Pieza] = []
renders: dict[str, list[tuple[str, dict]]] = {}


def pieza(p: Pieza, laminas):
    piezas.append(p)
    renders[p.id] = laminas


def carrusel(fecha, pilar, tema, titulo, texto, hashtags, portada, laminas, cierre, salida_id=None):
    sl = [("lamina", {"titulo": titulo, "etiqueta": portada[0], "foto": portada[1]})]
    for i, (t, x, f) in enumerate(laminas, 1):
        sl.append(("lamina", {"numero": i, "titulo": t, "texto": x, "foto": f, "oscuro": False, "posicion": "abajo" if f else None}))
    sl.append(("lamina", {"titulo": cierre[0], "etiqueta": "Escribinos", "texto": cierre[1], "oscuro": True}))
    pieza(Pieza(id=f"{fecha.isoformat()}-carrusel", fecha=fecha, hora="19:00", formato="carrusel", pilar=pilar,
                tema=tema, salida_id=salida_id, titulo=titulo, texto=texto, hashtags=HT + hashtags), sl)


def historia(fecha, tema, plantilla, datos, linea, nota, salida_id=None, titulo=""):
    pieza(Pieza(id=f"{fecha.isoformat()}-historias", fecha=fecha, hora="10:00", formato="historias", pilar="agencia",
                tema=tema, salida_id=salida_id, titulo=titulo or datos.get("titulo", datos.get("frase", datos.get("lugar", ""))),
                texto=linea + NOTA + nota), [(plantilla, datos)])


def reel(fecha, pilar, tema, titulo, ante, foto_portada, texto, guion, hashtags, salida_id=None, cierre="¿Nos acompañás?", posicion=None):
    pieza(Pieza(id=f"{fecha.isoformat()}-reel", fecha=fecha, hora="20:00", formato="reel", pilar=pilar, tema=tema,
                salida_id=salida_id, titulo=titulo, texto=texto + NOTA + guion, hashtags=HT + hashtags),
          [("portada_reel", {"etiqueta": ante, "titulo": titulo, "foto": foto_portada, "posicion": posicion}), ("placa_cierre", {"frase": cierre})])


def post(fecha, pilar, tema, titulo, texto, hashtags, lamina, hora="13:00", salida_id=None, plantilla="lamina"):
    pieza(Pieza(id=f"{fecha.isoformat()}-post", fecha=fecha, hora=hora, formato="post", pilar=pilar, tema=tema,
                salida_id=salida_id, titulo=titulo, texto=texto, hashtags=HT + hashtags), [(plantilla, lamina)])


D = date
# ============================== SEMANA 2 ==============================
carrusel(D(2026, 11, 9), "destino", "Norte de Italia en 5 paradas (La Dolce Vita)", "Norte de Italia: 5 paradas",
         "Lagos, ópera, castillos y trufas 🇮🇹\n\nEstas son cinco paradas que vivimos con el grupo de La Dolce Vita 2026, y que se quedaron en el corazón de todos. Deslizá 👉\n\n"
         "En 2027 repetimos la Dolce Vita. Comentá ITALIA y te avisamos cuando abramos los cupos ✈️",
         ["#italia", "#dolcevita", "#lagodicomo", "#verona"],
         ("La Dolce Vita 2026", foto("como", 14)),
         [("Lago di Como", "Villas, barquitos y pueblos de colores a orillas del lago.", foto("como", 15)),
          ("Verona", "Una noche de ópera en la Arena, un anfiteatro romano.", foto("arena", 8)),
          ("Sirmione", "El castillo que parece flotar sobre el lago di Garda.", foto("sirmione", 6)),
          ("Piemonte", "Salir al bosque con un trifulau a buscar trufas.", foto("tartufo", 15)),
          ("Noche de Blanco", "Una cena toda de blanco para celebrar el viaje en grupo.", foto("blanco-it", 5))],
         ("¿Te sumás en 2027?", "Comentá ITALIA y te avisamos cuando abramos los cupos."))
reel(D(2026, 11, 11), "destino", "La Noche de Blanco (recap)", "La Noche de Blanco", "Así se vive", foto("blanco-es", 9),
     "Hay noches que se planean con tiempo y se recuerdan para siempre 🤍\n\nLa Noche de Blanco es una de las experiencias que más disfrutamos en nuestras salidas: todo el grupo de blanco, una mesa larga y muchos brindis.\n\n"
     "En mayo la vivimos otra vez en el Norte de España, entre viñedos. ¿Nos acompañás? Escribinos por WhatsApp al +54 9 11 4434-0161 ✨",
     "Reel de 25 a 35 s con fotos y videos de las Noches de Blanco (Marbella 2024 y La Dolce Vita 2026): llegada del grupo, mesa, brindis, baile. "
     "Subtítulos: \"Todo el grupo de blanco\", \"Una mesa larga\", \"Muchos brindis\". Elegir los videos de esas carpetas para editarlo.",
     ["#nochedeblanco", "#viajarenamigas", "#españa", "#italia"])
post(D(2026, 11, 13), "destino", "Granada y la Alhambra", "Granada y la Alhambra",
     "Hay lugares que no alcanza con verlos en fotos 🌿\n\nCaminar la Alhambra con el grupo, sin apuro y con guía local, fue uno de los momentos más lindos de nuestro viaje por el sur de España.\n\n"
     "¿Ya la conocés o la tenés pendiente? Dejanos tu comentario 💬",
     ["#granada", "#alhambra", "#andalucia", "#españa"],
     {"titulo": "Granada y la Alhambra", "etiqueta": "Sur de España 2024", "foto": foto("alhambra", 12)})
historia(D(2026, 11, 9), "tip", "historia", {"etiqueta": "Tip de viaje", "titulo": "Una botellita reutilizable", "texto": "En Europa el agua de las fuentes es potable y te ahorrás comprarla.", "foto": foto("aeropuerto", 3)},
         "Tip: una botellita reutilizable.", "Placa 1: el tip. Placa 2: compartir el carrusel de Italia.")
historia(D(2026, 11, 10), "encuesta de destino", "historia", {"titulo": "¿Italia o España?", "alineacion": "centro", "posicion": "abajo", "foto": foto("como", 15)},
         "¿Italia o España?", "Agregar sticker de encuesta: Italia / España.")
historia(D(2026, 11, 11), "reel", "historia", {"etiqueta": "Nuevo reel", "titulo": "La Noche de Blanco", "texto": "Todo el grupo de blanco, una mesa larga y muchos brindis.", "foto": foto("blanco-es", 12), "posicion": "abajo"},
         "Nuevo reel: La Noche de Blanco.", "Placa 1: compartir el reel del día.")
historia(D(2026, 11, 12), "postal", "historia_postal", {"anio": "2024", "lugar": "Sevilla", "esquina": "abajo", "foto": foto("sevilla", 35)},
         "Postal: Sevilla 2024.", "Postal sin más texto. Etiquetar a las viajeras que aparecen si están de acuerdo.", titulo="Sevilla")
historia(D(2026, 11, 13), "frase", "historia_frase", {"frase": "Un viaje se recuerda por la gente con la que lo compartiste."},
         "Frase de marca.", "Subir tal cual.")

# ============================== SEMANA 3 ==============================
carrusel(D(2026, 11, 16), "educativo", "Qué llevar a Europa en mayo", "Qué llevar a Europa",
         "Mayo es uno de los mejores meses para viajar a Europa 🌿\n\nPero las mañanas son frescas y las tardes, templadas. Te dejo lo que nunca falta en mi valija. Deslizá 👉\n\n"
         "Guardalo para tu próximo viaje y escribinos si tenés dudas ✈️",
         ["#tipsdeviaje", "#valija", "#europa"],
         ("Tips de viaje", foto("aeropuerto", 2)),
         [("Ropa en capas", "Remera, sweater liviano y una campera que entre en la mochila.", None),
          ("Calzado ya usado", "Zapatillas cómodas que ya probaste: se camina mucho.", None),
          ("Adaptador de enchufe", "En casi toda Europa se usa el enchufe de dos patas redondas.", None),
          ("Pasaporte en el mail", "Una foto del pasaporte en tu correo, por las dudas.", None),
          ("Una muda en el carry-on", "Si la valija se demora, tenés lo básico para el primer día.", None)],
         ("¿Te quedó alguna duda?", f"{WA} · Guardá este posteo para tu próximo viaje."))
reel(D(2026, 11, 18), "destino", "Un día en Sevilla", "Un día en Sevilla", "Sur de España 2024", foto("sevilla", 34),
     "Sevilla tiene un color especial 🧡\n\nPlazas, naranjos, patios y un atardecer que pide quedarse un rato más. Así vivimos un día en Sevilla con el grupo.\n\n¿Qué ciudad de España tenés pendiente? Dejanos tu comentario 💬",
     "Reel de 20 a 30 s con fotos y videos de DIA 6 y DIA 7 - Sevilla: llegada, Plaza de España, paseo, cena. Subtítulos breves con los lugares.",
     ["#sevilla", "#andalucia", "#españa"])
post(D(2026, 11, 20), "especial", "Norte de España con los 5 sentidos", "Norte de España",
     "Cinco bases de tres noches para recorrer el norte sin apuro 🇪🇸\n\nGalicia, Asturias, Cantabria, País Vasco, Navarra y La Rioja, con cuatro bodegas, dos catas, el tour de pintxos en Bilbao y la Noche de Blanco entre viñedos.\n\n"
     f"📅 Del 24 de mayo al 10 de junio de 2027 · Desde {PRECIO} por persona en base doble. Suplemento single {formatear_precio(NORTE.suplemento_single)}. Cupos limitados.\n\n"
     "Comentá NORTE y te mando el itinerario completo por privado ✈️",
     ["#nortedeespaña", "#sansebastian", "#paisvasco"],
     {"etiqueta": "Especial de agencia · Salida acompañada", "titulo": "Norte de España",
      "subtitulo": f"{rango_fechas(NORTE.fecha_salida, NORTE.fecha_regreso)} · 18 días", "precio": NORTE.precio_desde,
      "letra_chica": f"Por persona en base doble · Suplemento single {formatear_precio(NORTE.suplemento_single)} · {LETRA_CHICA_VENTA}",
      "foto": STOCK / "san-sebastian-playa-aerea.jpg"},
     salida_id=NORTE.id, plantilla="post_paquete")
historia(D(2026, 11, 16), "tip", "historia", {"etiqueta": "Tip de viaje", "titulo": "Capas, capas y capas", "texto": "En mayo, Europa amanece fresca y se pone templada a la tarde.", "foto": foto("aeropuerto", 2)},
         "Tip: ropa en capas.", "Placa 1: el tip. Placa 2: compartir el carrusel del lunes.")
historia(D(2026, 11, 17), "encuesta de destino", "historia", {"titulo": "Si viajaras al Norte de España, ¿qué te gustaría vivir?", "alineacion": "centro", "top": 700, "tam": 90, "foto": STOCK / "gaztelugatxe-escaleras.jpg"},
         "Encuesta: ¿qué te gustaría vivir en el Norte de España?", "Sticker de encuesta: Bodegas / Pintxos / Paisajes / Todo.", titulo="¿Qué te gustaría vivir?")
historia(D(2026, 11, 18), "reel", "historia", {"etiqueta": "Nuevo reel", "titulo": "Un día en Sevilla", "foto": foto("sevilla", 15), "posicion": "abajo"},
         "Nuevo reel: un día en Sevilla.", "Placa 1: compartir el reel del día.")
historia(D(2026, 11, 19), "postal", "historia_postal", {"anio": "2026", "lugar": "Sirmione", "foto": foto("sirmione", 18)},
         "Postal: Sirmione 2026.", "Postal sin más texto.", titulo="Sirmione")
historia(D(2026, 11, 20), "secuencia Norte de España", "historia",
         {"etiqueta": "Nuestra próxima salida grupal", "titulo": "El Norte de España, con los cinco sentidos.",
          "texto": f"Del 24 de mayo al 10 de junio de 2027. Desde {PRECIO}. Cupos limitados.", "foto": STOCK / "gaztelugatxe-escaleras.jpg"},
         f"Norte de España 2027 · Desde {PRECIO} · Cupos limitados.", "Placa 1: esta. Placa 2: compartir el post del día con sticker de enlace a la web.",
         salida_id=NORTE.id, titulo="El Norte de España")

# ============================== SEMANA 4 ==============================
post(D(2026, 11, 23), "agencia", "Así viajamos: la ópera en la Arena de Verona", "Así viajamos",
     "Una noche de ópera bajo las estrellas, en un anfiteatro romano 🎭\n\nAsí vivimos la Arena de Verona con el grupo de La Dolce Vita 2026. Son esos momentos los que hacen que un viaje en grupo sea distinto.\n\n"
     "¿Te gustaría vivirlo? Escribinos y te contamos sobre la Dolce Vita 2027 ✈️",
     ["#verona", "#arenadiverona", "#opera", "#dolcevita"],
     {"titulo": "Así viajamos", "etiqueta": "Arena de Verona · 2026", "foto": foto("arena", 23), "posicion": "abajo"})
reel(D(2026, 11, 25), "agencia", "Bettina responde: ¿cómo es la charla informativa?", "¿Cómo es la charla?", "Bettina responde", foto("como", 34),
     "¿Te interesa un viaje pero tenés mil preguntas? 💬\n\nPara eso hacemos la charla informativa: te contamos el itinerario día por día, qué incluye, cómo se paga y respondemos todas las dudas.\n\n"
     "Escribinos por WhatsApp al +54 9 11 4434-0161 y te avisamos de la próxima ✈️",
     "Guion para Bettina a cámara (30 a 40 s): \"¿Te interesa un viaje pero tenés mil preguntas? Para eso hacemos la charla informativa. "
     "Te cuento el itinerario día por día, qué incluye, cómo se paga, y respondo todas tus dudas. Es gratis y podés venir aunque todavía no estés decidida. "
     "Escribinos y te aviso de la próxima.\" Tomas de apoyo: una charla anterior, el grupo en Porto.",
     ["#bettinaschwartz", "#viajesacompañados"], posicion="abajo")
post(D(2026, 11, 27), "destino", "Porto", "Porto, a orillas del Duero",
     "Porto se recorre despacio 🇵🇹\n\nCalles en subida, azulejos, el río Duero y un vino que lleva el nombre de la ciudad. Fue una de las paradas favoritas del grupo en nuestro viaje de 2024.\n\n"
     "¿La sumarías a tu próximo viaje? Dejanos tu comentario 💬",
     ["#porto", "#portugal", "#duero"],
     {"titulo": "Porto, a orillas del Duero", "etiqueta": "Portugal · 2024", "foto": foto("porto", 13)})
carrusel(D(2026, 11, 30), "educativo", "Viajar sola sin estar sola", "Viajar sola sin estar sola",
         "¿Querés viajar pero no tenés con quién? 💭\n\nNo hace falta esperar a nadie. Así es viajar sola en una salida grupal. Deslizá 👉\n\n"
         "Escribinos por WhatsApp al +54 9 11 4434-0161 y te contamos cuál es la próxima ✈️",
         ["#viajarsola", "#mujeresqueviajan", "#viajesacompañados"],
         ("Viajar en grupo", foto("alhambra", 1)),
         [("Habitación a tu medida", "Single, o te buscamos con quién compartir (sujeto a disponibilidad).", None),
          ("Nunca comés sola", "Las comidas en grupo son parte del viaje.", None),
          ("Alguien te acompaña", "Viajamos con el grupo de principio a fin.", None),
          ("Tiempo para vos", "Hay tiempo libre para recorrer a tu ritmo.", None)],
         ("¿Viajamos juntas?", WA))
historia(D(2026, 11, 23), "tip", "historia", {"etiqueta": "Tip de viaje", "titulo": "Avisale a tu banco", "texto": "Antes de viajar, avisá que vas a usar la tarjeta en el exterior.", "foto": foto("porto", 7), "posicion": "abajo"},
         "Tip: avisale a tu banco.", "Placa 1: el tip.")
historia(D(2026, 11, 24), "encuesta", "historia", {"titulo": "¿Viajaste alguna vez sola?", "alineacion": "centro", "posicion": "abajo", "foto": foto("porto", 13)},
         "Encuesta: ¿viajaste alguna vez sola?", "Sticker de encuesta: Sí / Todavía no.")
historia(D(2026, 11, 25), "reel", "historia", {"etiqueta": "Nuevo reel", "titulo": "¿Cómo es la charla?", "foto": foto("porto", 13)},
         "Nuevo reel: cómo es la charla informativa.", "Placa 1: compartir el reel del día.")
historia(D(2026, 11, 26), "postal", "historia_postal", {"anio": "2026", "lugar": "Piemonte", "foto": foto("tartufo", 42)},
         "Postal: Piemonte 2026.", "Postal sin más texto.", titulo="Piemonte")
historia(D(2026, 11, 27), "frase", "historia_frase", {"frase": "Lo mejor del viaje siempre es con quién."},
         "Frase de marca.", "Subir tal cual.")
historia(D(2026, 11, 30), "tip", "historia", {"etiqueta": "Tip de viaje", "titulo": "Viajar sola, pero acompañada", "texto": "Hoy en el feed: todo lo que tenés que saber.", "foto": foto("alhambra", 12), "posicion": "abajo"},
         "Tip: viajar sola en grupo.", "Placa 1: esta. Placa 2: compartir el carrusel del día.")

LINEA_CONTACTO = "📲 El WhatsApp de Bettina está en el link de nuestro perfil."
for p in piezas:
    if p.formato != "historias":
        cuerpo, sep, resto = p.texto.partition(NOTA)
        p.texto = cuerpo.rstrip() + "\n\n" + LINEA_CONTACTO + (sep + resto if sep else "")
# ============================== revisión y render ==============================
for p in piezas:
    for _, datos in renders[p.id]:
        f = datos.get("foto")
        if f is not None and not Path(f).exists():
            raise SystemExit(f"Falta la foto de {p.id}: {f}")
problemas = {p.id: v for p in piezas if (v := revisar(p, NORTE if p.salida_id else None, HOY))}
if problemas:
    print(json.dumps(problemas, ensure_ascii=False, indent=2))
    raise SystemExit("Hay piezas con problemas: no se renderiza nada.")

existentes = [p for p in cargar_piezas(MES / "piezas.json") if p.fecha < D(2026, 11, 9)]
guardar(MES / "piezas.json", sorted(existentes + piezas, key=lambda p: (p.fecha, p.hora)))
for pid, laminas in renders.items():
    for i, (plantilla, datos) in enumerate(laminas, 1):
        render_png(plantilla, datos, MES / "piezas" / pid / f"{i:02d}-{plantilla}.png")
    print("render", pid, len(laminas), flush=True)
print("listo:", len(piezas), "piezas nuevas")
