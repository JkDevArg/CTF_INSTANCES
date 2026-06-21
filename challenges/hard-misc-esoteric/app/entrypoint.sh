#!/bin/sh
set -e
mkdir -p /app/dist
python3 /app/build.py
exec python3 /app/server.py
