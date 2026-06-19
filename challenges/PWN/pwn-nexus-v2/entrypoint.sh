#!/bin/sh
set -e

# Write the dynamic flag (replaced by Whaley per-user instance)
echo -n "${FLAG:-HL4{placeholder_flag_here}}" > /home/ctf/flag.txt

# Prepare download directory (binary + libc only — flag.txt stays out)
mkdir -p /home/ctf/download
cp /home/ctf/nexus     /home/ctf/download/nexus
cp /home/ctf/libc.so.6 /home/ctf/download/libc.so.6

# Start the pwn service
socat TCP-LISTEN:9999,reuseaddr,fork EXEC:/home/ctf/nexus &

# Start the file download server
cd /home/ctf && exec python3 server.py
