"""Aplica el estilo real de @viajar.en.grupo (ejemplos del 20/10/2026) a las plantillas.

Paleta: #396c59 verde · #c8ceb5 salvia · #39b5b9 turquesa · #fffff0 marfil.
Títulos: Genica One (plantillas/fuentes/GenicaOne-Regular.otf); si faltara, Shrikhand.
Textos: Raleway liviana. Uso: .venv/Scripts/python docs/referencias/aplicar_estilo_2026-10-20.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
P = RAIZ / "plantillas"

AVION = ('<div class="ruta"><span class="punteada"></span><svg class="avion" viewBox="0 0 24 24" aria-hidden="true">'
         '<path d="M23 12 16 10 11 3H9l3 7H6L4 7H2.5l1 5-1 5H4l2-3h6l-3 7h2l5-7z"/></svg></div>')

HEAD = '<!doctype html><html lang="es"><head><meta charset="utf-8"><link rel="stylesheet" href="{{ raiz }}/base.css"><style>\n'
FOTO = '<div class="foto"{% if foto %} style="background-image:url(\'{{ foto }}\')"{% endif %}></div>'

ARCHIVOS = {
"base.css": """@font-face{font-family:"Genica One";src:url("fuentes/GenicaOne-Regular.otf") format("opentype")}
@font-face{font-family:"Shrikhand";src:url("fuentes/Shrikhand-Regular.ttf") format("truetype")}
@font-face{font-family:"Raleway";src:url("fuentes/Raleway.ttf") format("truetype");font-weight:100 900}
:root{--verde:#396c59;--salvia:#c8ceb5;--turquesa:#39b5b9;--marfil:#fffff0;--blanco:#ffffff;--negro:#000000;
--font-display:"Genica One","Shrikhand",Georgia,serif;--font-texto:"Raleway",Arial,sans-serif}
html,body{margin:0;background:transparent}
.lienzo{position:relative;overflow:hidden;font-family:var(--font-texto);color:var(--blanco)}
.v{width:1080px;height:1920px}.p{width:1080px;height:1350px}
.disp{font-family:var(--font-display);font-weight:400;margin:0;line-height:1.14;letter-spacing:0;text-wrap:balance}
.txt{font-family:var(--font-texto);font-weight:300;margin:0;line-height:1.4}
.txt b,.txt strong{font-weight:700}
.foto{position:absolute;inset:0;background:var(--verde) center/cover no-repeat}
.velo-arriba{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,.42) 28%,rgba(0,0,0,.28) 55%,rgba(0,0,0,0) 78%)}
.velo-centro{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 15%,rgba(0,0,0,.5) 40%,rgba(0,0,0,.5) 62%,rgba(0,0,0,0) 85%)}
.velo-abajo{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.75) 100%)}
.sombra{text-shadow:0 2px 18px rgba(0,0,0,.35)}
.ruta{display:flex;align-items:center}
.punteada{flex:1;border-top:5px dotted var(--verde);height:0}
.avion{width:110px;height:110px;fill:var(--verde);flex:none;margin-left:-6px}
.pie{position:absolute;font-family:var(--font-texto);font-weight:500;font-size:26px;letter-spacing:.04em}
""",

"historia.html.j2": HEAD + """.b{position:absolute;left:120px;right:120px;top:{{ top|default(590) }}px;display:grid;gap:30px}
.b.centro{text-align:center;left:90px;right:90px}
.ante{font-size:58px}
.b h1{font-size:{{ tam|default(100) }}px}
.b .x{font-size:58px}
.b .cta{font-size:58px;font-weight:700}
.b.abajo{top:auto;bottom:{{ bottom|default(380) }}px}
</style></head><body><div class="lienzo v">""" + FOTO + """<div class="{{ 'velo-abajo' if posicion == 'abajo' else ('velo-centro' if alineacion == 'centro' else 'velo-arriba') }}"></div>
<div class="b sombra{{ ' centro' if alineacion == 'centro' }}{{ ' abajo' if posicion == 'abajo' }}">
{% if etiqueta %}<p class="txt ante">{{ etiqueta }}</p>{% endif %}
<h1 class="disp">{{ titulo }}</h1>
{% if texto %}<p class="txt x">{{ texto }}</p>{% endif %}
{% if cta %}<p class="txt cta">{{ cta }}</p>{% endif %}
</div></div></body></html>
""",

"historia_postal.html.j2": HEAD + """.f{position:absolute;display:grid;gap:4px}
.f.arriba{top:260px;right:110px;text-align:right}.f.abajo{bottom:330px;left:110px}
.anio{font-size:52px}.lugar{font-size:62px}
</style></head><body><div class="lienzo v">""" + FOTO + """{% if esquina == 'abajo' %}<div class="velo-abajo"></div>{% endif %}
<div class="f sombra {{ 'abajo' if esquina == 'abajo' else 'arriba' }}"><p class="txt anio">{{ anio }}</p><p class="disp lugar">{{ lugar }}</p></div>
</div></body></html>
""",

"historia_frase.html.j2": HEAD + """.lienzo{background:var(--salvia);color:var(--verde)}
.ruta{position:absolute;top:310px;left:0;width:640px}
.ruta .avion{width:170px;height:170px}
.frase{position:absolute;right:110px;left:150px;top:{{ top|default(820) }}px;text-align:right;font-size:{{ tam|default(134) }}px;line-height:1.2;text-wrap:wrap}
</style></head><body><div class="lienzo v">""" + AVION + """<h1 class="disp frase">{{ frase }}</h1></div></body></html>
""",

"portada_reel.html.j2": HEAD + """.b{position:absolute;left:90px;right:90px;top:720px;text-align:center;display:grid;gap:28px}
.b h1{font-size:112px}
.b p{font-size:54px}
.ante{font-size:48px}
.b.abajo{top:auto;bottom:520px}
</style></head><body><div class="lienzo v">""" + FOTO + """<div class="{{ 'velo-abajo' if posicion == 'abajo' else 'velo-centro' }}"></div>
<div class="b sombra{{ ' abajo' if posicion == 'abajo' }}">{% if etiqueta %}<p class="txt ante">{{ etiqueta }}</p>{% endif %}<h1 class="disp">{{ titulo }}</h1>{% if subtitulo %}<p class="txt">{{ subtitulo }}</p>{% endif %}</div>
</div></body></html>
""",

"placa_cierre.html.j2": HEAD + """.lienzo{background:var(--salvia);color:var(--verde)}
.ruta{position:absolute;top:420px;left:0;width:640px}
.logo{position:absolute;right:110px;top:300px;width:230px;height:230px;border-radius:50%}
.t{position:absolute;left:110px;right:110px;top:860px;display:grid;gap:36px}
.t h1{font-size:120px}
.t p{font-size:54px;font-weight:600}
.t p.chica{font-size:34px;font-weight:400}
</style></head><body><div class="lienzo v">""" + AVION + """<img class="logo" src="{{ raiz }}/logo-circular.png" alt="">
<div class="t"><h1 class="disp">{{ frase }}</h1><p class="txt">WhatsApp +54 9 11 4434-0161</p><p class="txt chica">viajarengrupo.tur.ar · Leg. 19725</p></div>
</div></body></html>
""",

"subtitulo.html.j2": HEAD + """.s{position:absolute;left:90px;right:90px;bottom:430px;text-align:center}
.s p{font-size:54px;font-weight:600;line-height:1.3;text-shadow:0 2px 14px rgba(0,0,0,.75),0 0 3px rgba(0,0,0,.6)}
</style></head><body><div class="lienzo v"><div class="s"><p class="txt">{{ texto }}</p></div></div></body></html>
""",

"lamina.html.j2": HEAD + """.oscuro{background:var(--verde);color:var(--marfil)}.claro{background:var(--marfil);color:var(--verde)}
.n{font-family:var(--font-display);font-size:170px;line-height:1;color:var(--turquesa)}
.c{position:absolute;left:110px;right:110px;top:{{ top|default(300) }}px;display:flex;flex-direction:column;gap:32px}
.claro .c,.oscuro .c{top:0;bottom:110px;justify-content:center}
.c .ante{font-size:46px}
.c h1{font-size:{{ tam|default(98) }}px}
.c .x{font-size:54px}
.portada .c h1{font-size:{{ tam|default(118) }}px}
.pie{left:110px;bottom:70px}
.con-foto{color:var(--blanco)}
.c.abajo{top:auto;bottom:130px}
</style></head><body><div class="lienzo p {{ 'con-foto' if foto else ('oscuro' if oscuro else 'claro') }}{{ '' if numero else ' portada' }}">
{% if foto %}""" + FOTO + """<div class="{{ 'velo-abajo' if posicion == 'abajo' else 'velo-arriba' }}"></div>{% endif %}
<div class="c{{ ' sombra' if foto }}{{ ' abajo' if posicion == 'abajo' }}">{% if numero %}<div class="n">{{ numero }}</div>{% endif %}{% if etiqueta %}<p class="txt ante">{{ etiqueta }}</p>{% endif %}<h1 class="disp">{{ titulo }}</h1>{% if texto %}<p class="txt x">{{ texto }}</p>{% endif %}</div>
<div class="pie">@viajar.en.grupo</div>
</div></body></html>
""",

"post_paquete.html.j2": HEAD + """.b{position:absolute;left:100px;right:100px;top:150px;display:grid;gap:24px}
.ante{font-size:40px}
.b h1{font-size:100px}
.sub{font-size:44px}
.precio{font-size:52px}
.chica{position:absolute;left:100px;right:260px;bottom:60px;font-size:24px;font-weight:400;opacity:.92}
.logo{position:absolute;right:70px;bottom:50px;width:130px;height:130px;border-radius:50%}
</style></head><body><div class="lienzo p">""" + FOTO + """<div class="velo-arriba"></div><div class="velo-abajo" style="opacity:.6"></div>
<img class="logo" src="{{ raiz }}/logo-circular.png" alt="">
<div class="b sombra">
<p class="txt ante">{{ etiqueta }}</p>
<h1 class="disp">{{ titulo }}</h1>
<p class="txt sub">{{ subtitulo }}</p>
<p class="txt precio">{% if precio == "CONSULTÁ CUPOS" %}<b>Consultá cupos</b>{% else %}Desde <b>{{ precio }}</b>{% endif %}</p>
</div>
<p class="txt chica sombra">{{ letra_chica }}</p>
</div></body></html>
""",
}

for nombre, contenido in ARCHIVOS.items():
    (P / nombre).write_text(contenido, encoding="utf-8", newline="\n")
    print("plantilla", nombre)

render = RAIZ / "veg" / "render.py"
t = render.read_text(encoding="utf-8")
viejo = '"placa_cierre": (1080, 1920), "subtitulo": (1080, 1920),\n}'
if viejo in t:
    t = t.replace(viejo, '"placa_cierre": (1080, 1920), "subtitulo": (1080, 1920),\n'
                         '    "historia_postal": (1080, 1920), "historia_frase": (1080, 1920),\n}')
    render.write_text(t, encoding="utf-8", newline="\n")
    print("render.py: tamaños nuevos")
else:
    print("AVISO: render.py sin cambios")

tests = RAIZ / "tests" / "test_render.py"
t = tests.read_text(encoding="utf-8")
cambios = [
    ('"USD 9.680" in h and "DESDE" in h', '"USD 9.680" in h and "Desde" in h'),
    ('"CONSULTÁ CUPOS" in h and "DESDE" not in h', '"Consultá cupos" in h and "Desde" not in h'),
    ('    ("placa_cierre", {"frase": "¿Nos acompañás?"}, (1080, 1920)),\n])',
     '    ("placa_cierre", {"frase": "¿Nos acompañás?"}, (1080, 1920)),\n'
     '    ("historia_postal", {"anio": "2025", "lugar": "Sur de Francia", "esquina": "abajo"}, (1080, 1920)),\n'
     '    ("historia_frase", {"frase": "Viajar es lo único que comprás y te hace más rico."}, (1080, 1920)),\n])'),
]
for viejo, nuevo in cambios:
    n = t.count(viejo)
    if not n:
        print("AVISO: no encontré en tests:", viejo[:60])
    t = t.replace(viejo, nuevo)
tests.write_text(t, encoding="utf-8", newline="\n")
print("tests actualizados")
