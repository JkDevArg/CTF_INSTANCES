#!/bin/sh
set -e
echo "$FLAG" > /home/ctf/flag.txt
chmod 444 /home/ctf/flag.txt
socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"python3 /app/jail.py",pty,stderr,sane &
exec python3 /app/server.py
