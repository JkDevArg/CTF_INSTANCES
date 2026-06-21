#!/usr/bin/env python3
from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image

KEY = b"mate"
MARKER = b"::END::"
ROOT = Path(__file__).resolve().parents[1]
PLAYER_PATH = ROOT / "player" / "mural.png"


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))


def main() -> None:
    img = Image.open(PLAYER_PATH).convert("RGB")
    bits = [(b & 1) for _, _, b in img.getdata()]

    raw = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i:i + 8]
        if len(chunk) < 8:
            break
        value = 0
        for bit in chunk:
            value = (value << 1) | bit
        raw.append(value)

    decoded = xor_bytes(bytes(raw), KEY)
    end = decoded.find(MARKER)
    if end == -1:
        raise SystemExit("[-] No se encontró el marcador final")

    payload = decoded[:end]
    flag = base64.b64decode(payload).decode()
    print(flag)


if __name__ == "__main__":
    main()
