#!/usr/bin/env python3
"""
Solucion: medium-osint-username
Sigue la cadena: GitHub -> ByteGram -> Twitter -> FLAG

Requiere: pip install requests beautifulsoup4
"""
import sys
import re
import codecs
import requests
from bs4 import BeautifulSoup

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'

# Paso 1: GitHub
print(f"[*] Paso 1: Accediendo a perfil GitHub en {BASE}/github/h4ck3r_jc ...")
r1 = requests.get(f'{BASE}/github/h4ck3r_jc')
soup1 = BeautifulSoup(r1.text, 'html.parser')
# Buscar link a ByteGram
link = soup1.find('a', href=re.compile(r'/bytegram/'))
if link:
    bytegram_url = BASE + link['href']
    print(f"[+] Link a ByteGram encontrado: {link['href']}")
else:
    bytegram_url = BASE + '/bytegram/jc_2024'
    print(f"[*] Usando ByteGram por defecto: /bytegram/jc_2024")

# Paso 2: ByteGram — ROT13 bio
print(f"\n[*] Paso 2: Accediendo a ByteGram ...")
r2 = requests.get(bytegram_url)
soup2 = BeautifulSoup(r2.text, 'html.parser')
encoded_el = soup2.find(class_='bio-encoded')
if encoded_el:
    encoded = encoded_el.text.strip()
    decoded = codecs.decode(encoded, 'rot13')
    print(f"[+] Bio codificada : {encoded}")
    print(f"[+] Bio decodificada (ROT13): {decoded}")
    # Extraer username de twitter
    m = re.search(r'username:\s*(\S+)', decoded)
    twitter_user = m.group(1) if m else 'elite_jc'
    print(f"[+] Twitter username: {twitter_user}")
else:
    twitter_user = 'elite_jc'
    print(f"[!] No se encontro .bio-encoded, usando username por defecto: {twitter_user}")

# Paso 3: Twitter — FLAG
print(f"\n[*] Paso 3: Accediendo a Twitter/@{twitter_user} ...")
r3 = requests.get(f'{BASE}/twitter/{twitter_user}')
flags = re.findall(r'CTF\{{[^}}]+\}}', r3.text)
if flags:
    print(f"\n[+] FLAG: {flags[0]}")
else:
    print("[!] Patron CTF{{}} no encontrado. Buscando .flag-tweet ...")
    soup3 = BeautifulSoup(r3.text, 'html.parser')
    flag_el = soup3.find(class_='flag-tweet')
    if flag_el:
        print(f"[+] Token: {flag_el.text.strip()}")
    else:
        print("[!] Flag no encontrada.")
