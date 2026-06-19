#!/usr/bin/env python3
"""
Solución: easy-osint-robots
Lee robots.txt, encuentra rutas ocultas, accede al vault.
"""
import sys
import re
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

print(f"[*] Leyendo robots.txt en {BASE} ...")
r = requests.get(f'{BASE}/robots.txt')
print(r.text)

# Extraer rutas Disallow
paths = re.findall(r'Disallow:\s*(.+)', r.text)
print(f"[*] Rutas ocultas encontradas: {paths}")

# Probar cada ruta
for path in paths:
    url = BASE + path.rstrip('/') + '/'
    resp = requests.get(url)
    if resp.status_code == 200:
        print(f"\n[+] Ruta accesible: {url}")
        # Buscar flag en el contenido
        import re as re2
        flags = re2.findall(r'CTF\{[^}]+\}', resp.text)
        if flags:
            print(f"[+] FLAG: {flags[0]}")
            break
        else:
            print(f"[*] Contenido (primeros 200 chars): {resp.text[:200]}")
