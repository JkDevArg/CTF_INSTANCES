# hard-misc-esoteric

**Categoria:** Misc  
**Dificultad:** Hard  
**Puerto:** 80 (descarga de archivos)

## Descripcion

Reto de codificacion multi-capa. La flag fue procesada secuencialmente con tres transformaciones:

1. **Base64** — encode de la flag
2. **Brainfuck** — generacion de codigo BF que imprime el string base64
3. **ROT47** — rotacion de 47 posiciones del codigo BF

La transmision resultante esta disponible para descarga. El jugador debe revertir las tres capas en orden inverso.

## Capas

```
FLAG
  -> base64_encode -> "Q1RGe..."
  -> to_brainfuck  -> "++++++++...+."
  -> rot47         -> transmision.txt (lo que ves)
```

## Solucion resumida

1. Aplicar ROT47 a `transmission.txt` (ROT47 es simetrico) -> codigo Brainfuck
2. Ejecutar el codigo Brainfuck -> string en base64
3. Decodificar base64 -> FLAG

## Setup local

```bash
docker-compose up --build
# Descargar transmission.txt desde http://localhost/download/transmission.txt
python3 solve.py
```

## Archivos

- `app/build.py` — genera la transmision codificada
- `app/server.py` — pagina informativa con enlaces de descarga
- `solve.py` — solucion completa con explicacion
