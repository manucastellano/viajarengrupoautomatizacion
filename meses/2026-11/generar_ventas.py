"""Suma dos ventas de Europa BA a noviembre sin sacar piezas.

Viernes 13 → Europeando Fiestas; viernes 27 → Ellas a Europa. Granada pasa al sábado 14 y Porto al sábado 28.
Cada venta suma una placa extra a la historia de ese viernes.
Uso: .venv/Scripts/python meses/2026-11/generar_ventas.py
"""
import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from veg.formato import LETRA_CHICA_VENTA, formatear_precio, rango_fechas  # noqa: E402
from veg.modelos import Pieza, Salida, cargar_piezas, cargar_salidas, guardar  # noqa: E402
from veg.render import render_png  # noqa: E402
from veg.revisor import revisar  # noqa: E402

HOY = date(2026, 10, 21)
MES = RAIZ / "meses" / "2026-11"
MIX = RAIZ / "material" / "propias" / "MIX"
HT = ["#viajarengrupo", "#viajesgrupales", "#agenciadeviajes"]
CONTACTO = "📲 El WhatsApp de Bettina está en el link de nuestro perfil."
URL = "https://europaba.com/page/destinos-internacionales1610045318780"

FIESTAS = Salida(id="europaba-europeando-fiestas", destino="Europeando Fiestas", fecha_salida=date(2026, 12, 18),
                 fecha_regreso=date(2027, 1, 2), duracion="13 noches", operador="Europa BA", url=URL,
                 cupo="disponible", verificado_en=HOY, precio_desde=3900, base="por persona")
ELLAS = Salida(id="europaba-ellas-a-europa-feb", destino="Ellas a Europa", fecha_salida=date(2027, 2, 5),
               fecha_regreso=date(2027, 2, 22), duracion="15 noches", operador="Europa BA",
               url="https://europaba.com/page/ellas-viajan1657035006987", cupo="disponible", verificado_en=HOY,
               precio_desde=3900, base="por persona")

ventas = [
    (FIESTAS, date(2026, 11, 13), "Fiestas en Europa", "Salida grupal · Europa BA", MIX / "01-1-LmMEYNuDxgTkkDLFr0uLbY0f9n_W8yZ.jpg",
     "¿Te imaginás pasar las fiestas en Europa? 🎄✨\n\nUna salida grupal para recibir Navidad y Año Nuevo viajando, en compañía y con todo organizado.\n\n"
     f"📅 Del 18 de diciembre de 2026 al 2 de enero de 2027 · 13 noches · aéreo incluido\n"
     f"Desde {formatear_precio(3900)} por persona. Tarifa del operador sujeta a disponibilidad.\n\n"
     "Comentá FIESTAS y te mando el itinerario por privado ✈️",
     ["#navidadeneuropa", "#añonuevo", "#europa"]),
    (ELLAS, date(2026, 11, 27), "Ellas a Europa", "Salida de mujeres · Europa BA", MIX / "10-1szybzRnCItUPFb7Q7-_dhUD1VPPCqWJc.jpg",
     "Viajar entre mujeres tiene algo especial 💫\n\nUna salida pensada para viajar sola sin estar sola: grupo de mujeres, acompañamiento durante todo el viaje y Europa en febrero.\n\n"
     f"📅 Del 5 al 22 de febrero de 2027 · 15 noches · acompañada\n"
     f"Desde {formatear_precio(3900)} por persona. Tarifa del operador sujeta a disponibilidad.\n\n"
     "Comentá ELLAS y te mando el itinerario por privado ✈️",
     ["#ellasviajan", "#viajarsola", "#mujeresqueviajan"]),
]

piezas = cargar_piezas(MES / "piezas.json")
por_id = {p.id: p for p in piezas}
nuevas, renders = [], []
for salida, viernes, titulo, etiqueta, foto, texto, hashtags in ventas:
    # la pieza de destino del viernes pasa al sábado (mismas imágenes)
    vieja = por_id.pop(f"{viernes.isoformat()}-post")
    sabado = date(viernes.year, viernes.month, viernes.day + 1)
    movida = replace(vieja, id=f"{sabado.isoformat()}-post", fecha=sabado, hora="11:00")
    venta = Pieza(id=f"{viernes.isoformat()}-post", fecha=viernes, hora="13:00", formato="post", pilar="paquete",
                  tema=f"{salida.destino} ({salida.operador})", salida_id=salida.id, titulo=titulo,
                  texto=texto + "\n\n" + CONTACTO, hashtags=HT + hashtags)
    nuevas += [movida, venta]
    fechas = rango_fechas(salida.fecha_salida, salida.fecha_regreso)
    renders.append((venta.id, "01-post_paquete.png", "post_paquete",
                    {"etiqueta": etiqueta, "titulo": titulo, "subtitulo": f"{fechas} · {salida.duracion}", "precio": salida.precio_desde,
                     "letra_chica": f"Precio por persona publicado por el operador · {LETRA_CHICA_VENTA}", "foto": foto, "posicion": "abajo"}))
    historia = por_id[f"{viernes.isoformat()}-historias"]
    historia.salida_id = salida.id
    historia.texto = historia.texto + f"\nPlaca 2: venta de {titulo} · Desde {formatear_precio(3900)} · con sticker de enlace."
    renders.append((historia.id, "02-historia.png", "historia",
                    {"etiqueta": "Salida grupal", "titulo": titulo, "texto": f"{fechas} · Desde {formatear_precio(3900)}",
                     "cta": "Link en el perfil", "foto": foto, "posicion": "abajo"}))

todas = list(por_id.values()) + nuevas
salidas = {s.id: s for s in cargar_salidas(MES / "salidas.json") + [FIESTAS, ELLAS]}
for s in salidas.values():
    if s.especial:
        s.verificado_en = HOY
problemas = {p.id: v for p in nuevas + [por_id["2026-11-13-historias"], por_id["2026-11-27-historias"]]
             if (v := revisar(p, salidas.get(p.salida_id), HOY))}
if problemas:
    print(json.dumps(problemas, ensure_ascii=False, indent=2))
    raise SystemExit("Hay piezas con problemas.")
guardar(MES / "salidas.json", list(salidas.values()))
guardar(MES / "piezas.json", sorted(todas, key=lambda p: (p.fecha, p.hora)))
for pid, nombre, plantilla, datos in renders:
    render_png(plantilla, datos, MES / "piezas" / pid / nombre)
    print("render", pid, nombre)
