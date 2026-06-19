import os
from Crypto.Util.number import getPrime, bytes_to_long
from math import gcd

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

e = 3
m = bytes_to_long(FLAG.encode())

# Generate 2048-bit RSA modulus; ensure gcd(e, phi) = 1
while True:
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) == 1:
        break

# Since FLAG is short (~30-50 bytes = ~400 bits), m^3 << n (2048 bits).
# The modular reduction does NOT apply: c = m^3 exactly.
c = pow(m, e, n)

os.makedirs('dist', exist_ok=True)
with open('dist/rsa_data.txt', 'w') as f:
    f.write("# RSA — Parámetros públicos\n\n")
    f.write(f"n = {n}\n\n")
    f.write(f"e = {e}\n\n")
    f.write(f"c = {c}\n")

print(f"[build] rsa_data.txt generado (m={len(FLAG)} chars, e={e})")
