#!/usr/bin/env python3
"""
Genera el archivo de captura HTTP con la flag dividida en dos partes.
Se ejecuta al iniciar el contenedor con la FLAG real del entorno.
"""
import os
import sys

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# Dividir la flag en dos partes
mid   = len(FLAG) // 2
part1 = FLAG[:mid]
part2 = FLAG[mid:]

http_log = f"""GET /search?q=intruder+activity&token={part1} HTTP/1.1
Host: internal.corpsec.local
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml
Accept-Language: es-PE,es;q=0.9
Connection: keep-alive

HTTP/1.1 200 OK
Date: Mon, 15 Jan 2024 03:42:17 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
Content-Length: 312
X-Content-Type-Options: nosniff

<html>
<head><title>CorpSec Internal — Search</title></head>
<body>
<h1>Search Results</h1>
<p>No results found for query.</p>
<p><small>Session ID: a3f29b1c4d</small></p>
</body>
</html>

================================================================================

GET /api/v1/status HTTP/1.1
Host: internal.corpsec.local
User-Agent: CorpMonitor/3.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.Et9HFtf9R3GEMmf21DGmjQnfbXwjWzA7kmrxzm3rVCk
X-Forwarded-For: 10.0.1.42
Connection: keep-alive

HTTP/1.1 200 OK
Date: Mon, 15 Jan 2024 03:42:19 GMT
Server: nginx/1.18.0
Content-Type: application/json
Content-Length: 187
X-Powered-By: Express

{{
  "status": "operational",
  "services": 14,
  "alerts": 0,
  "debug_info": {{
    "session_data": "{part2}",
    "uptime_seconds": 99832,
    "last_check": "2024-01-15T03:42:19Z"
  }}
}}

================================================================================

POST /auth/logout HTTP/1.1
Host: internal.corpsec.local
Content-Type: application/x-www-form-urlencoded
Content-Length: 28
Cookie: session=a3f29b1c4d; csrf=7e9f2a

csrf_token=7e9f2a&confirm=1

HTTP/1.1 302 Found
Date: Mon, 15 Jan 2024 03:42:21 GMT
Location: /auth/login
Set-Cookie: session=; expires=Thu, 01 Jan 1970 00:00:00 GMT
Content-Length: 0

"""

os.makedirs('/app/dist', exist_ok=True)

with open('/app/dist/capture.log', 'w') as f:
    f.write("=== NetCapture Pro v2.3 — Follow HTTP Stream Export ===\n")
    f.write("Captura: 2024-01-15 03:42:17 UTC\n")
    f.write("Interfaz: eth0\n")
    f.write("Filtro: tcp port 80 and host internal.corpsec.local\n")
    f.write("Paquetes: 47 capturados, 47 mostrados\n")
    f.write("=" * 72 + "\n\n")
    f.write(http_log)

with open('/app/dist/README.txt', 'w') as f:
    f.write("CORPSEC INCIDENT RESPONSE — EVIDENCIA CAPTURADA\n")
    f.write("=" * 50 + "\n\n")
    f.write("Este archivo contiene el stream HTTP exportado desde Wireshark.\n")
    f.write("Captura tomada durante el incidente del 2024-01-15.\n\n")
    f.write("Analiza el trafico HTTP completo.\n")
    f.write("Los datos sensibles a veces se filtran en lugares inesperados.\n")
    f.write("La flag fue dividida en dos partes dentro del trafico.\n\n")
    f.write("Herramientas sugeridas: strings, grep, python\n")

print(f"[*] Archivo de captura generado: /app/dist/capture.log")
print(f"[*] Partes de flag: {len(part1)} + {len(part2)} chars")
sys.stdout.flush()
