import os

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# Opcodes
OP_LOAD  = 0x01  # LOAD Rd, imm8
OP_ADD   = 0x02  # ADD  Rd, Ra, Rb
OP_XOR   = 0x03  # XOR  Rd, Ra, Rb
OP_PRINT = 0x04  # PRINT Rd  (outputs reg ^ LFSR_next, so output is garbled)
OP_HALT  = 0xFF

def compile_flag(flag_str):
    prog = []
    for ch in flag_str:
        # LOAD R0, char_value
        prog += [OP_LOAD, 0x00, ord(ch)]
        # PRINT R0  (VM XORs with LFSR)
        prog += [OP_PRINT, 0x00]
    prog += [OP_HALT]
    return bytes(prog)

program = compile_flag(FLAG)

os.makedirs('dist', exist_ok=True)
with open('dist/program.bin', 'wb') as f:
    f.write(program)

vm_src = r'''#!/usr/bin/env python3
"""
MateVM v1.0 -- Virtual Machine Interpreter
Instruction Set Architecture (ISA):
  0x01 Rd imm8   : LOAD Rd, imm8     -- load 8-bit immediate into register Rd
  0x02 Rd Ra Rb  : ADD  Rd = Ra + Rb  (mod 256)
  0x03 Rd Ra Rb  : XOR  Rd = Ra ^ Rb
  0x04 Rd        : PRINT Rd           -- output char(Rd ^ lfsr_next())
  0xFF           : HALT
Registers: R0=0, R1=1, R2=2, R3=3
LFSR: 8-bit, initial state=0x42, rotate-left-1 each PRINT call
"""
import sys

def lfsr_next(state):
    """8-bit rotate-left by 1."""
    return ((state << 1) | (state >> 7)) & 0xFF

def run(program):
    regs  = [0, 0, 0, 0]
    ip    = 0
    lfsr  = 0x42
    out   = []
    while ip < len(program):
        op = program[ip]
        if op == 0x01:          # LOAD Rd, imm8
            rd, imm = program[ip+1], program[ip+2]
            regs[rd] = imm
            ip += 3
        elif op == 0x02:        # ADD Rd Ra Rb
            rd, ra, rb = program[ip+1], program[ip+2], program[ip+3]
            regs[rd] = (regs[ra] + regs[rb]) & 0xFF
            ip += 4
        elif op == 0x03:        # XOR Rd Ra Rb
            rd, ra, rb = program[ip+1], program[ip+2], program[ip+3]
            regs[rd] = regs[ra] ^ regs[rb]
            ip += 4
        elif op == 0x04:        # PRINT Rd
            rd = program[ip+1]
            lfsr = lfsr_next(lfsr)
            out.append(chr(regs[rd] ^ lfsr))
            ip += 2
        elif op == 0xFF:        # HALT
            break
        else:
            print(f"[!] Unknown opcode 0x{op:02x} at ip={ip}", file=sys.stderr)
            break
    return ''.join(out)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 vm.py program.bin")
        sys.exit(1)
    with open(sys.argv[1], 'rb') as f:
        prog = f.read()
    result = run(prog)
    print(result)
'''

with open('dist/vm.py', 'w') as f:
    f.write(vm_src)

isa_doc = """# MateVM v1.0 -- Instruction Set Architecture

## Registros
R0, R1, R2, R3 -- 8-bit unsigned (0-255)

## Instrucciones

| Opcode | Formato         | Descripcion                              |
|--------|-----------------|------------------------------------------|
| 0x01   | LOAD Rd, imm8   | Rd <- imm8                               |
| 0x02   | ADD  Rd, Ra, Rb | Rd <- (Ra + Rb) mod 256                  |
| 0x03   | XOR  Rd, Ra, Rb | Rd <- Ra XOR Rb                          |
| 0x04   | PRINT Rd        | output <- char(Rd XOR lfsr_next())      |
| 0xFF   | HALT            | detener ejecucion                        |

## LFSR
- Estado inicial: 0x42
- Avanza en cada instruccion PRINT
- Operacion: rotate-left 8-bit por 1 posicion
  `state = ((state << 1) | (state >> 7)) & 0xFF`

## Formato del bytecode
Los bytes del programa son leidos secuencialmente segun la longitud de cada instruccion.

## Ejemplo
```
01 00 41   -> LOAD R0, 0x41 ('A')
04 00      -> PRINT R0  (imprime 'A' XOR lfsr_next())
FF         -> HALT
```
"""

with open('dist/isa.md', 'w') as f:
    f.write(isa_doc)
