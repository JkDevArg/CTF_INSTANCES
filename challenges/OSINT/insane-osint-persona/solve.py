#!/usr/bin/env python3
"""
Solucion: insane-osint-persona -- Project TURING
Cadena: News -> LinkedIn -> GitLab profile -> GitLab repo -> Paste -> decode ROT13+base64 -> FLAG
"""
import sys
import re
import base64
import codecs
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

# Paso 1: News page
print(f"[*] Paso 1: Leyendo articulo de noticias en {BASE} ...")
r1 = requests.get(BASE)
linkedin_links = re.findall(r'href="(/linkedin/[^"]+)"', r1.text)
print(f"[+] Perfil LinkedIn encontrado: {linkedin_links}")

# Paso 2: LinkedIn
linkedin_url = BASE + (linkedin_links[0] if linkedin_links else '/linkedin/alex-turing')
print(f"\n[*] Paso 2: Analizando perfil LinkedIn: {linkedin_url} ...")
r2 = requests.get(linkedin_url)
gitlab_links = re.findall(r'href="(/gitlab/[^"]+)"', r2.text)
# Buscar pista de cifrado
rot_clue = 'ROT' in r2.text
print(f"[+] Links GitLab encontrados: {gitlab_links}")
print(f"[+] Pista de cifrado ROT encontrada: {rot_clue}")

# Paso 3: GitLab profile -> encontrar repo
gitlab_profile_url = BASE + (gitlab_links[0] if gitlab_links else '/gitlab/a_turing')
print(f"\n[*] Paso 3: Explorando perfil GitLab: {gitlab_profile_url} ...")
r3 = requests.get(gitlab_profile_url)
repo_links = re.findall(r'href="(/gitlab/a_turing/[^"]+)"', r3.text)
print(f"[+] Repositorios: {repo_links}")

# Paso 4: GitLab repo README -> encontrar paste
backup_repo_url = BASE + '/gitlab/a_turing/personal-backup'
print(f"\n[*] Paso 4: Leyendo README de {backup_repo_url} ...")
r4 = requests.get(backup_repo_url)
paste_links = re.findall(r'href="(/paste/[^"]+)"', r4.text)
print(f"[+] Links a paste: {paste_links}")

# Paso 5: Paste con flag codificada
paste_url = BASE + (paste_links[0] if paste_links else '/paste/b4ckup_2024')
print(f"\n[*] Paso 5: Accediendo al paste: {paste_url} ...")
r5 = requests.get(paste_url)

# Extraer contenido del div.content
content_match = re.search(r'class="content">([^<]+)<', r5.text)
if content_match:
    encoded = content_match.group(1).strip()
    print(f"[+] Contenido codificado (ROT13 de base64): {encoded}")

    # Decodificar: ROT13 primero -> base64
    b64 = codecs.decode(encoded, 'rot13')
    print(f"[+] Despues de ROT13: {b64}")

    try:
        flag = base64.b64decode(b64).decode('utf-8')
        print(f"\n[+] FLAG: {flag}")
    except Exception as e:
        print(f"[!] Error en base64: {e}")
        # Intentar con padding
        padding = 4 - len(b64) % 4
        if padding != 4:
            b64_padded = b64 + '=' * padding
            flag = base64.b64decode(b64_padded).decode('utf-8')
            print(f"\n[+] FLAG (con padding): {flag}")
else:
    print("[!] No se encontro contenido codificado en el paste")
    # Fallback: buscar CTF{ directamente
    flags = re.findall(r'CTF\{[^}]+\}', r5.text)
    if flags:
        print(f"[+] FLAG: {flags[0]}")
