import os
from Crypto.Util.number import getPrime, bytes_to_long
from math import gcd

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

e1, e2 = 3, 65537
m = bytes_to_long(FLAG.encode())

# Generate 2048-bit modulus shared between both encryptions
while True:
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e1, phi) == 1 and gcd(e2, phi) == 1:
        break

c1 = pow(m, e1, n)
c2 = pow(m, e2, n)

os.makedirs('dist', exist_ok=True)
with open('dist/intercepted.txt', 'w') as f:
    f.write("# Tráfico interceptado — Módulo RSA compartido\n\n")
    f.write("# Ambos mensajes cifran el mismo plaintext con el mismo módulo n.\n\n")
    f.write(f"n = {n}\n\n")
    f.write(f"e1 = {e1}\n")
    f.write(f"c1 = {c1}\n\n")
    f.write(f"e2 = {e2}\n")
    f.write(f"c2 = {c2}\n")

print(f"[build] intercepted.txt generado (m={len(FLAG)} chars)")
