# Investigador

Tu tarea: producir `meses/<AAAA-MM>/salidas.json` (lista de `Salida`, ver `veg/modelos.py`) con TODAS las salidas publicadas hoy.

1. Leé https://www.viajarengrupo.tur.ar/ y https://www.viajarengrupo.tur.ar/salidas. Por cada salida tomá: destino, fecha de salida (y regreso si está), duración, precio desde, base, suplemento single, operador y URL.
2. Por cada salida de operador, abrí la web pública del mayorista y confirmá fecha, precio y cupo. Valores de `cupo`: `disponible`, `ultimos` (si dice "últimos lugares" o similar), `agotado`, `sin_verificar` (no se pudo confirmar).
3. `verificado_en` = la fecha de hoy solo si confirmaste el cupo hoy.
4. `especial: true` solo para salidas propias acompañadas (hoy: Norte de España 24/05–10/06/2027 con Bettina, y The Beatle Experience 25/08–04/09/2027 con Alejandra Peñalva y Mirna Cappiello; esta última todavía sin precio: `precio_desde: null` hasta que la agencia lo confirme). Nunca para paquetes de mayorista.
5. Precio "a consultar" → `precio_desde: null`. Nunca estimes un precio.
6. Guardá con `veg.modelos.guardar`. Al final, informá en 5 líneas qué salidas quedaron vendibles y cuáles no se pudieron verificar y por qué.
