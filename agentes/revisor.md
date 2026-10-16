# Revisor

Entrada: todo `meses/<AAAA-MM>/`. Salida: `meses/<AAAA-MM>/revision.md`.

1. Re-verificá hoy, en la web del mayorista, el cupo y el precio de cada salida usada en piezas de venta. Actualizá `salidas.json` (`verificado_en`, `cupo`, `precio_desde`).
2. Corré `revisar(pieza, salida, hoy)` en todas las piezas.
3. Mirá cada PNG y cada preview contra la checklist "Revisión antes de enviar a aprobación" del manual.
4. Las piezas con problemas vuelven al agente que las hizo, con el problema escrito. Repetí hasta que no queden problemas (máximo 2 vueltas; lo que siga mal se lista en `revision.md` como "a decidir por Manuel").
5. Si al re-verificar cambió el precio o el cupo de una salida, regenerá con el agente que corresponda las piezas que la usan (texto y PNG) antes de subirlas; `revisar` marca el precio desactualizado.
