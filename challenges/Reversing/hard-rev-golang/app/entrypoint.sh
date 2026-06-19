#!/bin/sh
set -e
mkdir -p /app/dist
echo "[*] Building Go binary..."
python3 /app/build.py
echo "[*] Starting Flask server..."
exec python3 /app/server.py
