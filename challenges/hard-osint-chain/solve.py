#!/usr/bin/env python3
"""
Solución: hard-osint-chain
Sigue la cadena: TechLeaks blog → GitHub commits → Paste hex → FLAG
"""
import sys
import re
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

# Paso 1: Blog principal
print(f"[*] Paso 1: Explorando TechLeaks en {BASE} ...")
r1 = requests.get(BASE)
blog_links = re.findall(r'href="(/blog/post/[^"]+)"', r1.text)
print(f"[+] Posts encontrados: {blog_links}")

# Paso 2: Post del blog
blog_url = BASE + (blog_links[0] if blog_links else '/blog/post/leaked-config')
print(f"\n[*] Paso 2: Leyendo post del blog: {blog_url} ...")
r2 = requests.get(blog_url)
github_links = re.findall(r'href="(/github/[^"]+)"', r2.text)
print(f"[+] Links de GitHub encontrados: {github_links}")

# Paso 3: Repositorio GitHub
github_url = BASE + (github_links[0] if github_links else '/github/corpcorp/configs')
print(f"\n[*] Paso 3: Revisando commits en {github_url} ...")
r3 = requests.get(github_url)
# Buscar referencia al paste en el texto del commit
paste_refs = re.findall(r'/paste/([a-zA-Z0-9]+)', r3.text)
paste_refs = list(set(paste_refs))
print(f"[+] Pastes referenciados en commits: {paste_refs}")

# Paso 4: Paste con FLAG hex
paste_id = paste_refs[0] if paste_refs else 'abc123'
paste_url = f"{BASE}/paste/{paste_id}"
print(f"\n[*] Paso 4: Accediendo a paste en {paste_url} ...")
r4 = requests.get(paste_url)

# Extraer hex del contenido
hex_match = re.search(r'class="content">([0-9a-f]+)<', r4.text)
if hex_match:
    hex_str = hex_match.group(1)
    print(f"[+] Token hex: {hex_str}")
    flag = bytes.fromhex(hex_str).decode('utf-8')
    print(f"\n[+] FLAG: {flag}")
else:
    # Fallback: buscar CTF{ directamente
    flags = re.findall(r'CTF\{[^}]+\}', r4.text)
    if flags:
        print(f"\n[+] FLAG: {flags[0]}")
    else:
        print("[!] No se encontró la flag")
        print(f"[*] Contenido del paste (primeros 500 chars):\n{r4.text[:500]}")
