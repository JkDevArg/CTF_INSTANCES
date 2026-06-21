import os, base64

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# Layer 1: base64
b64 = base64.b64encode(FLAG.encode()).decode()

# Layer 2: brainfuck that outputs b64 string
def make_bf(text):
    code = []
    prev = 0
    for c in text:
        n = ord(c)
        diff = n - prev
        if diff > 0:
            code.append('+' * diff)
        elif diff < 0:
            code.append('-' * (-diff))
        code.append('.')
        prev = n
    return ''.join(code)

bf_src = make_bf(b64)

# Layer 3: ROT47
def rot47(s):
    return ''.join(
        chr(33 + (ord(c) - 33 + 47) % 94) if 33 <= ord(c) <= 126 else c
        for c in s
    )

encoded = rot47(bf_src)

os.makedirs('dist', exist_ok=True)
with open('dist/transmission.txt', 'w') as f:
    f.write("=== TRANSMISSION BEGINS ===\n\n")
    f.write(encoded)
    f.write("\n\n=== TRANSMISSION ENDS ===\n")

# Also provide a BF interpreter helper
bf_interp = '''#!/usr/bin/env python3
import sys

def run(code, inp=""):
    tape=[0]*30000; ptr=0; ip=0; i_ptr=0
    out=[]; brackets={}; stack=[]
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
        elif c==",":
            tape[ptr]=ord(inp[i_ptr]) if i_ptr<len(inp) else 0; i_ptr+=1
        elif c=="[" and tape[ptr]==0: ip=brackets[ip]
        elif c=="]" and tape[ptr]!=0: ip=brackets[ip]
        ip+=1
    return "".join(out)

with open(sys.argv[1]) as f: code=f.read()
print(run(code), end="")
'''
with open('dist/bf.py', 'w') as f:
    f.write(bf_interp)
