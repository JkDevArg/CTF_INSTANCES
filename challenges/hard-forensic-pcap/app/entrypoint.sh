#!/bin/sh
set -e

# Generar el archivo de captura con la FLAG real
python3 /app/build.py

exec python3 /app/server.py
