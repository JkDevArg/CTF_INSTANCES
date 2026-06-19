#!/usr/bin/env python3
"""
Solución: medium-osint-archive
Explora el archivo histórico del sitio para encontrar páginas eliminadas con datos sensibles.
"""
import sys
import re
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

print(f"[*] Explorando sitio actual en {BASE} ...")
r0 = requests.get(BASE)
# Buscar link al archivo
archive_links = re.findall(r'href="(/archive/[^"]*)"', r0.text)
print(f"[*] Links de archivo en página principal: {archive_links}")

print(f"\n[*] Accediendo al índice del archivo ...")
r1 = requests.get(f'{BASE}/archive/')
# Extraer snapshots
snapshots = re.findall(r'href="(/archive/\d{{4}}-\d{{2}}/)"', r1.text)
print(f"[*] Snapshots encontrados: {snapshots}")

# Explorar cada snapshot
for snapshot in snapshots:
    url = BASE + snapshot
    r = requests.get(url)
    print(f"\n[*] Explorando {snapshot} ...")
    # Buscar links internos en cada snapshot
    sub_links = re.findall(r'href="(/archive/[^"]+)"', r.text)
    for link in sub_links:
        if link not in snapshots:
            sub_url = BASE + link
            print(f"    [*] Sub-página: {link}")
            sub_r = requests.get(sub_url)
            flags = re.findall(r'CTF\{[^}]+\}', sub_r.text)
            if flags:
                print(f"\n[+] FLAG encontrada en {link}: {flags[0]}")
                sys.exit(0)
            # Buscar cualquier dato sensible
            if 'api-key' in sub_r.text.lower() or 'eliminada' in sub_r.text.lower() or 'comprometida' in sub_r.text.lower():
                print(f"    [!] Página con datos sensibles encontrada: {link}")
                # Extraer el contenido del div api-key
                api_keys = re.findall(r'class="api-key"[^>]*>([^<]+)<', sub_r.text)
                if api_keys:
                    print(f"[+] FLAG: {api_keys[0].strip()}")
                    sys.exit(0)
