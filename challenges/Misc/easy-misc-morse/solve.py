#!/usr/bin/env python3
"""
Solución de referencia para easy-misc-morse.
Uso: descarga signal.txt del servidor y ejecuta este script.
  python3 solve.py signal.txt
"""
import sys

MORSE = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',
    'F': '..-.', 'G': '--.',  'H': '....', 'I': '..',   'J': '.---',
    'K': '-.-',  'L': '.-..', 'M': '--',   'N': '-.',   'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '{': '-.--.-', '}': '-.--.',  '_': '..--.-', '!': '-.-.--',
    '@': '.--.-.', ':': '---...', '=': '-...-',  '+': '.-.-.',
    '-': '-....-', '(': '-.--.-', ')': '-.--.',
}

MORSE_DECODE = {v: k for k, v in MORSE.items()}


def decode_morse(morse_str):
    words = morse_str.strip().split(' / ')
    result = []
    for word in words:
        tokens = word.strip().split()
        result.append(''.join(MORSE_DECODE.get(t, '?') for t in tokens))
    return ' '.join(result)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'signal.txt'
    with open(path) as f:
        content = f.read()

    # Encuentra la línea que contiene la señal Morse (puntos y rayas)
    morse_line = None
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and all(c in '.-/ ' for c in stripped) and ('.' in stripped or '-' in stripped):
            morse_line = stripped
            break

    if not morse_line:
        print("[-] No se encontró una línea Morse válida en el archivo.")
        sys.exit(1)

    decoded = decode_morse(morse_line)
    # El encode usa mayúsculas; la flag suele tener forma CTF{...}
    # Ajusta mayúsculas/minúsculas si es necesario
    print(f"[+] Morse encontrado: {morse_line[:80]}...")
    print(f"[+] FLAG: {decoded}")


if __name__ == '__main__':
    main()
