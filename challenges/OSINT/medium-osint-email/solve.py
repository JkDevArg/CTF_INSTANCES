#!/usr/bin/env python3
"""
Solución: medium-osint-email
Descarga el .eml, parsea headers, decodifica X-Correlation-ID en base64.
"""
import sys
import base64
import email
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

print(f"[*] Descargando email desde {BASE}/email ...")
r = requests.get(f'{BASE}/email')
if r.status_code != 200:
    print(f"[!] Error: HTTP {r.status_code}")
    sys.exit(1)

# Parsear el email
msg = email.message_from_bytes(r.content)

print(f"\n[*] Headers del email:")
for key, value in msg.items():
    print(f"    {key}: {value}")

# Encontrar y decodificar X-Correlation-ID
correlation_id = msg.get('X-Correlation-ID')
if correlation_id:
    print(f"\n[+] X-Correlation-ID (base64): {correlation_id}")
    try:
        decoded = base64.b64decode(correlation_id).decode('utf-8')
        print(f"[+] FLAG: {decoded}")
    except Exception as e:
        print(f"[!] Error decodificando: {e}")
else:
    print("[!] Header X-Correlation-ID no encontrado")
