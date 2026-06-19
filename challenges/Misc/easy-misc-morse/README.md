# easy-misc-morse — Estación Alfa-7

## Descripción
El servidor genera un archivo `signal.txt` que contiene el FLAG codificado en código Morse internacional. El jugador debe descifrar la señal para obtener la flag.

## Mecánica
- `build.py` toma el FLAG del entorno y lo convierte a Morse carácter por carácter.
- Los caracteres se separan por un espacio, las palabras (si las hubiera) por `/`.
- El archivo `signal.txt` se sirve para descarga vía Flask.

## Tabla de caracteres especiales utilizados
| Carácter | Morse     |
|----------|-----------|
| `{`      | `-.--.-`  |
| `}`      | `-.--.`   |
| `_`      | `..--.-`  |
| `-`      | `-....-`  |

## Solución rápida
Descarga `signal.txt`, extrae la línea de Morse y decodifícala con cualquier herramienta:
- Online: https://morsecode.world/international/translator.html
- Python: ver `solve.py` incluido en este directorio.

## Dificultad
Fácil — el jugador solo necesita conocer (o buscar) el alfabeto Morse y decodificar la cadena.
