# Solución de referencia: hard-aes-ecb-oracle
# Ataque: AES-ECB Byte-at-a-time Decryption
#
# El oráculo cifra: user_input + SECRET bajo AES-ECB con clave fija.
# Como ECB es determinista (mismo bloque → mismo ciphertext), podemos
# recuperar SECRET byte a byte controlando el alineamiento del input.

import requests

BASE = "http://localhost:8080"


def oracle(data: bytes) -> bytes:
    r = requests.post(f"{BASE}/encrypt", json={"data": data.hex()}, timeout=10)
    r.raise_for_status()
    return bytes.fromhex(r.json()["ciphertext"])


def detect_block_size() -> int:
    base = len(oracle(b''))
    for i in range(1, 33):
        new_len = len(oracle(b'A' * i))
        if new_len > base:
            return new_len - base
    raise RuntimeError("No se pudo detectar el tamaño de bloque")


def detect_secret_length(block_size: int) -> int:
    base = len(oracle(b''))
    for i in range(1, block_size + 1):
        if len(oracle(b'A' * i)) > base:
            return base - i
    return base


def confirm_ecb(block_size: int) -> bool:
    ct = oracle(b'A' * (block_size * 2))
    return ct[:block_size] == ct[block_size:block_size * 2]


def decrypt_secret(block_size: int, secret_len: int) -> bytes:
    secret = b''
    for i in range(secret_len):
        # Alinear para que SECRET[i] quede al final del bloque objetivo
        alignment = b'A' * (block_size - 1 - i % block_size)
        block_idx = i // block_size

        # Bloque objetivo: contiene alignment + secret[:i] + SECRET[i]
        target = oracle(alignment)[block_idx * block_size:(block_idx + 1) * block_size]

        # Prefijo conocido de 15 bytes para el bloque de bruteforce
        known_prefix = (b'A' * (block_size - 1) + secret)[-( block_size - 1):]

        found = False
        for b in range(256):
            guess = known_prefix + bytes([b])
            ct = oracle(guess)
            if ct[:block_size] == target:
                secret += bytes([b])
                found = True
                break

        if not found:
            print(f"[!] Byte {i} no encontrado — posiblemente padding PKCS7")
            break

        print(f"[{i+1}/{secret_len}] {secret}", end='\r')

    return secret


if __name__ == '__main__':
    block_size = detect_block_size()
    print(f"[*] Tamaño de bloque: {block_size}")

    if not confirm_ecb(block_size):
        print("[!] No parece ser ECB")
        exit(1)
    print("[*] Modo ECB confirmado")

    secret_len = detect_secret_length(block_size)
    print(f"[*] Longitud del secreto: ~{secret_len} bytes")

    secret = decrypt_secret(block_size, secret_len)
    print(f"\n[+] Secreto recuperado: {secret.decode(errors='replace')}")
