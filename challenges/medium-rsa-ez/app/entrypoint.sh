#!/bin/sh
set -e
mkdir -p dist
python3 build.py
echo "[entrypoint] Build done, starting server..."
exec python3 server.py
