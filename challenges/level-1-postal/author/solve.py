#!/usr/bin/env python3
from __future__ import annotations

import base64
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PLAYER_PATH = ROOT / "player" / "postal.png"


def main() -> None:
    img = Image.open(PLAYER_PATH)
    comment = img.info.get("Comment")
    if not comment:
        raise SystemExit("[-] No se encontró metadata Comment")

    flag = base64.b64decode(comment).decode()
    print(f"Comment: {comment}")
    print(f"Flag: {flag}")


if __name__ == "__main__":
    main()
