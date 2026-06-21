#!/usr/bin/env python3
"""
Padding Oracle Attack on AES-CBC.

Para cada bloque b y cada byte i (de derecha a izquierda):
  - Modificar el byte i del IV/bloque anterior
  - Probar los 256 valores posibles
  - Cuando el oracle devuelve valid=True, tenemos el byte intermedio
  - plaintext_byte = intermediate_byte XOR original_byte_from_prev_block

Uso: python3 solve.py [URL_BASE]
     Por defecto: http://localhost:8080
"""
import sys, requests, json

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://localhost:8080'

print(f"[*] Target: {BASE}")

# Leer el ciphertext interceptado
r = requests.get(f'{BASE}/download/intercepted.json')
data = json.loads(r.content)
IV         = bytes.fromhex(data['iv'])
CIPHERTEXT = bytes.fromhex(data['ciphertext'])

print(f"[*] IV:         {IV.hex()}")
print(f"[*] Ciphertext: {CIPHERTEXT.hex()} ({len(CIPHERTEXT)} bytes, {len(CIPHERTEXT)//16} bloques)")


def oracle(iv: bytes, ct: bytes) -> bool:
    """Llama al oraculo de padding. True si padding valido."""
    r = requests.post(f'{BASE}/oracle',
                      json={'iv': iv.hex(), 'ciphertext': ct.hex()})
    return r.json().get('valid', False)


def decrypt_block(prev_block: bytes, curr_block: bytes) -> bytes:
    """Descifra un bloque de 16 bytes usando el oraculo de padding."""
    intermediate = bytearray(16)

    for pos in range(15, -1, -1):
        pad_byte = 16 - pos  # valor de padding objetivo (1..16)

        # Construir bloque modificado: bytes ya conocidos dan padding correcto
        crafted = bytearray(16)
        for k in range(pos + 1, 16):
            crafted[k] = intermediate[k] ^ pad_byte

        # Probar los 256 valores para la posicion actual
        found = False
        for guess in range(256):
            crafted[pos] = guess
            if oracle(bytes(crafted), curr_block):
                # Encontramos el valor intermedio
                intermediate[pos] = guess ^ pad_byte
                found = True
                break

        if not found:
            # Puede haber colision de padding valido casual; reintentar con offset
            # (raro para posicion 15 donde 0x01 puede coincidir con otro byte)
            raise ValueError(f"No se encontro solucion para pos={pos} — reintenta el script")

    # XOR del intermedio con el bloque anterior original = plaintext
    return bytes(i ^ p for i, p in zip(intermediate, prev_block))


# Descifrar todos los bloques
blocks     = [CIPHERTEXT[i:i+16] for i in range(0, len(CIPHERTEXT), 16)]
all_blocks = [IV] + blocks
plaintext  = b''

for i in range(1, len(all_blocks)):
    print(f"[*] Descifrando bloque {i}/{len(blocks)}...")
    plaintext += decrypt_block(all_blocks[i-1], all_blocks[i])

# Eliminar PKCS#7 padding
pad_len   = plaintext[-1]
plaintext = plaintext[:-pad_len]

print(f"\n[+] Plaintext: {plaintext.decode(errors='replace')}")
