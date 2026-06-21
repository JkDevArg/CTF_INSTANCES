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
