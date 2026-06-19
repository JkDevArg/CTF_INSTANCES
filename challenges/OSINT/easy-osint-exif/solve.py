#!/usr/bin/env python3
"""
Solución: easy-osint-exif
Extrae el FLAG del campo Comment en los metadatos PNG.
"""
import sys
import requests
from PIL import Image
import io

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

print(f"[*] Descargando imagen desde {BASE}/foto ...")
r = requests.get(f'{BASE}/foto')
if r.status_code != 200:
    print(f"[!] Error: HTTP {r.status_code}")
    sys.exit(1)

img = Image.open(io.BytesIO(r.content))
meta = img.info
print(f"[*] Metadatos encontrados: {list(meta.keys())}")

flag = meta.get('Comment', 'no encontrado')
print(f"[+] FLAG: {flag}")
# Alternativa con exiftool (desde terminal):
# curl -o summit_2024.png http://localhost:8080/foto
# exiftool summit_2024.png | grep Comment
