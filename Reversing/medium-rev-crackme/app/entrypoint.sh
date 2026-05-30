#!/bin/sh
set -e
mkdir -p dist
python3 build.py
gcc -o dist/crackme challenge.c -O2 -s -no-pie
echo "[build] Binary compiled and stripped"
exec python3 server.py
