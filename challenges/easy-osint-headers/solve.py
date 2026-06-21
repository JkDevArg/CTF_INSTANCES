#!/usr/bin/env python3
"""
Solucion: easy-osint-headers
Encuentra el FLAG en el header X-Internal-Token de la respuesta HTTP.
"""
import sys
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

print(f"[*] Inspeccionando headers de {BASE} ...")
r = requests.get(BASE)

print(f"\n[*] Headers de respuesta:")
for k, v in r.headers.items():
    print(f"    {k}: {v}")

flag = r.headers.get('X-Internal-Token', 'no encontrado')
print(f"\n[+] X-Internal-Token: {flag}")

# Alternativa con curl:
# curl -I http://localhost:8080/ | grep X-Internal-Token
