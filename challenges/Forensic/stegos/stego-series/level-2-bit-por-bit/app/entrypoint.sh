#!/bin/sh
set -e
mkdir -p dist
python3 build.py
exec python3 server.py
