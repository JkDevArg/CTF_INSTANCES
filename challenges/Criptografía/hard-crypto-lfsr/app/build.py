import os, random

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# 16-bit Galois LFSR con polinomio conocido
# Polinomio: x^16 + x^14 + x^13 + x^11 + 1
# Representacion Galois de los taps (bits 14, 13, 11 desde la derecha)
TAPS = 0xB400


def lfsr16(state: int, n_bytes: int) -> bytes:
    """Genera n_bytes usando un LFSR Galois de 16 bits."""
    out = []
    for _ in range(n_bytes):
        byte_val = 0
        for b in range(8):
            bit = state & 1
            byte_val |= (bit << b)
            state >>= 1
            if bit:
                state ^= TAPS
        out.append(byte_val)
    return bytes(out)


# Semilla aleatoria de 16 bits (espacio de busqueda: 65 536 estados)
SEED = random.randint(1, 0xFFFF)

# Prefijo conocido (dado al jugador)
KNOWN_PREFIX = b'HACKL4BS_CTF_'
MESSAGE      = KNOWN_PREFIX + FLAG.encode()

keystream  = lfsr16(SEED, len(MESSAGE))
ciphertext = bytes(m ^ k for m, k in zip(MESSAGE, keystream))

os.makedirs('dist', exist_ok=True)
with open('dist/stream.txt', 'w') as f:
    f.write("=== LFSR Stream Cipher ===\n\n")
    f.write("Polinomio: x^16 + x^14 + x^13 + x^11 + 1\n")
    f.write("Taps (hex): 0xB400\n")
    f.write("Longitud de clave: 16 bits (65 536 posibilidades)\n")
    f.write("Prefijo de texto plano conocido: HACKL4BS_CTF_\n\n")
    f.write(f"Ciphertext (hex):\n{ciphertext.hex()}\n")
