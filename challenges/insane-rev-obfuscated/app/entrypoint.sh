#!/bin/sh
set -e
mkdir -p /app/dist
echo "[*] Generating obfuscated checker..."
python3 /app/build.py
echo "[*] Starting Flask server..."
exec python3 /app/server.py
