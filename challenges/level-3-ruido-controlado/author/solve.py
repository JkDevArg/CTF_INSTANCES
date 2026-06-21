#!/usr/bin/env python3
from __future__ import annotations

import binascii
import hashlib
import random
import struct
import zlib
from pathlib import Path
from PIL import Image

MAGIC = b"H4LSTEG2"
ROOT = Path(__file__).resolve().parents[1]
PLAYER_PATH = ROOT / "player" / "ruido.png"


def xor_stream(data: bytes, key_material: bytes) -> bytes:
    stream = bytearray()
    counter = 0
    while len(stream) < len(data):
        block = hashlib.sha256(key_material + counter.to_bytes(4, "big")).digest()
        stream.extend(block)
        counter += 1
    return bytes(a ^ b for a, b in zip(data, stream))


def main() -> None:
    img = Image.open(PLAYER_PATH).convert("RGB")
    width, height = img.size
    pixels = list(img.getdata())

    key = f"mate{width}{height}".encode()
    key_material = hashlib.sha256(key).digest()
    seed = int.from_bytes(key_material[:8], "big")

    indices = list(range(len(pixels)))
    rng = random.Random(seed)
    rng.shuffle(indices)

    bits = [(pixels[idx][0] & 1) for idx in indices]
    raw = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i + 8]
        if len(chunk) < 8:
            break
        value = 0
        for bit in chunk:
            value = (value << 1) | bit
        raw.append(value)

    plain = xor_stream(bytes(raw), key_material)
    if plain[:8] != MAGIC:
        raise SystemExit("[-] Magic incorrecto")

    length = struct.unpack(">I", plain[8:12])[0]
    compressed = plain[12:12 + length]
    crc_expected = struct.unpack(">I", plain[12 + length:16 + length])[0]
    crc_actual = binascii.crc32(compressed) & 0xFFFFFFFF
    if crc_actual != crc_expected:
        raise SystemExit(f"[-] CRC inválido: {crc_actual:#x} != {crc_expected:#x}")

    flag = zlib.decompress(compressed).decode()
    print(flag)


if __name__ == "__main__":
    main()
