#!/bin/sh
set -e

echo "$FLAG" > /home/ctf/flag.txt
chmod 400 /home/ctf/flag.txt

mkdir -p /app/download
cp /app/logger /app/download/logger

socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"/app/logger",pty,stderr,sane &

exec python3 /app/server.py
