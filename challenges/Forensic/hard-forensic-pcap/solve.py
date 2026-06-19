#!/usr/bin/env python3
"""
Solución para hard-forensic-pcap.

Busca las dos partes de la flag en el tráfico HTTP:
  - Parte 1: parámetro GET ?token=<parte1>
  - Parte 2: campo JSON "session_data": "<parte2>"

Uso:
  python3 solve.py [capture.log]
"""
import re
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'capture.log'

try:
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
except FileNotFoundError:
    print(f"[-] Archivo no encontrado: {filename}")
    print("[*] Descarga capture.log del servidor primero.")
    sys.exit(1)

# Parte 1: parámetro token en GET request
m1 = re.search(r'[?&]token=([^\s&\r\n]+)', content)

# Parte 2: session_data en respuesta JSON
m2 = re.search(r'"session_data":\s*"([^"]+)"', content)

if m1 and m2:
    part1 = m1.group(1)
    part2 = m2.group(1)
    flag  = part1 + part2
    print(f'[+] Parte 1 (GET ?token=): {part1}')
    print(f'[+] Parte 2 (JSON session_data): {part2}')
    print(f'\n[+] FLAG: {flag}')
else:
    print('[-] No se encontraron todas las partes de la flag.')
    if m1:
        print(f'[*] Parte 1 encontrada: {m1.group(1)}')
    else:
        print('[-] Parte 1 NO encontrada — busca: ?token=...')
    if m2:
        print(f'[*] Parte 2 encontrada: {m2.group(1)}')
    else:
        print('[-] Parte 2 NO encontrada — busca: "session_data": "..."')
