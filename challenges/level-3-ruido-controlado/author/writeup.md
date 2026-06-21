# Writeup — ruido_controlado

## Idea

La flag está en LSB del canal rojo, pero no en orden lineal. El orden de lectura depende de una permutación pseudoaleatoria basada en `sha256("mate" + width + height)`.

## Pipeline

1. `flag -> zlib.compress`
2. `MAGIC + LEN + compressed + CRC32`
3. XOR stream con bloques SHA256
4. Inserción bit a bit en LSB rojo usando índice permutado

## Resolución esperada

1. Leer `nota.txt`.
2. Derivar la key con las dimensiones reales de `ruido.png`.
3. Reconstruir la misma permutación.
4. Extraer bits del canal rojo.
5. Reagrupar en bytes.
6. Aplicar el mismo XOR stream.
7. Validar `MAGIC`, longitud y CRC.
8. Descomprimir y obtener la flag.
