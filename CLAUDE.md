# Community Manager VEG

Sistema de contenido de Instagram para Viajar en Grupo (@viajar.en.grupo).

- Manual de marca: https://claude.ai/artifact/PtTQiusa72f1hrbhu3Jy7J. Leé su `project/README.md` antes de escribir o diseñar.
- Especificación: docs/specs/2026-10-15-community-manager-veg-design.md
- Comando de trabajo: "armá <mes>" (skill `arma-mes`). "revisá el tablero" aplica los pedidos de cambio.
- Python: `.venv/Scripts/python`. Tests: `.venv/Scripts/python -m pytest -m "not lento"` (rápidos) y `-m lento` (render y video).
- Publicar en Instagram (Composio, cuenta @viajar.en.grupo) solo piezas `aprobada` en el tablero y solo después de que Manuel lo confirme en el chat para esas piezas puntuales ("publicá lo de hoy", sección del skill `arma-mes`). Nunca publicar por iniciativa propia ni desde una tarea programada.
- Nunca inventar precios, fechas ni cupos: si no están verificados hoy, la pieza no es de venta.
