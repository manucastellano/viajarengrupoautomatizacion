# Editor de video

Entrada: la pieza `reel` de `piezas.json`, `material/`, la portada y la placa del diseñador. Salida: `meses/<AAAA-MM>/finales/<id>.mp4` y `meses/<AAAA-MM>/piezas/<id>/<id>-preview.mp4`.

1. Elegí de 10 a 25 tomas de `material/` para contar: gancho (lo más fuerte primero), desarrollo y dato concreto. Cada toma dura de 1,5 a 3 s (máximo 6 s si es Bettina hablando).
2. Subtítulos: de 4 a 8 en todo el reel, 2 líneas como máximo, que digan el dato o la emoción ("Ópera en la Arena de Verona", "Desde USD 9.680").
3. `armar_reel(tomas, portada, placa, carpeta=meses/<AAAA-MM>/finales, nombre=<id>)`; mové la preview a `piezas/<id>/`.
4. En `piezas/<id>/musica.txt` sugerí 2 temas de la biblioteca de Instagram por estilo (no se agrega música al MP4).
5. Extraé 3 fotogramas (segundo 2, mitad, final) con ffmpeg y miralos con Read: encuadre correcto y subtítulos legibles.
6. Tomas con sonido propio que se tiene que oír (Bettina hablando a cámara): `Toma(..., con_audio=True)`. Solo para clips que tienen audio; el resto queda en silencio para agregar música en Instagram.
