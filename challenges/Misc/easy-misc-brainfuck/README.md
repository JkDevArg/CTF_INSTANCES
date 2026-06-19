# easy-misc-brainfuck — BrainMatic

## Descripción
El servidor genera un programa en Brainfuck que al ejecutarse imprime el FLAG. También se provee un intérprete Python (`bf.py`) para que el jugador no tenga que instalar nada adicional.

## Mecánica
- `build.py` convierte cada carácter del FLAG en una secuencia BF usando un patrón de multiplicación eficiente.
- Se generan dos archivos en `dist/`:
  - `program.bf`: el programa Brainfuck con el FLAG "codificado"
  - `bf.py`: intérprete Python 3 de Brainfuck

## Cómo resolver

### Opción A — Con el intérprete incluido
```bash
# Descarga ambos archivos del servidor
python3 bf.py program.bf
```

### Opción B — Interprete inline en Python
Ver `solve.py` incluido en este directorio.

### Opción C — Herramientas online
Sube el contenido de `program.bf` a:
- https://brainfuck.online/
- https://copy.sh/brainfuck/

## Notas técnicas
El código BF generado usa celdas de 8 bits (módulo 256) y 30 000 celdas de tape.
La estrategia de codificación es: para cada carácter con valor ASCII `n`, se calcula
`d ≈ sqrt(n)` y se genera `+d[->`+`q`+`<]>+r.[−]<` que calcula `d*q+r = n` eficientemente.

## Dificultad
Fácil — el jugador solo necesita ejecutar el programa con el intérprete provisto.
