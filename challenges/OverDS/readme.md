# OverDS

| Field      | Value                        |
|------------|------------------------------|
| Category   | Forensic                     |
| Difficulty | Easy                         |
| Docker     | Yes                          |
| Port       | 80 (host default: 8080)      |

## Description

Una imagen descargada de una fuente sospechosa. No parece peligrosa. Pero lo que contiene adentro podría sorprenderte.

Una ROM de Nintendo DS está embebida dentro de un archivo JPG mediante esteganografía de archivos concatenados. El jugador debe extraerla y ejecutarla en un emulador de DS para ver la flag.

## Files

| File                    | Description                                            |
|-------------------------|--------------------------------------------------------|
| `base/bajando_pepa.jpg` | JPG con ROM NDS embebida (9911 bytes) — se sirve este  |
| `bajando_pepa.jpg`      | JPG limpio de referencia (3807 bytes)                  |
| `base/over_ds.nds`      | ROM NDS extraída (referencia)                          |

## Vulnerability / Solution

1. Descargar `bajando_pepa.jpg` (el que sirve el servidor; contiene la ROM).
2. Analizar con `binwalk bajando_pepa.jpg` — detecta un NDS ROM embebido.
3. Extraer: `binwalk -e bajando_pepa.jpg`.
4. Abrir el `.nds` extraído con un emulador de Nintendo DS (ej. melonDS, DeSmuME).
5. La ROM muestra la flag en pantalla.

Note: the flag is static — baked into the pre-compiled ROM inside the JPG. The FLAG env var is not used during build.

## How to run

```bash
# Build and start
docker compose up --build -d

# Access
http://localhost:8080

# Stop
docker compose down
```
