#!/usr/bin/env python3
"""
RSA LSB Oracle Attack.

Propiedad RSA: Enc(2) * Enc(m) mod n = Enc(2m mod n)

En cada iteracion multiplicamos el ciphertext por Enc(2).
El oraculo nos dice si el nuevo plaintext es par o impar.
Eso nos permite hacer busqueda binaria sobre el valor de m.

Complejidad: O(log n) consultas = n.bit_length() iteraciones

Uso: python3 solve.py [URL_BASE]
     Por defecto: http://localhost:8080
"""
import sys, requests, json
from Crypto.Util.number import long_to_bytes

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:8080'

print(f"[*] Target: {BASE}")

r      = requests.get(f'{BASE}/download/params.json')
params = json.loads(r.content)
n      = params['n']
e      = params['e']
c_orig = params['c']

print(f"[*] n ({n.bit_length()} bits): {str(n)[:40]}...")
print(f"[*] e: {e}")
print(f"[*] c: {str(c_orig)[:40]}...")


def oracle(c: int) -> int:
    """Consulta al oraculo: devuelve el LSB del descifrado de c."""
    r = requests.post(f'{BASE}/oracle', json={'c': c})
    return r.json()['lsb']


# f = Enc(2) = 2^e mod n (por homomorficidad: f*c = Enc(2*m))
f    = pow(2, e, n)
bits = n.bit_length()

lo, hi = 0, n
c      = c_orig

print(f"[*] Iniciando ataque LSB Oracle ({bits} iteraciones)...")
print(f"[*] Esto realizara {bits} peticiones al oraculo...")

for i in range(bits):
    c   = (c * f) % n
    lsb = oracle(c)
    mid = (lo + hi) // 2

    # lsb == 1 → 2^(i+1)*m mod n es impar → m esta en la mitad superior
    # lsb == 0 → 2^(i+1)*m mod n es par   → m esta en la mitad inferior
    if lsb == 1:
        lo = mid
    else:
        hi = mid

    if i % 64 == 0:
        print(f"  [{i:4d}/{bits}] rango actual: {hi - lo} ({(hi-lo).bit_length()} bits)")

# Al final, hi == m (o muy cercano por aritmetica entera)
m = hi
try:
    flag = long_to_bytes(m).decode()
    print(f"\n[+] FLAG: {flag}")
except Exception:
    # Probar hi y hi-1 por si hay error de redondeo de 1
    for candidate in [hi, hi - 1, lo, lo + 1]:
        try:
            flag = long_to_bytes(candidate).decode()
            if flag.startswith('CTF{'):
                print(f"\n[+] FLAG: {flag}")
                break
        except Exception:
            continue
    else:
        print(f"\n[?] Bytes recuperados (puede necesitar ajuste): {long_to_bytes(m)}")
