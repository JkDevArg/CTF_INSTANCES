"""
Solucion: hard-misc-vm

La VM aplica XOR con un LFSR (rotate-left 8-bit, seed=0x42) en cada PRINT.
El bytecode LOAD almacena el valor REAL de cada byte de la flag.
El PRINT imprime (real_value XOR lfsr_state), que es basura.

Para obtener la flag sin ejecutar el programa (analisis estatico):
  1. Parsear el bytecode e identificar instrucciones LOAD seguidas de PRINT
  2. Extraer el valor inmediato de cada LOAD
  3. Ese valor ES el byte real de la flag

Para obtener la flag ejecutando el programa y revirtiendo:
  1. Correr vm.py program.bin -> salida garbled
  2. Simular el LFSR con seed=0x42
  3. XOR cada byte de output con el LFSR correspondiente -> flag
"""

# Metodo 1: analisis estatico del bytecode
with open('program.bin', 'rb') as f:
    prog = list(f.read())

flag_bytes = []
ip = 0
while ip < len(prog):
    op = prog[ip]
    if op == 0x01:   # LOAD Rd, imm8
        rd = prog[ip+1]
        imm = prog[ip+2]
        # Verificar si la siguiente instruccion es PRINT sobre el mismo registro
        if ip+3 < len(prog) and prog[ip+3] == 0x04 and prog[ip+4] == rd:
            flag_bytes.append(imm)
        ip += 3
    elif op in (0x02, 0x03):  # ADD o XOR (4 bytes)
        ip += 4
    elif op == 0x04:           # PRINT (2 bytes)
        ip += 2
    elif op == 0xFF:           # HALT
        break
    else:
        ip += 1

flag = bytes(flag_bytes).decode(errors='replace')
print(f"[+] Flag (analisis estatico): {flag}")

# Metodo 2: ejecutar la VM y revertir el LFSR
def lfsr_next(state):
    return ((state << 1) | (state >> 7)) & 0xFF

def run_vm(program):
    regs = [0,0,0,0]; ip=0; lfsr=0x42; out=[]
    while ip < len(program):
        op = program[ip]
        if op == 0x01:
            regs[program[ip+1]] = program[ip+2]; ip += 3
        elif op == 0x02:
            regs[program[ip+1]] = (regs[program[ip+2]]+regs[program[ip+3]])&0xFF; ip+=4
        elif op == 0x03:
            regs[program[ip+1]] = regs[program[ip+2]]^regs[program[ip+3]]; ip+=4
        elif op == 0x04:
            lfsr = lfsr_next(lfsr)
            out.append(regs[program[ip+1]] ^ lfsr)
            ip+=2
        elif op == 0xFF:
            break
        else:
            ip+=1
    return bytes(out)

with open('program.bin', 'rb') as f:
    raw = list(f.read())

garbled = run_vm(raw)
print(f"[*] Salida garbled: {garbled}")

# Revertir: garbled[i] = flag_byte[i] XOR lfsr[i]
# Por tanto:  flag_byte[i] = garbled[i] XOR lfsr[i]
lfsr = 0x42
recovered = []
for b in garbled:
    lfsr = lfsr_next(lfsr)
    recovered.append(b ^ lfsr)
print(f"[+] Flag (reversion LFSR): {bytes(recovered).decode(errors='replace')}")
