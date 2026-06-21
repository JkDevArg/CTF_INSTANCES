import hashlib
import zlib

def rifthash2(password: str, salt: bytes, version: int = 2) -> str:
    p = password.encode()
    c = zlib.crc32(p) & 0xFFFFFFFF
    cbytes = c.to_bytes(4, "little")

    x = hashlib.sha256(salt + p).digest()

    for i in range(65535):
        block = bytearray(x)
        for j in range(32):
            block[j] ^= cbytes[(i + j) % 4]
            block[j] = ((block[j] << 3) | (block[j] >> 5)) & 0xFF
        x = hashlib.sha256(bytes(block) + p + i.to_bytes(2, "little")).digest()

    return f"$rift${version}${salt.decode()}${x.hex()}"


target = "$rift$2$ogs-sfd-unl$d5ac90b87b14b8b8c9789bfe1547643f8146f1806b14e05576a5ea8e1e5e9cdf"

flag_correcta = "HL4{SFD_111_Body_Rare_Spell}"
salt = "ogs-sfd-unl"

hash_generado = rifthash2(flag_correcta, salt.encode(), version=2)

print(f"Flag: {flag_correcta}")
print(f"Hash generado: {hash_generado}")
print(f"Hash objetivo:  {target}")
print(f"¿Coinciden? {hash_generado == target}")