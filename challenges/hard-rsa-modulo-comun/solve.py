# Solución de referencia: hard-rsa-modulo-comun
# Ataque: Common Modulus Attack
#
# Si gcd(e1, e2) = 1, el Algoritmo de Euclides Extendido encuentra a, b tal que:
#   a*e1 + b*e2 = 1
# Entonces:
#   m = c1^a * c2^b  (mod n)
# Si a < 0: c1^a = modinv(c1, n)^(-a)
# Si b < 0: c2^b = modinv(c2, n)^(-b)

from Crypto.Util.number import long_to_bytes

# ── Pega aquí los valores de intercepted.txt ───────────────────────────────
n  = 0  # reemplazar
e1 = 3
c1 = 0  # reemplazar
e2 = 65537
c2 = 0  # reemplazar
# ───────────────────────────────────────────────────────────────────────────


def extended_gcd(a, b):
    """Versión iterativa — evita stack overflow con e2 = 65537."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t  # gcd, coef_a, coef_b


def modinv(a, m):
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError("No existe inverso modular")
    return x % m


g, a, b = extended_gcd(e1, e2)
assert g == 1, "gcd(e1, e2) != 1 — el ataque no aplica directamente"

if a < 0:
    base1 = modinv(c1, n)
    a = -a
else:
    base1 = c1

if b < 0:
    base2 = modinv(c2, n)
    b = -b
else:
    base2 = c2

m = (pow(base1, a, n) * pow(base2, b, n)) % n
flag = long_to_bytes(m).decode(errors='replace')
print(f"[+] Flag: {flag}")
