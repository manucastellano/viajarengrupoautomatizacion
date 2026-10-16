# Community Manager VEG — Especificación de diseño

Fecha: 2026-10-15 · Estado: diseño aprobado por Manuel, pendiente de revisión escrita

## 1. Objetivo

Un equipo de agentes que produce todo el contenido mensual de Instagram de Viajar en Grupo (@viajar.en.grupo): reels, posts e historias. Manuel solo aprueba o pide cambios desde un tablero web, y publica lo aprobado desde Meta Business Suite.

**Éxito:** cada mes, el día 25, el tablero tiene todas las piezas del mes siguiente listas para revisar. Para aprobar, Manuel no tiene que diseñar, escribir ni editar nada.

## 2. Alcance

Incluye:
- Investigación de salidas vendibles (web propia + webs públicas de mayoristas).
- Calendario mensual.
- Textos de posteo.
- Diseño de posts, carruseles e historias.
- Edición de reels verticales.
- Revisión de calidad.
- Tablero de aprobación.
- Exportación de archivos finales.

No incluye:
- Publicar en Instagram. No hay conector: Manuel programa desde Meta Business Suite.
- Responder mensajes o comentarios.
- Pauta paga.
- Otras redes.

## 3. Insumos fijos

| Insumo | Fuente |
| --- | --- |
| Manual de marca (colores, tipografías, voz, pilares, plantillas) | https://claude.ai/artifact/PtTQiusa72f1hrbhu3Jy7J (`project/README.md`, `project/tokens.json`, `project/components/*`) |
| Salidas y precios | viajarengrupo.tur.ar + webs públicas de Dopazo & Ravenna, Eurovips, King Midas, Europa BA, Tower Travel |
| Especial de agencia | Norte de España con los 5 sentidos, 24 may – 10 jun 2027, desde USD 9.680 p/p base doble, suplemento single USD 2.290 |
| Material propio | Google Drive de la agencia (requiere conectar el conector de Google Drive, o descarga a carpeta local `material/`) |
| Tipografías | Unica One (provisoria, Google Fonts) → Genica cuando llegue el archivo; Raleway |

## 4. Grilla y reparto mensual

- **Lunes 19:00:** post o carrusel.
- **Miércoles 20:00:** reel (1 por semana, ≤ 90 s, ideal 30–60 s, 1080×1920).
- **Viernes 13:00:** post de venta.
- **Lunes a viernes:** 3–5 historias por día, con un tema por día:
  - Lunes: tip.
  - Martes: encuesta de destino.
  - Miércoles: compartir el reel y mostrar los cupos.
  - Jueves: Bettina o detrás de escena (con guion de 3 líneas para grabar).
  - Viernes: próximas salidas con link.
- **Mes de 4 semanas:** 4 reels (especial, paquete, destino, agencia) y 8 posts. Los viernes van 2 especiales y 2 paquetes; los lunes, 2 educativos, 1 de destino y 1 de agencia. En el feed suman 12 piezas: especial 3 (25 %), paquete 3 (25 %), destino 2, educativo 2 y agencia 2 (17 % cada uno). Las historias compensan destino y agencia. En un mes de 5 semanas, la semana extra repite el esquema de la semana 1.
- **Reglas de selección:**
  - Solo salidas con cupo verificado el mismo día.
  - Se priorizan las de partida más próxima.
  - Las salidas que parten dentro del mes calendario no se venden: se usan para contenido de "salimos" y después de recap.
- Los horarios se ajustan cuando Manuel comparta las estadísticas de Instagram.

## 5. Agentes y flujo mensual

Todo se dispara con el pedido "armá <mes>". Más adelante puede programarse para el día 18.

| Día | Agente | Entrada | Salida |
| --- | --- | --- | --- |
| 18 | Investigador | Webs de la agencia y mayoristas | `meses/<AAAA-MM>/salidas.json`: destino, fechas, precio desde, base, suplemento, operador, URL, cupo, fecha de verificación |
| 18 | Estratega | `salidas.json`, grilla, pilares | `meses/<AAAA-MM>/calendario.json`: una entrada por pieza con id, fecha, hora, formato, pilar, tema, objetivo y material requerido |
| 19 | (pedido de material) | `calendario.json` | Lista legible para Manuel con los clips y fotos que hacen falta por pieza |
| 20–23 | Copywriter | Calendario y voz del manual | Texto de posteo, CTA y hashtags por pieza |
| 20–23 | Diseñador | Calendario, plantillas del manual y fotos | PNG 1080×1350 (post/lámina) y 1080×1920 (historia) |
| 20–23 | Editor de video | Calendario, clips, música libre | MP4 final 1080×1920 (calidad completa) + preview 720p ≤ 18 MB |
| 24 | Revisor | Todas las piezas | Checklist del manual por pieza; precios y cupos re-verificados; piezas que no pasan vuelven al agente que las hizo |
| 25 | — | Piezas aprobadas por el revisor | Tablero del mes publicado |
| 26–30 | (ajustes) | Pedidos de cambio del tablero | Versión 2 de cada pieza observada |

**Producción técnica**
- Gráficas: HTML/CSS con los tokens y las plantillas del manual, renderizado a PNG con un navegador headless.
- Reels: ffmpeg para cortes, escalado, subtítulos quemados y placa de cierre. La placa y las portadas se renderizan desde las plantillas.
- Música: biblioteca de Instagram (se agrega al subir) o temas con licencia libre. Por defecto el MP4 sale sin música y con una nota de qué tema sugerido usar en Instagram, para evitar problemas de derechos.

## 6. Tablero de aprobación

Es un artifact privado por mes ("Tablero Noviembre 2026").

**Capacidades**
- `db`: piezas y decisiones.
- `assets`: imágenes y previews de video.
- `downloads`: bajar finales.
- `user`: saber quién aprobó.

**Datos, colección `piezas`, un documento por pieza**
```
id, fecha (AAAA-MM-DD), hora (HH:MM), formato (reel|post|carrusel|historia),
pilar (especial|paquete|destino|educativo|agencia), titulo, texto, hashtags,
assets: [ids], verificacion: {fuente, fecha}, version (1..n),
estado (pendiente|aprobada|cambios|descartada), comentario, decididoPor, decididoEn
```

**Pantalla**
- **Resumen:** totales por estado y barra de avance.
- **Dos vistas:** Calendario (miniaturas por día, color por pilar) y Grilla de Instagram (cómo queda el feed).
- **Detalle de pieza:**
  - Vista previa (imagen, carrusel deslizable o video vertical).
  - Texto con botón "Copiar".
  - Ficha con fecha, hora, pilar y verificación.
  - Botones Aprobar, Pedir cambio (con caja de texto) y Descartar.
  - Botón "Descargar" en las piezas aprobadas.

**Ciclo**
1. Manuel decide en el tablero y escribe "revisá el tablero".
2. Claude lee `piezas` con `estado = cambios`, corrige, sube la versión nueva, incrementa `version` y vuelve el estado a `pendiente`.

**Límites**
- Cada archivo pesa como máximo 20 MB. Por eso los reels se suben en preview 720p.
- El MP4 final queda en `meses/<AAAA-MM>/finales/` (local o Drive).
- El tablero es mobile-first y usa los colores y tipografías del manual.

## 7. Estructura de carpetas del proyecto

```
Community Manager VEG/
  agentes/            instrucciones de cada agente (investigador, estratega, copy, diseño, video, revisor)
  plantillas/         plantillas HTML de piezas (derivadas del manual)
  herramientas/       scripts: render PNG, edición de reel, subida al tablero
  material/           fotos y clips (o sincronizados desde Drive)
  meses/AAAA-MM/      salidas.json, calendario.json, piezas/, finales/
```

## 8. Errores y casos límite

- **Una web de mayorista no responde o cambió:** la salida queda "sin verificar" y no se usa para venta. El revisor lo informa.
- **Falta material para un reel:** se usa la alternativa "reel de fotos + texto" o stock, siempre marcado en la ficha.
- **Precio "a consultar":** la cápsula de precio dice CONSULTÁ CUPOS.
- **Cambia una fecha o precio después del 25:** antes de exportar se vuelve a verificar. Si cambió, la pieza vuelve a pendiente con nota.
- **Genica no llega:** se sigue con Unica One sin bloquear.

## 9. Verificación

- Cada pieza pasa la checklist del manual (revisor).
- **Prueba de punta a punta antes del primer mes real:** un mini-mes de 1 semana (1 reel, 2 posts, 5 días de historias) recorre todo el flujo hasta el tablero, y Manuel aprueba o rechaza al menos una pieza para probar el ciclo de cambios.
- **Primer mes real:** noviembre 2026, con el tablero entregado el 25/10/2026.

## 10. Dependencias pendientes de Manuel

1. Conectar Google Drive o bajar material a `material/`.
2. Elegir la carpeta definitiva del proyecto.
3. Archivo de la fuente Genica (opcional, no bloquea).
4. Estadísticas de Instagram para ajustar horarios (opcional).
