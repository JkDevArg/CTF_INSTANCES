#!/usr/bin/env python3
"""
Solución: medium-misc-matbot
Técnica: automatización con pwntools — leer cada problema, calcular, enviar.
"""
import sys, re
from pwn import *

HOST = args.HOST or 'localhost'
PORT = int(args.PORT or 9999)

if args.REMOTE:
    p = remote(HOST, PORT)
else:
    p = process(['python3', 'app/bot.py'])

# Consumir encabezado hasta la línea en blanco posterior al conteo
p.recvuntil(b'la flag es tuya.\n\n')

while True:
    try:
        line = p.recvuntil(b'= ', timeout=5).decode(errors='replace')
        # Extraer: [01/50] 123 + 456 =
        m = re.search(r'(\d+)\s*([+\-*])\s*(\d+)\s*=', line)
        if not m:
            # Ya no hay mas preguntas — recibir resultado final
            remaining = p.recvall(timeout=3).decode(errors='replace')
            print(line + remaining)
            break
        a   = int(m.group(1))
        op  = m.group(2)
        b   = int(m.group(3))
        result = eval(f"{a}{op}{b}")
        p.sendline(str(result).encode())
    except EOFError:
        break

try:
    print(p.recvall(timeout=2).decode(errors='replace'))
except Exception:
    pass
