#!/usr/bin/env bash
# Genera certificado autofirmado para el lab
mkdir -p "$(dirname "$0")/certs"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$(dirname "$0")/certs/lab.key" \
  -out    "$(dirname "$0")/certs/lab.crt" \
  -subj "/C=US/ST=Lab/L=Lab/O=EthicalHackingLab/CN=lab02.local"
echo "✅ Certificado generado en nginx/certs/"
