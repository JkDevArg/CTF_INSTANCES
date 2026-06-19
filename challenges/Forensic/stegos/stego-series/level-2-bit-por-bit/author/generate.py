#!/usr/bin/env python3
from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image, ImageDraw

FLAG = "HL4{LSB_ESCONDIDO_EN_AZUL}"
KEY = b"mate"
MARKER = b"::END::"
ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source"
PLAYER_DIR = ROOT / "player"
SOURCE_PATH = SOURCE_DIR / "cover.png"
PLAYER_PATH = PLAYER_DIR / "mural.png"


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))


def bits_from_bytes(data: bytes) -> list[int]:
    bits: list[int] = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def build_cover(width: int = 320, height: int = 320) -> Image.Image:
    img = Image.new("RGB", (width, height), (16, 18, 28))
    draw = ImageDraw.Draw(img)
    tile = 20
    colors = [(214, 80, 118), (236, 178, 45), (54, 145, 140), (94, 112, 201)]
    for y in range(0, height, tile):
        for x in range(0, width, tile):
            idx = ((x // tile) + (y // tile)) % len(colors)
            draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=colors[idx])
    for offset in range(0, width, 16):
        draw.line((offset, 0, width - offset // 2, height), fill=(255, 255, 255), width=1)
    draw.text((18, height - 30), "bit_por_bit", fill=(10, 10, 10))
    return img


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    PLAYER_DIR.mkdir(parents=True, exist_ok=True)

    cover = build_cover()
    cover.save(SOURCE_PATH)

    payload = xor_bytes(base64.b64encode(FLAG.encode()) + MARKER, KEY)
    bits = bits_from_bytes(payload)

    img = cover.copy().convert("RGB")
    pixels = list(img.getdata())
    if len(bits) > len(pixels):
        raise SystemExit("[-] La imagen no tiene suficiente capacidad")

    new_pixels = []
    for idx, (r, g, b) in enumerate(pixels):
        if idx < len(bits):
            b = (b & 0xFE) | bits[idx]
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(PLAYER_PATH)

    print(f"[+] Fuente creada: {SOURCE_PATH}")
    print(f"[+] Reto creado:   {PLAYER_PATH}")
    print(f"[+] Bytes embebidos: {len(payload)}")


if __name__ == "__main__":
    main()
