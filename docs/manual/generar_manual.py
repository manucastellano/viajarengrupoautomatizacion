"""Genera los archivos del manual de marca (artifact Design System) con el estilo real de la cuenta.

Uso: .venv/Scripts/python docs/manual/generar_manual.py  → escribe docs/manual/project/...
"""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
P = AQUI / "project"
RAIZ = AQUI.parents[1]
FOTO1 = "/_blob/5e50bf0c0b29515002037e3bd7889d65"  # Gaztelugatxe (Pexels)
FOTO2 = "/_blob/fe9c118f5a4d1ce9a9ce517ffeae0862"  # San Sebastián (Pexels)


def w(rel, texto):
    ruta = P / rel
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- tokens
tokens = {
    "name": "Viajar en Grupo",
    "version": 2,
    "meta": {"source": "Paleta y tipografías indicadas por la agencia (20/10/2026) + 16 historias publicadas tomadas como referencia"},
    "color": {
        "themes": [{"id": "marca", "name": "Marca"}],
        "tokens": [
            {"name": "verde", "value": "#396c59", "usage": "Verde de marca. Texto de las frases sobre salvia y de las láminas sobre marfil; fondo de láminas oscuras con texto marfil. El avión y la línea punteada van en verde."},
            {"name": "salvia", "value": "#c8ceb5", "usage": "Fondo de las piezas sin foto (frases, placa de cierre). Texto encima siempre en verde."},
            {"name": "turquesa", "value": "#39b5b9", "usage": "Acento: numerales de carruseles y una palabra destacada dentro de un título. Solo en tamaños grandes (60 px o más): sobre marfil no alcanza contraste para texto chico."},
            {"name": "marfil", "value": "#fffff0", "usage": "Fondo claro de láminas de carrusel, con texto verde. Texto sobre fondo verde."},
            {"name": "blanco", "value": "#ffffff", "usage": "Todo texto que va sobre foto, siempre con el velo oscuro debajo."},
            {"name": "negro", "value": "#000000", "usage": "Velos sobre foto (35 a 75 % de opacidad) y fondo de piezas de curiosidades (como la de Halloween)."},
        ],
    },
    "type": {
        "fonts": [{"family": "Genica One", "file": "fonts/GenicaOne-Regular.otf", "weight": "400"}],
        "families": {
            "display": "\"Genica One\", Georgia, serif",
            "texto": "\"Raleway\", \"Helvetica Neue\", Arial, sans-serif",
        },
        "groups": [
            {"name": "Títulos (Genica One, en minúscula de oración)", "family": "display", "styles": [
                {"name": "titulo-historia", "fontSize": "100px", "lineHeight": "1.14", "fontWeight": 400, "usage": "Título de historia sobre foto (lienzo 1080 × 1920)."},
                {"name": "titulo-portada", "fontSize": "112px", "lineHeight": "1.14", "fontWeight": 400, "usage": "Portada de reel, centrado."},
                {"name": "titulo-post", "fontSize": "100px", "lineHeight": "1.14", "fontWeight": 400, "usage": "Post 4:5 de salida, sobre foto."},
                {"name": "titulo-lamina", "fontSize": "98px", "lineHeight": "1.14", "fontWeight": 400, "usage": "Lámina de carrusel; la portada del carrusel va en 118 px."},
                {"name": "frase", "fontSize": "134px", "lineHeight": "1.2", "fontWeight": 400, "usage": "Frase de marca en verde sobre salvia, alineada a la derecha."},
                {"name": "postal-lugar", "fontSize": "62px", "lineHeight": "1.14", "fontWeight": 400, "usage": "Destino de la postal (\"Sur de Francia\"), chico, en una esquina."},
            ]},
            {"name": "Textos (Raleway liviana)", "family": "texto", "styles": [
                {"name": "antetitulo", "fontSize": "58px", "lineHeight": "1.4", "fontWeight": 300, "usage": "Línea antes del título (\"Nuestra próxima salida grupal\")."},
                {"name": "cuerpo-historia", "fontSize": "58px", "lineHeight": "1.4", "fontWeight": 300, "usage": "Texto de historia. Los datos clave (fechas límite, \"incluida\", \"Cupos limitados\") van en negrita 700."},
                {"name": "cuerpo-post", "fontSize": "54px", "lineHeight": "1.4", "fontWeight": 300, "usage": "Texto de lámina de carrusel y de post."},
                {"name": "postal-anio", "fontSize": "52px", "lineHeight": "1.4", "fontWeight": 300, "usage": "Año de la postal (\"2025\")."},
                {"name": "subtitulo-video", "fontSize": "54px", "lineHeight": "1.3", "fontWeight": 600, "usage": "Subtítulos quemados en reels, blancos con sombra suave, 2 líneas como máximo."},
                {"name": "letra-chica", "fontSize": "24px", "lineHeight": "1.3", "fontWeight": 400, "usage": "Base del precio, suplemento y \"Leg. 19725 · Precios sujetos a disponibilidad y cambio\"."},
            ]},
        ],
    },
    "spacing": {"tokens": [
        {"name": "margen-historia", "value": "120px", "usage": "Margen lateral del bloque de texto en historias alineadas a la izquierda (90 px si va centrado)."},
        {"name": "margen-post", "value": "100px", "usage": "Margen lateral en posts y láminas 4:5."},
        {"name": "separacion-bloque", "value": "30px", "usage": "Espacio entre antetítulo, título y texto."},
        {"name": "zona-segura-arriba", "value": "250px", "usage": "Historias y reels: nada importante en los 250 px superiores."},
        {"name": "zona-segura-abajo", "value": "330px", "usage": "Historias: nada importante en los 330 px inferiores (400 px en reels)."},
    ]},
    "radius": {"tokens": [
        {"name": "radius-0", "value": "0px", "usage": "Fotos y fondos: siempre a sangre, sin bordes ni marcos."},
        {"name": "radius-logo", "value": "50%", "usage": "Solo el logo circular."},
    ]},
}
w("tokens.json", json.dumps(tokens, ensure_ascii=False, indent=2) + "\n")

# ---------------------------------------------------------------- fuente
(P / "fonts").mkdir(parents=True, exist_ok=True)
shutil.copy(RAIZ / "plantillas" / "fuentes" / "GenicaOne-Regular.otf", P / "fonts" / "GenicaOne-Regular.otf")

# ---------------------------------------------------------------- README (brand book)
README = """Viajar en Grupo es la agencia de Bettina Schwartz, Lic. en Turismo con 30 años de experiencia (Leg. 19725, Av. Congreso 2157, CABA). Arma salidas grupales acompañadas para gente que quiere conocer el mundo sin viajar sola: grupos chicos, más noches por ciudad, hoteles bien ubicados y una persona real detrás de cada itinerario. Todo lo que se publica tiene que transmitir eso: **confianza, compañía y experiencias reales**.

## Voz y tono

- Escribí en la voz de la cara del programa (ver **Programas**): primera persona, cálida y cercana. Sin cara (Destinos) o en lo institucional, usá el plural de la agencia ("Te invitamos a viajar con nosotras"); en recaps y relatos, la primera persona singular de quien viajó ("Me vuelvo con el corazón lleno…").
- Usá voseo rioplatense: "¿Te sumás?", "¿Nos acompañás?", "Escribinos".
- Abrí con una pregunta o una frase emotiva y después bajá a lo concreto. Ejemplos reales de la cuenta: *"Si te dijéramos que en mayo viajás a España en grupo… ¿te sumás?"*, *"Los mejores paisajes se miran en compañía"*, *"Viajar es lo único que comprás y te hace más rico."*
- En las imágenes, el texto va en minúscula de oración, nunca todo en mayúsculas. Las preguntas y exclamaciones llevan los dos signos (¿?, ¡!).
- Usá entre 1 y 3 emojis por texto de posteo, como puntuación. No pongas emojis dentro de las imágenes.
- Prohibido: urgencia falsa, superlativos vacíos, mayúsculas sostenidas y anglicismos innecesarios.
- Siempre hay un solo llamado a la acción: "Escribinos por WhatsApp al +54 9 11 4434-0161", "Comentá NORTE y te mando el itinerario" o "Link en bio".
- Todo posteo y reel termina con la línea: "📲 El WhatsApp de Bettina está en el link de nuestro perfil." El número es +54 9 11 4434-0161.
- Hashtags: de 5 a 8, al final, con `#viajarengrupo` primero.

## Datos que no pueden fallar

- Los precios van siempre con "Desde" y su base: "Desde **USD 9.680** por persona en base doble", más el suplemento single si existe.
- Las fechas, el cupo y la disponibilidad se verifican el mismo día en viajarengrupo.tur.ar y en la web del mayorista (Dopazo & Ravenna, Eurovips, King Midas, Europa BA, Tower Travel). Si no hay cupo verificado, no se publica.
- Toda pieza de venta lleva en `letra-chica`: "Leg. 19725 · Precios sujetos a disponibilidad y cambio".
- "Especial de agencia" es solo para las salidas propias acompañadas. Hoy son dos: **Norte de España con los 5 sentidos** (24 de mayo al 10 de junio de 2027, con Bettina) y **The Beatle Experience: de Londres a Liverpool** (25 de agosto al 4 de septiembre de 2027, con Alejandra Peñalva y Mirna Cappiello). Nunca para paquetes de mayorista.

## Programas

La cuenta funciona como un canal con programas. Viajar en Grupo es el canal: pone la marca, el legajo, los colores y la calidad. Cada programa tiene su cara, su voz y sus formatos, pero todos se ven de la misma casa:
- Misma piel visual: tipografía, colores y recetas de este manual. Lo único propio de cada programa es su etiqueta (`antetitulo`) con el nombre del programa.
- Mismo cierre: un solo llamado a la acción hacia el WhatsApp de la agencia, y "Leg. 19725" en toda pieza de venta.
- Bettina es la directora del canal: conduce su programa y aparece de vez en cuando en los otros para presentar a sus caras.
- Cada programa tiene su historia destacada en el perfil.

| Programa | Cara y voz | Qué es | Formatos | Pilar |
| --- | --- | --- | --- | --- |
| Norte de España con los 5 sentidos | Bettina, primera persona | Salida propia, 24/05–10/06/2027 | Reels a cámara, serie de un sentido por semana, cuenta regresiva, recaps durante el viaje | especial |
| The Beatle Experience | Alejandra Peñalva y Mirna Cappiello, comunicadoras que acompañan el viaje | Salida propia, Londres y Liverpool, 25/08–04/09/2027, a 70 años del primer encuentro de John y Paul | Reels de las dos a cámara, sección "Una canción, un lugar", historias | especial |
| La salida de la semana | Juana, agente de viajes de Viajar en Grupo, primera persona | Paquetes de mayoristas (King Midas, Eurovips, etc.) con cupo verificado | Reel de Juana de 45 a 60 s + post de salida + historia de cupos | paquete |
| Destinos | Sin cara: plural de la agencia | Curiosidades, qué ver y postales de los destinos que vendemos | Carruseles, reels de fotos, postales | destino, educativo |

Las caras graban 4 videos por mes cada una (reels o tandas de historias); la agencia escribe el guion y edita. Nadie aparece sin haber dado su conformidad.

Peso de cada programa en el mes:

| Período | España | Beatles | Salida de la semana | Destinos |
| --- | --- | --- | --- | --- |
| Diciembre a mayo | 35 % | 30 % | 20 % | 15 % |
| Junio a agosto | 15 % (recaps) | 45 % | 25 % | 15 % |

En LinkedIn, la cuenta de Bettina sigue con España y el oficio; la página de la empresa suma Beatles, la salida de la semana y las reseñas. Instagram es el canal principal.

Ritmo semanal: 1 reel, 2 o 3 posts e historias de lunes a viernes.

## Fundamentos visuales

**Color.** Cuatro colores, nada más:
- `verde` (#396c59) es el color de marca.
- `salvia` (#c8ceb5) es el fondo de las piezas sin foto, con texto `verde`.
- `marfil` (#fffff0) es el fondo claro de los carruseles, con texto `verde`. Sobre `verde`, el texto va en `marfil`.
- `turquesa` (#39b5b9) es el acento: numerales y una palabra destacada, siempre en tamaño grande.
- Sobre foto, el texto va siempre en `blanco`.

**Fotos.** La protagonista de casi todas las piezas es una foto real, a sangre y sin marcos. Priorizá, en este orden:
1. El grupo real viajando: de espaldas mirando un paisaje, caminando, abrazadas.
2. Bettina.
3. El paisaje del destino: costa, pueblo o viñedo.
4. Un detalle sensorial: pintxos, vino.

Para que el texto se lea, va un velo de `negro` en degradé (35 a 55 % detrás del texto, transparente en el resto) y una sombra muy suave en las letras. Nunca uses cajas de color detrás del texto.

**Tipografía.**
- Los títulos van en **Genica One** (`titulo-historia`, `titulo-post`, `frase`, `postal-lugar`): una serif gruesa e inclinada, en minúscula de oración.
- Los textos van en **Raleway liviana** (`antetitulo`, `cuerpo-historia`, `cuerpo-post`). Usá negrita solo para el dato clave: una fecha límite, "incluida" o "Cupos limitados".
- Máximo 6 palabras de título y 35 de texto por pieza.

**Recetas de diseño** (cada una es un componente de este manual):
1. **Historia de bloque:** antetítulo + título + texto, alineados a la izquierda en el tercio central, sobre foto. Para anuncios, destinos y beneficios.
2. **Historia de pregunta:** el mismo bloque, centrado. Para "¿Te sumás?" y "¿Qué te gustaría vivir?".
3. **Postal:** foto del grupo casi sin intervenir, con el año y el destino chiquitos en una esquina.
4. **Frase:** fondo `salvia`, frase grande en `verde` alineada a la derecha, y el avión con su línea punteada arriba.
5. **Lámina de carrusel:** numeral `turquesa`, título y texto centrados verticalmente sobre `marfil`; portada sobre `verde` o sobre foto.
6. **Post de salida:** foto, antetítulo, título, fechas y "Desde **USD …**", con la letra chica abajo y el logo en la esquina.

**Secuencias.** Las salidas se cuentan en series de 3 historias, como la del Norte de España:
1. Anuncio con fechas.
2. Destinos y qué la hace única.
3. Beneficio o pregunta final.

**Formatos y zonas seguras.**
- Historias y reels en 1080 × 1920. Dejá libres 250 px arriba y `zona-segura-abajo` abajo.
- Posts y carruseles en 1080 × 1350.
- Reels de 90 s como máximo.

**Bordes.** Sin bordes, sin esquinas redondeadas (`radius-0`) y sin sombras de caja. La única forma redonda es el logo.

## Reels

1. **Gancho (0–3 s):** la imagen más fuerte primero, con el título en Genica One.
2. **Desarrollo:** cortes cada 1,5 a 3 s, con `subtitulo-video`.
3. **Dato concreto:** fechas y "Desde USD".
4. **Placa de cierre** de 3 s.

Música: de la biblioteca de Instagram o con licencia libre.

## Material, stock e IA

- Primero va el material propio de los viajes.
- Después, stock libre de derechos (Pexels), anotando la fuente en `material/stock/fuentes.txt`.
- La IA se usa solo para ambientar. Nunca para mostrar hoteles, comidas, personas de un paquete ni a Bettina.

## Logo

Usá el logo circular (`assets/Logos/logo-circular.png`) completo: en la placa de cierre y en la esquina de los posts de venta, con 120 px como mínimo. No lo recortes ni lo recolorees. Si el logo no funciona sobre un fondo, escribí "Viajar en Grupo" en Genica One y en `verde`.

## Iconografía

El único recurso gráfico propio es **el avión con su línea punteada**, en `verde` sobre `salvia`. No hay set de íconos, stickers ni flechas: la foto y la tipografía hacen todo el trabajo.

## Revisión antes de enviar a aprobación

- [ ] Precio con "Desde" y su base; fechas y cupos verificados hoy.
- [ ] Un solo llamado a la acción.
- [ ] Título en Genica One, en minúscula de oración y de 6 palabras como máximo.
- [ ] Solo los 4 colores de marca, más blanco sobre foto.
- [ ] Foto real a sangre, con el texto legible gracias al velo.
- [ ] Leg. 19725 en las piezas de venta.
- [ ] Ortografía, voseo, los dos signos de pregunta y hashtags con `#viajarengrupo` primero.
"""
w("README.md", README)

# ---------------------------------------------------------------- previews
FUENTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;600;700&display=swap">')
BASE = """html,body{margin:0}body{background:#fff;display:flex;gap:16px;padding:12px;flex-wrap:wrap;font-family:"Raleway",Arial,sans-serif}
.marco{overflow:hidden;flex:none}.lienzo{transform-origin:0 0;position:relative;overflow:hidden;color:#fff;font-family:"Raleway",Arial,sans-serif}
.v{width:1080px;height:1920px}.p{width:1080px;height:1350px}
.disp{font-family:"Genica One",Georgia,serif;font-weight:400;margin:0;line-height:1.14}
.txt{font-weight:300;margin:0;line-height:1.4}.txt b{font-weight:700}
.foto{position:absolute;inset:0;background:var(--verde) center/cover no-repeat}
.velo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,.42) 28%,rgba(0,0,0,.28) 55%,rgba(0,0,0,0) 78%)}
.sombra{text-shadow:0 2px 18px rgba(0,0,0,.35)}
.ruta{display:flex;align-items:center}.punteada{flex:1;border-top:5px dotted var(--verde)}.avion{fill:var(--verde);flex:none}
.ej{font-size:12px;line-height:16px;color:#555;width:100%;margin:0}"""
AVION = ('<div class="ruta" style="position:absolute;top:310px;left:0;width:640px"><span class="punteada"></span>'
         '<svg class="avion" width="170" height="170" viewBox="0 0 24 24"><path d="M23 12 16 10 11 3H9l3 7H6L4 7H2.5l1 5-1 5H4l2-3h6l-3 7h2l5-7z"/></svg></div>')


def preview(card, titulo, css, cuerpo):
    return f"""{card}
<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>{FUENTES}
<style>{BASE}
{css}</style></head><body>
{cuerpo}
</body></html>
"""


V = '.marco{width:216px;height:384px}.lienzo{transform:scale(.2)}'
VP = '.marco.p4{width:270px;height:337px}.marco.p4 .lienzo{transform:scale(.25)}'

w("components/Historia/preview.html", preview('<!-- @dsCard group="Historias" height=430 -->', "Historia de bloque y de pregunta", V + """
.b{position:absolute;left:120px;right:120px;top:590px;display:grid;gap:30px}
.b.c{left:90px;right:90px;text-align:center}
.b h1{font-size:100px}.b p{font-size:58px}""",
f"""<div class="marco"><div class="lienzo v"><div class="foto" style="background-image:url('{FOTO1}')"></div><div class="velo"></div>
<div class="b sombra"><p class="txt">Nuestra próxima salida grupal</p><h1 class="disp">El Norte de España, con los cinco sentidos.</h1><p class="txt">Del 24 de mayo al 10 de junio de 2027.</p></div></div></div>
<div class="marco"><div class="lienzo v"><div class="foto" style="background-image:url('{FOTO2}')"></div><div class="velo"></div>
<div class="b c sombra"><h1 class="disp">Si te dijéramos que en mayo viajás a España en grupo… ¿te sumás?</h1></div></div></div>
<p class="ej">Bloque a la izquierda para anuncios, destinos y beneficios; centrado para preguntas. Fotos de Pexels como ejemplo.</p>"""))
w("components/Historia/README.md", """Historia 9:16 con una foto a sangre y un bloque de texto (antetítulo, título en Genica One y texto en Raleway liviana) en el tercio central.

- **Qué hay que darle:** una foto vertical real, un título de 6 palabras o menos y, si hace falta, un antetítulo y una línea de texto. En el texto, la negrita marca el dato clave ("**25/10**", "**Cupos limitados**").
- A la izquierda, con `margen-historia` (120 px), para anuncios, destinos y beneficios. Centrado (90 px) para preguntas.
- El texto va en `blanco` sobre el velo de `negro`. Sin cajas de color ni stickers.
- Las salidas se cuentan en series de 3 historias: anuncio, destinos y beneficio o pregunta.
""")

w("components/HistoriaPostal/preview.html", preview('<!-- @dsCard group="Historias" height=430 -->', "Postal", V + """
.f{position:absolute;display:grid;gap:4px}.f.ar{top:260px;right:110px;text-align:right}.f.ab{bottom:330px;left:110px}
.anio{font-size:52px}.lugar{font-size:62px}""",
f"""<div class="marco"><div class="lienzo v"><div class="foto" style="background-image:url('{FOTO2}')"></div>
<div class="f ar sombra"><p class="txt anio">2025</p><p class="disp lugar">San Sebastián</p></div></div></div>
<div class="marco"><div class="lienzo v"><div class="foto" style="background-image:url('{FOTO1}')"></div>
<div class="f ab sombra"><p class="txt anio">2025</p><p class="disp lugar">Norte de España</p></div></div></div>
<p class="ej">Foto del grupo casi sin intervenir; año y destino chiquitos en una esquina.</p>"""))
w("components/HistoriaPostal/README.md", """Postal de un viaje realizado: una foto del grupo a sangre, con el año en Raleway y el destino en Genica One, chiquitos en una esquina.

- **Qué hay que darle:** una foto real del grupo o de las viajeras, el año y el destino.
- La esquina va arriba a la derecha cuando el cielo deja lugar, o abajo a la izquierda con un velo inferior.
- No lleva más texto ni logo: la foto cuenta el viaje.
""")

w("components/HistoriaFrase/preview.html", preview('<!-- @dsCard group="Historias" height=430 -->', "Frase", V + """
.lienzo{background:var(--salvia);color:var(--verde)}
.fr{position:absolute;right:110px;left:150px;top:820px;text-align:right;font-size:134px;line-height:1.2}""",
f"""<div class="marco"><div class="lienzo v">{AVION}<h1 class="disp fr">Viajar es lo único que comprás y te hace más rico.</h1></div></div>
<p class="ej">Fondo salvia, frase en verde alineada a la derecha y el avión con su línea punteada.</p>"""))
w("components/HistoriaFrase/README.md", """Frase de marca sin foto: fondo `salvia`, frase en Genica One y en `verde` alineada a la derecha, y el avión con su línea punteada arriba.

- **Qué hay que darle:** una frase de 12 palabras o menos.
- Se usa una o dos veces por mes, entre piezas de venta, para dar aire a la grilla.
""")

w("components/PortadaReel/preview.html", preview('<!-- @dsCard group="Reels" height=430 -->', "Portada de reel", V + """
.b{position:absolute;left:90px;right:90px;top:720px;text-align:center;display:grid;gap:28px}.b h1{font-size:112px}.b p{font-size:54px}""",
f"""<div class="marco"><div class="lienzo v"><div class="foto" style="background-image:url('{FOTO1}')"></div><div class="velo"></div>
<div class="b sombra"><p class="txt">Bettina responde</p><h1 class="disp">¿Y si viajo sola?</h1></div></div></div>
<p class="ej">El título va en el tercio central, para que se lea recortado a 4:5 en la grilla.</p>"""))
w("components/PortadaReel/README.md", """Portada y primer cuadro del reel: una foto real a sangre con el título centrado en Genica One, en el tercio central.

- **Qué hay que darle:** el mejor cuadro del video (si aparece Bettina, uno donde se la vea) y un título de 6 palabras o menos.
- El título va en `titulo-portada`, en `blanco` sobre el velo.
""")

w("components/PostPaquete/preview.html", preview('<!-- @dsCard group="Posts" height=380 -->', "Post de salida", VP + """
.b{position:absolute;left:100px;right:100px;top:150px;display:grid;gap:24px}.b h1{font-size:100px}
.a{font-size:40px}.s{font-size:44px}.pr{font-size:52px}
.ch{position:absolute;left:100px;right:260px;bottom:60px;font-size:24px;font-weight:400}
.logo{position:absolute;right:70px;bottom:50px;width:130px;height:130px;border-radius:50%}""",
f"""<div class="marco p4"><div class="lienzo p"><div class="foto" style="background-image:url('{FOTO1}')"></div><div class="velo"></div>
<img class="logo" src="/_blob/c4722e25534c8b0ed90b45356b4663bd" alt="">
<div class="b sombra"><p class="txt a">Especial de agencia · Salida acompañada</p><h1 class="disp">Norte de España</h1>
<p class="txt s">24 may – 10 jun 2027 · 18 días</p><p class="txt pr">Desde <b>USD 9.680</b></p></div>
<p class="txt ch sombra">Por persona en base doble · Suplemento single USD 2.290 · Leg. 19725 · Precios sujetos a disponibilidad y cambio</p></div></div>
<p class="ej">Ejemplo con datos verificados en la web el 20/10/2026.</p>"""))
w("components/PostPaquete/README.md", """Post 4:5 para vender una salida: foto a sangre, antetítulo, título, fechas y "Desde **USD …**", con la letra chica abajo y el logo en la esquina.

- **Qué hay que darle:** foto del destino o del grupo, el tipo (Especial de agencia solo para salidas propias; si no, Salida grupal), el destino, las fechas, el precio "desde" verificado hoy y la letra chica.
- Sin precio publicado, la línea dice "**Consultá cupos**".
""")

w("components/LaminaEducativa/preview.html", preview('<!-- @dsCard group="Posts" height=380 -->', "Lámina de carrusel", VP + """
.oscuro{background:var(--verde);color:var(--marfil)}.claro{background:var(--marfil);color:var(--verde)}
.c{position:absolute;left:110px;right:110px;top:0;bottom:110px;display:flex;flex-direction:column;justify-content:center;gap:32px}
.c h1{font-size:98px}.portada .c h1{font-size:118px}.c .x{font-size:54px}.c .a{font-size:46px}
.n{font-family:"Genica One",Georgia,serif;font-size:170px;line-height:1;color:var(--turquesa)}
.pie{position:absolute;left:110px;bottom:70px;font-size:26px;font-weight:500}""",
"""<div class="marco p4"><div class="lienzo p oscuro portada"><div class="c"><p class="txt a">Tips de viaje</p><h1 class="disp">5 mitos del viaje grupal</h1></div><div class="pie">@viajar.en.grupo</div></div></div>
<div class="marco p4"><div class="lienzo p claro"><div class="c"><div class="n">1</div><h1 class="disp">"Voy a estar con gente que no conozco"</h1><p class="txt x">La mayoría llega sin conocer a nadie. El grupo se arma solo, entre cenas y recorridos.</p></div><div class="pie">@viajar.en.grupo</div></div></div>
<p class="ej">Portada sobre verde (o sobre foto) y láminas sobre marfil con numeral turquesa.</p>"""))
w("components/LaminaEducativa/README.md", """Lámina 4:5 de carrusel: numeral en `turquesa`, título en Genica One y texto en Raleway liviana, centrados verticalmente.

- **Qué hay que darle:** un título corto y un texto de 35 palabras o menos por lámina.
- La portada va sobre `verde` con texto `marfil`, o sobre una foto con velo. Las láminas van sobre `marfil` con texto `verde`.
- La última lámina siempre lleva el llamado a la acción.
""")

w("components/PlacaCierre/preview.html", preview('<!-- @dsCard group="Reels" height=430 -->', "Placa de cierre", V + """
.lienzo{background:var(--salvia);color:var(--verde)}
.logo{position:absolute;right:110px;top:300px;width:230px;height:230px;border-radius:50%}
.t{position:absolute;left:110px;right:110px;top:860px;display:grid;gap:36px}.t h1{font-size:120px}.t p{font-size:54px;font-weight:600}.t p.ch{font-size:34px;font-weight:400}""",
f"""<div class="marco"><div class="lienzo v">{AVION.replace('top:310px', 'top:420px')}<img class="logo" src="/_blob/c4722e25534c8b0ed90b45356b4663bd" alt="">
<div class="t"><h1 class="disp">¿Nos acompañás?</h1><p class="txt">WhatsApp +54 9 11 4434-0161</p><p class="txt ch">viajarengrupo.tur.ar · Leg. 19725</p></div></div></div>
<p class="ej">Últimos 3 segundos de cada reel.</p>"""))
w("components/PlacaCierre/README.md", """Últimos 3 segundos de cada reel: fondo `salvia`, el avión con su línea punteada, el logo, la frase de cierre en Genica One y el WhatsApp.

- **Qué hay que darle:** una frase de cierre de 4 palabras o menos ("¿Nos acompañás?", "¿Te sumás?").
- Entra con un fundido de 0,3 s.
""")

# ---------------------------------------------------------------- portada
w("components/Cover/preview.html", """<!-- @dsCard height=288 -->
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Viajar en Grupo</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500&display=swap">
<style>
  html, body { margin:0; height:100%; }
  body { background:var(--marfil); color:var(--verde); font-family:"Raleway", Arial, sans-serif; overflow:hidden; }
  .cover { position:relative; height:288px; overflow:hidden; }
  .art { position:absolute; top:0; left:480px; width:480px; height:288px; overflow:hidden; }
  .art svg { display:block; width:480px; height:288px; }
  .verde { fill:var(--verde); }
  .salvia { fill:var(--salvia); }
  .turquesa { fill:var(--turquesa); }
  .ruta { fill:none; stroke:var(--marfil); stroke-width:4; stroke-dasharray:2 10; stroke-linecap:round; }
  .avion { fill:var(--marfil); }
  .words { position:absolute; left:64px; bottom:40px; max-width:440px; }
  .name { margin:0; font-family:"Genica One", Georgia, serif; font-weight:400; font-size:76px; line-height:1.02; color:var(--verde); }
  .tag { margin:14px 0 0 2px; font-size:14px; line-height:20px; font-weight:500; color:var(--verde); }
</style>
</head>
<body>
<div class="cover">
<div class="art" aria-hidden="true">
<svg viewBox="0 0 480 288" width="480" height="288">
<!--
  blocks      salvia 288x320 bled off the top and bottom (the background of the brand's quote pieces) - verde 176x256 bled off the right - turquesa 64x96 once; about 45% of 960x288
  arrangement one tall salvia field with a verde slab bled off the right and a small turquesa satellite, bottoms aligned
  pattern     literal motif from the brand's quote stories: one dotted flight route in marfil crossing the salvia field, ending in the plane silhouette
  scales      sides in 16px multiples; corners radius-0 everywhere (photos and fields are always bleed, no rounded corners)
-->
<rect class="salvia" x="16" y="-16" width="288" height="320"/>
<rect class="verde" x="320" y="48" width="176" height="256"/>
<rect class="turquesa" x="240" y="176" width="64" height="96"/>
<path class="ruta" d="M16 120 C 90 70, 170 70, 236 104"/>
<g transform="translate(232 82) scale(2.2)"><path class="avion" d="M23 12 16 10 11 3H9l3 7H6L4 7H2.5l1 5-1 5H4l2-3h6l-3 7h2l5-7z"/></g>
</svg>
</div>
<div class="words">
<h1 class="name">Viajar en Grupo</h1>
<p class="tag">Salidas grupales acompañadas, armadas por personas.</p>
</div>
</div>
</body>
</html>
""")

# ---------------------------------------------------------------- índice (se publica último)
indice = json.loads((P / "design-system.json").read_text(encoding="utf-8"))
ahora = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
indice["groups"] = ["Logos", "Fotos"]
indice["assetGroups"]["Fotos"] = {"name": "Fotos", "tile": "m", "order": ["gaztelugatxe.jpg", "san-sebastian.jpg"], "files": {
    "gaztelugatxe.jpg": {"name": "gaztelugatxe.jpg", "blob": "5e50bf0c0b29515002037e3bd7889d65", "size": 355902, "type": "image/jpeg"},
    "san-sebastian.jpg": {"name": "san-sebastian.jpg", "blob": "fe9c118f5a4d1ce9a9ce517ffeae0862", "size": 326057, "type": "image/jpeg"},
}}
indice["lastChange"] = {"by": "Manuel", "at": ahora, "via": "Claude Code",
                        "note": "Paleta propia (#396c59, #c8ceb5, #39b5b9, #fffff0), Genica One + Raleway y recetas tomadas de las historias publicadas"}
w("design-system.json", json.dumps(indice, ensure_ascii=False, indent=2) + "\n")
w("assets/Fotos/README.md", "Fotos libres de Pexels usadas solo para mostrar el tratamiento de imagen en los ejemplos del manual. En las piezas reales va primero el material propio de los viajes.\n")
print("manual listo en", P)
