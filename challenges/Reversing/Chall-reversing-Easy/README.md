# OverUma

| Field      | Value                        |
|------------|------------------------------|
| Category   | Reversing                    |
| Difficulty | Easy                         |
| Docker     | Yes                          |
| Port       | 80 (host default: 8080)      |

## Description

El equipo de respuesta a incidentes detectó un binario proveniente de una dirección catalogada como maliciosa de una APT peruana. El análisis dinámico no revela nada. Necesitas ir más profundo.

Un binario Windows x86 PE. Los jugadores deben revertirlo estáticamente para encontrar la dirección IP del servidor C2 embebida en el binario. Formato de flag: `H4L{IP_ADDRESS}`.

## Files

| File          | Description                          |
|---------------|--------------------------------------|
| `OverUma.exe` | Binario Windows x86 PE (49,664 bytes)|

Note: the flag is static — baked into the pre-compiled binary. The FLAG env var is not used during build.

## Vulnerability / Solution

1. Descargar `OverUma.exe`.
2. Analizar las cadenas de texto: `strings OverUma.exe` o usar Ghidra/IDA.
3. Buscar cadenas con formato de IP address.
4. La IP del servidor C2 es la flag: `H4L{<IP>}`.

## How to run

```bash
# Build and start
docker compose up --build -d

# Access
http://localhost:8080

# Stop
docker compose down
```
