#!/usr/bin/env python3
"""
Solución de referencia para easy-misc-brainfuck.

Opcion 1: usar el interprete incluido
  python3 bf.py program.bf

Opcion 2: este script (lee program.bf y lo ejecuta directamente)
  python3 solve.py program.bf
"""
import sys


def run_bf(code):
    tape = [0] * 30000
    ptr = 0
    ip = 0
    brackets = {}
    stack = []
    out = []

    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            j = stack.pop()
            brackets[j] = i
            brackets[i] = j

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

    return ''.join(out)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'program.bf'
    with open(path) as f:
        code = f.read()
    result = run_bf(code)
    print(f"[+] FLAG: {result}")


if __name__ == '__main__':
    main()
