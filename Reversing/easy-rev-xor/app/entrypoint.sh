#!/bin/sh
set -e
mkdir -p dist
python3 build.py
gcc -o dist/challenge challenge.c -O2 -s -no-pie
echo "[build] Binary compiled successfully"
exec python3 server.py
