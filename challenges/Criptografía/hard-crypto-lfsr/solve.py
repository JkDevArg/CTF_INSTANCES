#!/usr/bin/env python3
"""
Known-plaintext attack on 16-bit LFSR stream cipher.

Prefijo conocido: b'HACKL4BS_CTF_'
Espacio de estados: 2^16 = 65 536 — brute force es trivial.

Uso: python3 solve.py [ruta_a_stream.txt]
     Por defecto busca stream.txt en el directorio actual.
"""
import sys, re

TAPS         = 0xB400
KNOWN_PREFIX = b'HACKL4BS_CTF_'
FILENAME     = sys.argv[1] if len(sys.argv) > 1 else 'stream.txt'


def lfsr16(state: int, n: int) -> bytes:
    """Genera n bytes del LFSR Galois de 16 bits con taps 0xB400."""
    out = []
    for _ in range(n):
        byte_val = 0
        for b in range(8):
            bit = state & 1
            byte_val |= (bit << b)
            state >>= 1
            if bit:
                state ^= TAPS
        out.append(byte_val)
    return bytes(out)


with open(FILENAME) as f:
    content = f.read()

m = re.search(r'Ciphertext \(hex\):\n([0-9a-f]+)', content)
if not m:
    print("[-] No se encontro el ciphertext en el archivo.")
    sys.exit(1)

ciphertext = bytes.fromhex(m.group(1))
print(f"[*] Longitud del ciphertext: {len(ciphertext)} bytes")
print(f"[*] Fuerza bruta sobre 65 536 estados LFSR...")

found = False
for seed in range(1, 0x10000):
    ks = lfsr16(seed, len(KNOWN_PREFIX))
    candidate = bytes(c ^ k for c, k in zip(ciphertext, ks))
    if candidate == KNOWN_PREFIX:
        print(f"[+] Semilla encontrada: {seed} (0x{seed:04x})")
        full_ks  = lfsr16(seed, len(ciphertext))
        plaintext = bytes(c ^ k for c, k in zip(ciphertext, full_ks))
        print(f"[+] Plaintext: {plaintext.decode(errors='replace')}")
        found = True
        break

if not found:
    print("[-] No se encontro la semilla. Verifica el archivo stream.txt.")
