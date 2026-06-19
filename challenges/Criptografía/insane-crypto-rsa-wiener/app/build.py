import os
from Crypto.Util.number import getPrime, bytes_to_long, inverse, GCD

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')


def gen_wiener_rsa(bits: int = 512):
    """
    Genera parametros RSA vulnerables al ataque de Wiener.
    Condicion de Wiener: d < n^0.25 / 3

    Estrategia:
      1. Generar p, q primos de `bits` bits
      2. Elegir d pequeno (~n^0.25 / 4) que sea coprimo con phi(n)
      3. Calcular e = d^{-1} mod phi(n)
    """
    while True:
        p   = getPrime(bits)
        q   = getPrime(bits)
        n   = p * q
        phi = (p - 1) * (q - 1)

        # d debe ser menor que n^0.25 / 3 para que el ataque funcione
        # Usamos ~n^0.24 para tener margen
        d_bits = int(bits * 0.24)
        d = getPrime(d_bits)

        if GCD(d, phi) != 1:
            continue

        e = inverse(d, phi)

        # Verificar condicion de Wiener: d < n^0.25 / 3
        if d < (n ** 0.25) / 3:
            return n, e, d, p, q


n, e, d, p, q = gen_wiener_rsa(512)
m = bytes_to_long(FLAG.encode())
assert m < n, "FLAG demasiado larga para el modulo RSA"
c = pow(m, e, n)

os.makedirs('dist', exist_ok=True)
with open('dist/wiener.txt', 'w') as f:
    f.write("=== RSA Public Key ===\n\n")
    f.write(f"n = {n}\n\n")
    f.write(f"e = {e}\n\n")
    f.write(f"c = {c}\n\n")
    f.write("Nota: el exponente privado d fue elegido con criterios de 'eficiencia'.\n")
    f.write("Quizas demasiado eficiente.\n")
