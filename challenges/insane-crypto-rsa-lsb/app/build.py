import os, json
from math import gcd
from Crypto.Util.number import getPrime, bytes_to_long, inverse

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

bits = 512
while True:
    p   = getPrime(bits)
    q   = getPrime(bits)
    n   = p * q
    e   = 65537
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) == 1:
        break

d = inverse(e, phi)
m = bytes_to_long(FLAG.encode())
assert m < n, "FLAG demasiado larga para el modulo RSA de 512 bits"
c = pow(m, e, n)

# Guardar clave completa para el oraculo (solo el servidor la lee)
key_data = {'n': n, 'e': e, 'd': d, 'c': c}
with open('/tmp/rsa_lsb_key.json', 'w') as f:
    json.dump(key_data, f)

os.makedirs('dist', exist_ok=True)
pub_data = {
    'n':      n,
    'e':      e,
    'c':      c,
    'oracle': 'POST /oracle {"c": <decimal>} → {"lsb": 0 o 1}'
}
with open('dist/params.json', 'w') as f:
    json.dump(pub_data, f, indent=2)
