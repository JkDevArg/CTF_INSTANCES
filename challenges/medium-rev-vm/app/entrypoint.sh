#!/bin/sh
set -e
mkdir -p dist
python3 build.py
gcc -o dist/vm_challenge challenge.c -O2 -s -no-pie
echo "[build] VM binary compiled and stripped"
exec python3 server.py
