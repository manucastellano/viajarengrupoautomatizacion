---
name: arma-mes
description: Usar cuando Manuel pida "armá <mes>" o "revisá el tablero" para el contenido de Instagram de Viajar en Grupo.
---

# Armá <mes>

Mes objetivo = el que nombra Manuel (si dice "el próximo", el mes siguiente a hoy). Carpeta: `meses/AAAA-MM/`.

1. **Investigador**: lanzá un subagente con `agentes/investigador.md`. Esperá `salidas.json`.
2. **Estratega**: subagente con `agentes/estratega.md`. Esperá `calendario.json` y `material.md`.
3. **Material**: mostrale a Manuel el contenido de `material.md` y pedile que deje los archivos en `material/` (o que confirme que ya están en Drive). Si falta material para una pieza, se usa el plan B del manual (stock o fotos + texto) y se anota.
4. **Producción**: primero un subagente con `agentes/copywriter.md`; cuando termina, en paralelo, un subagente con `agentes/disenador.md` y uno con `agentes/editor-video.md` por reel (el editor espera la portada y la placa del diseñador).
5. **Revisor**: subagente con `agentes/revisor.md`. Seguí hasta que `revision.md` no tenga problemas abiertos, salvo los marcados "a decidir por Manuel".
6. **Tablero**:
   a. `preparar_pagina(anio, mes, meses/AAAA-MM/tablero.html)` y publicarlo con Artifact (`icon: "calendar"`, `capabilities: {"db": {}, "downloads": true, "user": {}, "assets": {}}`; `assets` es obligatorio para poder subir las imágenes).
   b. Subir los PNG y las previews como assets (`asset: true`, `file_paths`, hasta 25 por llamada) y guardar `assets.json` = `{pieza_id: [{id, tipo, nombre}]}`.
   c. `escribir_filas(...)` → `filas.json`; `escribir_documentos(filas.json, meses/AAAA-MM/docs)` → un `<id>.json` por pieza; cargarlos con `ArtifactData` `batch` (hasta 50 entradas `{op: "set", collection: "piezas", doc_id, file_path}` por llamada).
   d. `ArtifactData` `list` de `piezas`: debe haber tantos documentos como piezas.
7. Avisale a Manuel con el link del tablero y 3 líneas: cantidad de piezas, salidas vendidas y lo que quedó "a decidir".

# Revisá el tablero

1. `ArtifactData` `query` en `piezas` con `estado == "cambios"`.
2. Para cada una, aplicá el `comentario` con el agente que corresponda, regenerá los archivos, subí los assets nuevos y hacé `update` con `assets`, `texto`/`titulo` si cambiaron, `version + 1`, `estado: "pendiente"` y `comentario: ""`.
3. Si todo está `aprobada` o `descartada`, avisale a Manuel que ya se puede publicar día por día con "publicá lo de hoy" (o descargar y programar en Meta Business Suite), y recordale que el MP4 final de cada reel está en `meses/AAAA-MM/finales/`.

# Publicá lo de hoy

Manuel lo pide en el chat ("publicá lo de hoy", "publicá el post del 13"). La API de Instagram no programa: se publica en el momento.

1. `ArtifactData` `query` en `piezas` con la fecha pedida. Solo sirven las piezas con `estado == "aprobada"`; las demás se nombran y se saltean.
2. Si la pieza es de venta (`salida_id` de una salida no especial), volvé a mirar hoy la web del operador: cupo, fecha y precio. Si algo cambió o no se puede confirmar, no se publica y se avisa.
3. Mostrale a Manuel, por pieza: formato, título, texto completo con hashtags y las imágenes (`SendUserFile`). Esperá un "sí" explícito para esas piezas. Una confirmación vale solo para lo que se mostró.
4. Publicá con Composio (toolkit `instagram`; `COMPOSIO_SEARCH_TOOLS` da el plan):
   - Post: `INSTAGRAM_POST_IG_USER_MEDIA` con la imagen en JPEG (convertir el PNG) y el `caption` = texto + hashtags; después `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`.
   - Carrusel: un contenedor por lámina con `is_carousel_item: true`, después `INSTAGRAM_CREATE_CAROUSEL_CONTAINER` y publish del contenedor padre.
   - Reel: el MP4 de `finales/` con `media_type: "REELS"`, `share_to_feed: true` y la portada como `cover_url`; `max_wait_seconds` 300.
   - Historias: una por placa con `media_type: "STORIES"`. La API no pone stickers (enlace, encuesta, música): las historias que los necesitan las sube Bettina desde el celular, y se le avisa a Manuel.
5. Con `INSTAGRAM_GET_IG_MEDIA` tomá el `permalink`, y hacé `update` de la pieza en el tablero con `publicado: {fecha, permalink}` (el `estado` queda `aprobada`: el tablero no conoce otro). Antes de publicar, si la pieza ya tiene `publicado`, no se vuelve a publicar. Pasale los links a Manuel.

# Publicación automática

Desde el 01/11/2026 Manuel no confirma pieza por pieza: lo `aprobada` en el tablero se publica solo. Lo hace la tarea programada "Publicar lo aprobado" (corre 8 min antes de cada horario: 08:52, 09:52, 10:52, 12:52, 18:52 y 19:52, hora de Argentina), con los mismos pasos de "Publicá lo de hoy" salvo el 3 (no se espera el "sí"), y con estas reglas:

1. Se toman las piezas de hoy con `estado == "aprobada"`, sin `publicado` ni `aviso_publicacion`, y con `hora` hasta 20 minutos después de ahora.
2. El caption es el `texto` hasta la línea `———` (la "Nota de producción" nunca se publica) más los `hashtags`.
3. Las imágenes se bajan del tablero (Artifact `read` con el id del asset), se pasan a JPEG en `publicar/<id>/NN.jpg`, se hace commit y push, y se publican con la URL `https://raw.githubusercontent.com/manucastellano/viajarengrupoautomatizacion/<sha del commit>/publicar/<id>/NN.jpg`.
4. Se saltean y se avisa (campo `aviso_publicacion` en la pieza + notificación):
   - historias cuya nota pide sticker (encuesta, enlace, música) o compartir otra publicación: se publican solo las placas que no lo necesitan y Bettina sube el resto desde el celular;
   - reels sin el MP4 final entre los assets;
   - posts de la página de LinkedIn (falta la app de Community Management);
   - piezas de venta de salidas no especiales cuyo precio en `public.salidas` (proyecto Lovable) no coincida o tenga `verificado_en` de más de 15 días.
5. Al publicar: `publicado: {fecha, permalink}` en la pieza.
