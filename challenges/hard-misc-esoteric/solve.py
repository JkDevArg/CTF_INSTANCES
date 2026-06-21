"""
Solucion: hard-misc-esoteric

Capas (en orden de aplicacion):
  FLAG -> base64 -> brainfuck(base64) -> ROT47(brainfuck)

Reversion (de afuera hacia adentro):
  1. ROT47(transmission.txt) -> codigo brainfuck
  2. Ejecutar brainfuck -> string base64
  3. base64.decode() -> FLAG

ROT47 es simetrico: aplicarlo dos veces devuelve el original.
"""
import base64

# Leer la transmision
with open('transmission.txt') as f:
    content = f.read()

# Extraer la parte codificada (entre las lineas de separacion)
lines = [l for l in content.splitlines() if l.strip() and '===' not in l]
encoded = '\n'.join(lines)

# Paso 1: ROT47 inverso (ROT47 es simetrico, aplicar una vez revierte)
def rot47(s):
    return ''.join(
        chr(33 + (ord(c) - 33 + 47) % 94) if 33 <= ord(c) <= 126 else c
        for c in s
    )

bf_src = rot47(encoded)
print(f"[*] BF source (primeros 80 chars): {bf_src[:80]}...")

# Paso 2: ejecutar brainfuck
def run_bf(code):
    tape=[0]*30000; ptr=0; ip=0; out=[]; brackets={}; stack=[]
    for i,c in enumerate(code):
        if c=="[": stack.append(i)
        elif c=="]":
            j=stack.pop(); brackets[j]=i; brackets[i]=j
    while ip<len(code):
        c=code[ip]
        if c==">": ptr+=1
        elif c=="<": ptr-=1
        elif c=="+": tape[ptr]=(tape[ptr]+1)%256
        elif c=="-": tape[ptr]=(tape[ptr]-1)%256
        elif c==".": out.append(chr(tape[ptr]))
        elif c=="[" and tape[ptr]==0: ip=brackets[ip]
        elif c=="]" and tape[ptr]!=0: ip=brackets[ip]
        ip+=1
    return "".join(out)

b64_str = run_bf(bf_src)
print(f"[*] Base64: {b64_str}")

# Paso 3: decodificar base64
flag = base64.b64decode(b64_str).decode()
print(f"[+] Flag: {flag}")
