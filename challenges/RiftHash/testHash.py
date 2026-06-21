import hashlib
import zlib

def rifthash(password: str, salt: bytes, version: int = 1) -> str:
    p = password.encode()
    c = zlib.crc32(p) & 0xFFFFFFFF
    cbytes = c.to_bytes(4, "little")

    x = hashlib.sha256(salt + p).digest()

    for i in range(65536):
        block = bytearray(x)
        for j in range(32):
            block[j] ^= cbytes[(i + j) % 4]
            block[j] = ((block[j] << 3) | (block[j] >> 5)) & 0xFF
        x = hashlib.sha256(bytes(block) + p + i.to_bytes(2, "little")).digest()

    return f"$rift${version}${salt.decode()}${x.hex()}"


target = "$rift$1$unleashed-lab$ca0fbdf06382365b8bd9ad6e1340778516d9f6c5a3e7135409ffd8f5c23064b8"

flag_correcta = "HL4{143a_chaos}"
salt = "unleashed-lab"

hash_generado = rifthash(flag_correcta, salt.encode(), version=1)

print(f"Flag: {flag_correcta}")
print(f"Hash generado: {hash_generado}")
print(f"Hash objetivo:  {target}")
print(f"¿Coinciden? {hash_generado == target}")