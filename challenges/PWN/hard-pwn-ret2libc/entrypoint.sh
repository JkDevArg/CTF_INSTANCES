#!/bin/sh
set -e

echo "$FLAG" > /home/ctf/flag.txt
chmod 400 /home/ctf/flag.txt

mkdir -p /app/download
cp /app/target /app/download/target
cp /lib/x86_64-linux-gnu/libc.so.6 /app/download/libc.so.6

socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"/app/target",pty,stderr,sane &

exec python3 /app/server.py
