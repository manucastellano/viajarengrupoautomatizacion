# Diseñador

Entrada: `piezas.json`, `material/`. Salida: PNG en `meses/<AAAA-MM>/piezas/<id>/`.

- Post de venta (especial, paquete) → `post_paquete` con `letra_chica` = base + suplemento + `LETRA_CHICA_VENTA`.
- Post de agencia → `lamina` con `oscuro: true`, `etiqueta` "Viajar en Grupo" y el titular.
- Carrusel → `lamina`: portada (`numero` vacío, `oscuro: true`) + de 4 a 7 láminas (`numero` 1..n, `oscuro: false`) + lámina final con CTA.
- Historias → `historia`, una por línea del texto.
- Reel → `portada_reel` y `placa_cierre` (frase según el pilar: "¿Nos acompañás?", "Sumate a la charla", "Reservá tu lugar").
- Fotos: elegí de `material/` la mejor según el orden del manual (grupo real > Bettina > paisaje > detalle). Sin foto propia: stock libre de derechos (anotá la fuente en `piezas/<id>/fuentes.txt`) o fondo liso.
- Mirá cada PNG con Read antes de darlo por terminado: texto dentro de los márgenes, nada tapado.
