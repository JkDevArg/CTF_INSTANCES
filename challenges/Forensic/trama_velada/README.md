# Trama Velada

| Field      | Value                        |
|------------|------------------------------|
| Category   | Forensic                     |
| Difficulty | Hard                         |
| Docker     | Yes                          |
| Port       | 80 (host default: 8080)      |

## Description

El tráfico fue capturado. El cifrado oculta su contenido. Pero las claves fueron recuperadas. Ahora depende de ti reconstruir lo que viajó por el cable.

PCAP con tráfico HTTPS cifrado con TLS 1.3. Se provee el keylog para descifrar en Wireshark. El payload HTTP contiene JSON comprimido con gzip; una segunda respuesta chunked trae un payload XOR-cifrado en base64.

## Files

| File           | Description                                         |
|----------------|-----------------------------------------------------|
| `traffic.pcap` | Captura de tráfico TLS 1.3 (3674 bytes)             |
| `keylog.txt`   | NSS keylog para descifrar sesiones TLS              |
| `solve.py`     | Script de solución de referencia (requiere tshark)  |
| `WRITEUP.md`   | Writeup detallado                                   |

## Vulnerability / Solution

1. Descargar `traffic.pcap` y `keylog.txt`.
2. En Wireshark: Edit > Preferences > Protocols > TLS > (Pre)-Master-Secret log filename → apuntar a `keylog.txt`.
3. Abrir `traffic.pcap` — el tráfico HTTPS aparece descifrado.
4. Seguir los flujos HTTP (Follow > HTTP Stream).
5. La primera respuesta es JSON gzip → contiene el seed.
6. La segunda respuesta (chunked) contiene el payload base64 → decodificar y aplicar XOR con el seed.
7. El resultado es la flag.

Note: the flag is static — está embebida en `traffic.pcap` y no depende de la variable de entorno FLAG.

## How to run

```bash
# Build and start
docker compose up --build -d

# Access
http://localhost:8080

# Stop
docker compose down
```
