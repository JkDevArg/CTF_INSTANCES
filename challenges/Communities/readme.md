# Capas Ocultas

| Field      | Value                        |
|------------|------------------------------|
| Category   | Forensic                     |
| Difficulty | Easy                         |
| Docker     | Yes                          |
| Port       | 80 (host default: 8080)      |

## Description

Un archivo fue enviado como un simple ZIP. Pero las apariencias engañan. Cambia su extensión y mira con los ojos correctos.

El reto entrega `communities.zip`, que en realidad es un archivo Krita (`.kra`). Al renombrarlo y abrirlo con Krita, el jugador descubre una capa oculta que contiene la flag.

## Files

| File               | Description                          |
|--------------------|--------------------------------------|
| `communities.zip`  | Archivo Krita disfrazado de ZIP      |

## Vulnerability / Solution

1. Descargar `communities.zip`.
2. Renombrar a `communities.kra`.
3. Abrir con Krita.
4. Activar la visibilidad de todas las capas en el panel de capas.
5. La capa oculta revela la flag.

Note: the flag is static — baked into the pre-generated `communities.zip` file. The FLAG env var is not used during build.

## How to run

```bash
# Build and start
docker compose up --build -d

# Access
http://localhost:8080

# Stop
docker compose down
```
