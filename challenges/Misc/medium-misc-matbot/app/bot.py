#!/usr/bin/env python3
import os, random, sys, signal

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')
NUM  = 50
TIME = 30

def timeout_handler(signum, frame):
    sys.stdout.write("\n[-] Tiempo agotado. Demasiado lento para una maquina.\n")
    sys.stdout.flush()
    sys.exit(0)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(TIME)

sys.stdout.write("=" * 50 + "\n")
sys.stdout.write("  MathBot Corp — Verificacion Automatizada\n")
sys.stdout.write("=" * 50 + "\n")
sys.stdout.write(f"Resuelve {NUM} operaciones en {TIME} segundos.\n")
sys.stdout.write("Si eres mas rapido que un humano, la flag es tuya.\n\n")
sys.stdout.flush()

score = 0
ops = ['+', '-', '*']

for i in range(NUM):
    a = random.randint(1, 999)
    b = random.randint(1, 999)
    op = random.choice(ops)
    correct = eval(f"{a}{op}{b}")
    sys.stdout.write(f"[{i+1:02d}/{NUM}] {a} {op} {b} = ")
    sys.stdout.flush()
    try:
        line = sys.stdin.readline().strip()
        if int(line) == correct:
            score += 1
        else:
            sys.stdout.write(f"    [!] Incorrecto (era {correct})\n")
            sys.stdout.flush()
    except Exception:
        sys.stdout.write("    [!] Entrada invalida\n")
        sys.stdout.flush()

signal.alarm(0)

sys.stdout.write(f"\n{'='*50}\n")
if score == NUM:
    sys.stdout.write(f"[+] {score}/{NUM} — Perfecto! Eres una maquina.\n")
    sys.stdout.write(f"[+] FLAG: {FLAG}\n")
else:
    sys.stdout.write(f"[-] {score}/{NUM} — Insuficiente. Automatiza tu solucion.\n")
sys.stdout.flush()
