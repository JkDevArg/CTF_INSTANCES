#!/usr/bin/env python3
from __future__ import annotations

import binascii
import hashlib
import random
import struct
import zlib
from pathlib import Path
from PIL import Image

FLAG = "HL4{NO_TODO_RUIDO_ES_AZAR}"
MAGIC = b"H4LSTEG2"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source"
PLAYER_DIR = ROOT / "player"
SOURCE_PATH = SOURCE_DIR / "cover.png"
PLAYER_PATH = PLAYER_DIR / "ruido.png"
NOTE_PATH = PLAYER_DIR / "nota.txt"
SIZE = (320, 320)


def xor_stream(data: bytes, key_material: bytes) -> bytes:
    stream = bytearray()
    counter = 0
    while len(stream) < len(data):
        block = hashlib.sha256(key_material + counter.to_bytes(4, "big")).digest()
        stream.extend(block)
        counter += 1
    return bytes(a ^ b for a, b in zip(data, stream))


def bits_from_bytes(data: bytes) -> list[int]:
    bits: list[int] = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def build_cover(width: int, height: int) -> Image.Image:
    rng = random.Random(0xEC05)
    img = Image.new("RGB", (width, height))
    pixels = []
    for y in range(height):
        for x in range(width):
            base = int(90 + 60 * ((x ^ y) % 17) / 16)
            pixels.append((
                (base + rng.randrange(0, 96)) % 256,
                (base + rng.randrange(32, 160)) % 256,
                (base + rng.randrange(64, 192)) % 256,
            ))
    img.putdata(pixels)
    return img


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    PLAYER_DIR.mkdir(parents=True, exist_ok=True)

    width, height = SIZE
    cover = build_cover(width, height)
    cover.save(SOURCE_PATH)

    key = f"mate{width}{height}".encode()
    key_material = hashlib.sha256(key).digest()
    seed = int.from_bytes(key_material[:8], "big")

    compressed = zlib.compress(FLAG.encode())
    crc = binascii.crc32(compressed) & 0xFFFFFFFF
    payload = MAGIC + struct.pack(">I", len(compressed)) + compressed + struct.pack(">I", crc)
    encrypted = xor_stream(payload, key_material)
    bits = bits_from_bytes(encrypted)

    img = cover.copy().convert("RGB")
    pixels = list(img.getdata())
    if len(bits) > len(pixels):
        raise SystemExit("[-] La imagen no tiene suficiente capacidad")

    indices = list(range(len(pixels)))
    rng = random.Random(seed)
    rng.shuffle(indices)

    for bit_index, pixel_index in enumerate(indices[:len(bits)]):
        r, g, b = pixels[pixel_index]
        pixels[pixel_index] = ((r & 0xFE) | bits[bit_index], g, b)

    img.putdata(pixels)
    img.save(PLAYER_PATH)
    NOTE_PATH.write_text(
        "No mires la imagen de izquierda a derecha.\n"
        "El orden correcto nace de: mate + dimensiones.\n",
        encoding="utf-8",
    )

    print(f"[+] Fuente creada: {SOURCE_PATH}")
    print(f"[+] Reto creado:   {PLAYER_PATH}")
    print(f"[+] Nota creada:   {NOTE_PATH}")
    print(f"[+] Payload cifrado: {len(encrypted)} bytes")


if __name__ == "__main__":
    main()
