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


def parse_hash(line: str):
    parts = line.strip().split("$")
    if len(parts) != 5 or parts[1] != "rift":
        raise ValueError(f"Invalid rift hash: {line!r}")
    version = int(parts[2])
    salt = parts[3].encode()
    digest = parts[4]
    return version, salt, digest


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: rifthash.py <password> <salt>")
        sys.exit(1)

    password = sys.argv[1]
    salt = sys.argv[2].encode()
    print(rifthash(password, salt))