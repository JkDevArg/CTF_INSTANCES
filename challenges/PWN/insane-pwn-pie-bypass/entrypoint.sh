#!/bin/sh
set -e

echo "$FLAG" > /home/ctf/flag.txt
chmod 400 /home/ctf/flag.txt

mkdir -p /app/download
cp /app/safebox /app/download/safebox

socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"/app/safebox",pty,stderr,sane &

exec python3 /app/server.py
