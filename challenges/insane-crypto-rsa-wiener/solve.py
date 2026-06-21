#!/usr/bin/env python3
"""
Wiener's Attack on RSA with small private exponent d.

Algoritmo:
  1. Calcular la expansion en fracciones continuas de e/n
  2. Para cada convergente k/d de la fraccion continua:
     - Si phi = (e*d - 1) / k es entero
     - Y las raices de x^2 - (n - phi + 1)x + n = 0 son enteras (p y q)
     - Entonces d es el exponente privado correcto

Uso: python3 solve.py [ruta_a_wiener.txt]
     Por defecto busca wiener.txt en el directorio actual.
"""
import sys, re
from Crypto.Util.number import long_to_bytes

FILENAME = sys.argv[1] if len(sys.argv) > 1 else 'wiener.txt'

with open(FILENAME) as f:
    content = f.read()

n = int(re.search(r'n = (\d+)', content).group(1))
e = int(re.search(r'e = (\d+)', content).group(1))
c = int(re.search(r'c = (\d+)', content).group(1))

print(f"[*] n = {n}")
print(f"[*] e = {e}")
print(f"[*] Ejecutando ataque de Wiener via fracciones continuas...")


def continued_fraction(num: int, den: int) -> list:
    """Calcula los coeficientes de la fraccion continua de num/den."""
    cf = []
    while den:
        cf.append(num // den)
        num, den = den, num % den
    return cf


def convergents(cf: list) -> list:
    """Calcula los convergentes a partir de los coeficientes de la fraccion continua."""
    convs = []
    h_prev, h_curr = 1, cf[0]
    k_prev, k_curr = 0, 1
    convs.append((h_curr, k_curr))
    for i in range(1, len(cf)):
        h_prev, h_curr = h_curr, cf[i] * h_curr + h_prev
        k_prev, k_curr = k_curr, cf[i] * k_curr + k_prev
        convs.append((h_curr, k_curr))
    return convs


def isqrt(n: int) -> int:
    """Raiz cuadrada entera exacta."""
    if n < 0:
        return -1
    x = int(n ** 0.5)
    # Ajustar por errores de punto flotante
    while x * x > n:
        x -= 1
    while (x + 1) * (x + 1) <= n:
        x += 1
    return x


cf    = continued_fraction(e, n)
convs = convergents(cf)

print(f"[*] Analizando {len(convs)} convergentes...")

found = False
for k, d in convs:
    if k == 0:
        continue
    if (e * d - 1) % k != 0:
        continue
    phi = (e * d - 1) // k
    if phi <= 0:
        continue

    # Verificar: p y q son raices de x^2 - (n - phi + 1)x + n = 0
    b            = n - phi + 1
    discriminant = b * b - 4 * n
    if discriminant < 0:
        continue
    sq = isqrt(discriminant)
    if sq * sq != discriminant:
        continue

    p = (b + sq) // 2
    q = (b - sq) // 2
    if p * q == n:
        print(f"[+] d encontrado: {d}")
        print(f"[+] k = {k}, phi = {phi}")
        print(f"[+] p = {p}")
        print(f"[+] q = {q}")
        m    = pow(c, d, n)
        flag = long_to_bytes(m).decode(errors='replace')
        print(f"\n[+] FLAG: {flag}")
        found = True
        break

if not found:
    print("[-] Ataque fallido. Verifica que d satisface la condicion de Wiener (d < n^0.25 / 3).")
