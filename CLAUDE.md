# Community Manager VEG

Sistema de contenido de Instagram para Viajar en Grupo (@viajar.en.grupo).

- Manual de marca: https://claude.ai/artifact/PtTQiusa72f1hrbhu3Jy7J. Leé su `project/README.md` antes de escribir o diseñar.
- Especificación: docs/specs/2026-10-15-community-manager-veg-design.md
- Comando de trabajo: "armá <mes>" (skill `arma-mes`). "revisá el tablero" aplica los pedidos de cambio.
- Python: `.venv/Scripts/python`. Tests: `.venv/Scripts/python -m pytest -m "not lento"` (rápidos) y `-m lento` (render y video).
- Publicación automática (autorizada por Manuel el 01/11/2026): toda pieza `aprobada` en el tablero se publica sola en su fecha y hora con Composio (Instagram @viajar.en.grupo; LinkedIn solo cuenta "bettina", nunca "manuel-personal"), desde la tarea programada "Publicar lo aprobado" (sección "Publicación automática" del skill `arma-mes`). La aprobación en el tablero es la confirmación. Nunca se publica algo que no esté `aprobada`, ni dos veces la misma pieza, ni una pieza de venta cuyo precio no esté verificado en los últimos 15 días: esas se saltean y se le avisa a Manuel.
- Nunca inventar precios, fechas ni cupos: si no están verificados hoy, la pieza no es de venta.
