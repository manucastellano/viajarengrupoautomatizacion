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
3. Si todo está `aprobada` o `descartada`, avisale a Manuel que puede descargar y programar en Meta Business Suite, y recordale que el MP4 final de cada reel está en `meses/AAAA-MM/finales/`.
