import os

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')


def make_bf(text):
    """
    Genera código Brainfuck que imprime cada carácter del texto.
    Estrategia eficiente: para cada carácter con valor n,
    usa un bucle multiplicador cuando n > 20.
    Formato: [celda A = contador, celda B acumula]
    Para n = q*d + r: 'A' se llena con d, el bucle suma q a B, luego r adicionales.
    """
    code = []
    for ch in text:
        n = ord(ch)
        if n == 0:
            code.append('.')
            continue
        # Encuentra el divisor óptimo (raíz cuadrada aproximada)
        d = max(1, round(n ** 0.5))
        # Ajusta d para que q*d sea lo más cercano a n
        q, r = divmod(n, d)
        if d > 1 and q > 1:
            # Patrón: d veces '+' en celda 0, luego bucle que suma q veces a celda 1
            # Estructura: +d[->>+q<<] entonces mueve a celda 1 y añade r
            # Usando celdas 0 y 1: ptr empieza en 0
            part = '+' * d                    # celda 0 = d
            part += '[->' + '+' * q + '<]'    # bucle: celda0-- ; celda1 += q  => celda1 = d*q
            part += '>'                        # mueve a celda 1
            part += '+' * r                    # celda1 += r  => celda1 = d*q + r = n
            part += '.'                        # imprime
            part += '[-]'                      # limpia celda 1
            part += '<'                        # vuelve a celda 0 (ya es 0)
        else:
            # Para valores pequeños o d=1, simplemente +n .[-]
            part = '+' * n + '.' + '[-]'
        code.append(part)
    return ''.join(code)


def make_interpreter():
    return '''#!/usr/bin/env python3
"""Interprete de Brainfuck incluido como ayuda para el reto."""
import sys


def run(code):
    tape = [0] * 30000
    ptr = 0
    ip = 0
    brackets = {}
    stack = []

    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            j = stack.pop()
            brackets[j] = i
            brackets[i] = j

    out = []
    while ip < len(code):
        c = code[ip]
        if   c == '>': ptr += 1
        elif c == '<': ptr -= 1
        elif c == '+': tape[ptr] = (tape[ptr] + 1) % 256
        elif c == '-': tape[ptr] = (tape[ptr] - 1) % 256
        elif c == '.': out.append(chr(tape[ptr]))
        elif c == ',': tape[ptr] = ord(sys.stdin.read(1))
        elif c == '[' and tape[ptr] == 0: ip = brackets[ip]
        elif c == ']' and tape[ptr] != 0: ip = brackets[ip]
        ip += 1

    print(''.join(out))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 bf.py programa.bf")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        run(f.read())
'''


bf_code = make_bf(FLAG)

os.makedirs('dist', exist_ok=True)

with open('dist/program.bf', 'w') as f:
    f.write(bf_code)

with open('dist/bf.py', 'w') as f:
    f.write(make_interpreter())

print(f"[+] program.bf generado ({len(bf_code)} bytes).")
print("[+] bf.py (interprete) generado.")
