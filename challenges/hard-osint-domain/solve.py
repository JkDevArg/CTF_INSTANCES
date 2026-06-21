#!/usr/bin/env python3
"""
Solución: hard-osint-domain
Obtiene la mitad del FLAG de WHOIS y la otra mitad del CT Log.
Decodifica base64 y concatena para obtener el FLAG completo.
"""
import sys
import re
import base64
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'
DOMAIN = 'corpcorp.local'

# Paso 1: WHOIS — extraer email del registrante (contiene half1 en base64)
print(f"[*] Consultando WHOIS para {DOMAIN} ...")
r1 = requests.get(f'{BASE}/whois', params={'domain': DOMAIN})

# El email del registrante tiene formato: BASE64_HALF1@corpcorp.local
email_match = re.search(r'Registrant Email.*?<span class="value">([^@]+)@corpcorp\.local', r1.text)
if not email_match:
    # Fallback regex
    email_match = re.search(r'([A-Za-z0-9+/=]{10,})@corpcorp\.local', r1.text)

if email_match:
    half1_b64 = email_match.group(1)
    print(f"[+] Registrant Email (base64): {half1_b64}")
    try:
        half1 = base64.b64decode(half1_b64).decode('utf-8')
        print(f"[+] Primera mitad: {half1}")
    except Exception as e:
        print(f"[!] Error decodificando half1: {e}")
        half1 = ''
else:
    print("[!] No se encontró email del registrante")
    half1 = ''

# Paso 2: CT Log — extraer SAN con half2 en base64
print(f"\n[*] Consultando CT Log para {DOMAIN} ...")
r2 = requests.get(f'{BASE}/ct-log', params={'domain': DOMAIN})

# El SAN del cert expirado tiene: BASE64_HALF2.internal.corpcorp.local
san_match = re.search(r'([A-Za-z0-9+/=]{10,})\.internal\.corpcorp\.local', r2.text)
if san_match:
    half2_b64 = san_match.group(1)
    print(f"[+] SAN (base64): {half2_b64}")
    try:
        half2 = base64.b64decode(half2_b64).decode('utf-8')
        print(f"[+] Segunda mitad: {half2}")
    except Exception as e:
        print(f"[!] Error decodificando half2: {e}")
        half2 = ''
else:
    print("[!] No se encontró SAN con datos codificados")
    half2 = ''

# Reconstruir FLAG
flag = half1 + half2
print(f"\n[+] FLAG: {flag}")
