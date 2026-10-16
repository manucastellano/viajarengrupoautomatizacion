# Estratega

Entrada: `meses/<AAAA-MM>/salidas.json`. Salida: `meses/<AAAA-MM>/calendario.json` y `meses/<AAAA-MM>/material.md`.

1. Generá la base: `armar_calendario(anio, mes, cargar_salidas(...), hoy)` y guardala con `guardar`.
2. Completá `tema` de cada pieza:
   - especial/paquete: el ángulo concreto de la salida (ej. "Bodegas de La Rioja", "Cupos para Mercadillos").
   - destino: un destino que vendemos, sin repetir en el mes.
   - educativo: un tema útil (documentación, seguro, valija, mitos de viajar en grupo, cómo es una charla informativa).
   - agencia: Bettina, la oficina, un testimonio o el recap de un viaje reciente.
   - historias: mantené el tema del día y agregá el detalle (qué encuesta, qué tip).
   - Salidas que parten dentro del mes: usá historias de "¡salimos!" y dejá anotado un recap para el mes siguiente.
3. Escribí `material.md` para Manuel: por pieza, qué fotos o clips hacen falta, en lenguaje simple ("8 a 12 clips del grupo en Verona, de 3 a 10 segundos cada uno"). Al final, la lista de guiones de 3 líneas para las historias de los jueves.
