# Nivel 3 — ruido_controlado  - by p0mb3r0

**Dificultad:** Hard  
**Archivos entregados:** `ruido.png`, `nota.txt`

La flag tiene formato:

`H4L{...}`

## Descripción

La imagen parece ruido o una textura sin información útil a simple vista.
Pero no todo el ruido es azar.

Hay un mensaje escondido dentro de `ruido.png` y una pista en `nota.txt`.
La resolución requiere analizar cómo se recorren los píxeles, no solo inspeccionar la imagen de forma lineal.

## Reglas del reto

- Todo se resuelve localmente.
- No hace falta internet.
- No hay fuerza bruta pesada.
- No hay contraseñas externas imposibles.

## Pistas

1. No todo ruido es azar.
2. El camino no es lineal.
3. Las dimensiones importan.
4. Hay algo comprimido adentro.
5. Buscá una cabecera, no una flag directa.

## Objetivo didáctico

Este nivel busca que el jugador:

- detecte que hay ocultación en bits,
- use la pista para reconstruir un orden de lectura,
- procese un payload antes de obtener la flag,
- y valide resultados en vez de confiar en basura o decoys.
