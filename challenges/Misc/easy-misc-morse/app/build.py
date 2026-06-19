import os

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

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


def encode(text):
    result = []
    for c in text.upper():
        if c == ' ':
            result.append('/')
        elif c in MORSE:
            result.append(MORSE[c])
        else:
            result.append('?')
    return ' '.join(result)


morse = encode(FLAG)

os.makedirs('dist', exist_ok=True)
with open('dist/signal.txt', 'w') as f:
    f.write("=== SEÑAL INTERCEPTADA ===\n")
    f.write("Origen: Estación Alfa-7\n")
    f.write("Clasificación: TOP SECRET\n\n")
    f.write(morse + "\n\n")
    f.write("Clave de transmisión: MORSE\n")
    f.write("Separador de palabras: /\n")

print("[+] signal.txt generado correctamente.")
