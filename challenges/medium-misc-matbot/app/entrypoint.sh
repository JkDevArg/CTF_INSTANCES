#!/bin/sh
set -e
export FLAG="${FLAG}"
socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"python3 /app/bot.py",pty,stderr,sane &
exec python3 /app/server.py
