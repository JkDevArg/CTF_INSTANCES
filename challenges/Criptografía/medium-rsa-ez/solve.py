# Solución de referencia: medium-rsa-ez
# Ataque: Small Public Exponent (e=3) — Raíz cúbica entera
#
# Como el mensaje m es corto (~30-50 bytes) y n es de 2048 bits,
# se cumple que m^3 < n, por lo que c = m^3 (sin reducción modular).
# La solución es simplemente calcular la raíz cúbica entera de c.

from Crypto.Util.number import long_to_bytes

# ── Pega aquí los valores de rsa_data.txt ──────────────────────────────────
n = 0  # reemplazar
e = 3
c = 0  # reemplazar
# ───────────────────────────────────────────────────────────────────────────


def iroot(n, k):
    """Raíz k-ésima entera exacta de n usando búsqueda binaria."""
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if k == 1:
        return n, True
    lo, hi = 0, min(n, 1 << ((n.bit_length() + k - 1) // k + 1))
    while lo < hi:
        mid = (lo + hi + 1) >> 1
        if mid ** k <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo, lo ** k == n


m, exact = iroot(c, e)

if not exact:
    print("[!] c no es un cubo perfecto — verifica los valores.")
else:
    flag = long_to_bytes(m).decode(errors='replace')
    print(f"[+] Flag: {flag}")
