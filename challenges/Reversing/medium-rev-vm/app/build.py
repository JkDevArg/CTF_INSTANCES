import os

FLAG = os.environ.get('FLAG') or 'CTF{placeholder_flag_here}'

# VM opcodes:
#   OP_CHECK = 0x01  args: index(u8), expected(u8)
#     -> takes input[index], applies (char ^ (index * 0x13 + 0x5A)) & 0xFF
#     -> compares with expected; if mismatch, HALT_FAIL
#   OP_HALT  = 0x02  no args: print "Correct!" and exit 0
#   OP_FAIL  = 0x03  no args: print "Wrong."  and exit 1
#
# Encoding: expected = (ord(flag[i]) ^ (i * 0x13 + 0x5A)) & 0xFF
# Reverse:  flag[i]  = chr((expected ^ (i * 0x13 + 0x5A)) & 0xFF)

prog = []
for i, c in enumerate(FLAG):
    expected = (ord(c) ^ (i * 0x13 + 0x5A)) & 0xFF
    prog.extend([0x01, i & 0xFF, expected])  # OP_CHECK, index, expected
prog.append(0x02)  # OP_HALT

arr = ', '.join(f'0x{b:02x}' for b in prog)
with open('bytecode.h', 'w') as f:
    f.write(f'#define INPUT_LEN {len(FLAG)}\n')
    f.write(f'#define PROG_LEN  {len(prog)}\n')
    f.write(f'static const unsigned char prog[] = {{{arr}}};\n')

print(f'[build] bytecode.h: {len(prog)} bytes for {len(FLAG)}-char flag')
