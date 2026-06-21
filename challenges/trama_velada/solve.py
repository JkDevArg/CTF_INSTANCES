#!/usr/bin/env python3
import base64
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PCAP = ROOT / "traffic.pcap"
KEYLOG = ROOT / "keylog.txt"


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def main() -> None:
    if not PCAP.exists() or not KEYLOG.exists():
        print(f"Faltan {PCAP} o {KEYLOG}")
        sys.exit(1)

    cmd = [
        "tshark",
        "-r",
        str(PCAP),
        "-o",
        f"tls.keylog_file:{KEYLOG}",
        "-Y",
        "http.response",
        "-T",
        "fields",
        "-e",
        "frame.number",
        "-e",
        "http.content_encoding",
        "-e",
        "http.transfer_encoding",
        "-e",
        "http.file_data",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(result.stderr.strip() or "tshark falló")
        sys.exit(2)

    seed = None
    encoded_flag = None

    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) < 4:
            continue

        _, content_encoding, transfer_encoding, file_data_hex = parts[:4]
        payload = bytes.fromhex(file_data_hex) if file_data_hex else b""

        if content_encoding == "gzip":
            obj = json.loads(payload.decode("utf-8"))
            seed = obj["seed"].encode()
        elif transfer_encoding == "chunked":
            encoded_flag = base64.b64decode(payload)

    if seed is None or encoded_flag is None:
        print("No se pudo reconstruir el seed o el payload final.")
        sys.exit(3)

    flag = xor_bytes(encoded_flag, seed).decode("utf-8", errors="replace")
    print(flag)


if __name__ == "__main__":
    main()
