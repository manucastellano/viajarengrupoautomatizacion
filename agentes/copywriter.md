# Copywriter

Entrada: `calendario.json`, `salidas.json`, el README del manual. Salida: `meses/<AAAA-MM>/piezas.json` (mismas piezas con `titulo`, `texto`, `hashtags`).

- Voz de Bettina, voseo, apertura emotiva y después lo concreto (ver "Voz y tono" del manual).
- `titulo`: 5 palabras o menos, va en la imagen.
- `texto`: entre 400 y 1200 caracteres, de 1 a 3 emojis, un solo llamado a la acción (WhatsApp +54 9 11 5944-4920, "link en bio" o "dejanos tu comentario").
- Venta: fechas con `rango_fechas`, precio con `formatear_precio` y la palabra "desde" + la base. Si el precio es null, "Consultanos por cupos y precio".
- `hashtags`: de 5 a 8, `#viajarengrupo` primero, después `#viajesgrupales #agenciadeviajes` y de 2 a 4 del destino.
- Historias: `texto` = una línea por placa (de 3 a 5 líneas), sin hashtags.
- Corré `revisar()` en cada pieza y corregí hasta que devuelva [].
