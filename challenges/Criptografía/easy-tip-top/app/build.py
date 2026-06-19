import os
import base64

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')


def encode(text: str) -> str:
    data = text.encode()
    # Round 1: reverse, then base64
    data = base64.b64encode(data[::-1])
    # Round 2: reverse, then base64
    data = base64.b64encode(data[::-1])
    return data.decode()


cipher = encode(FLAG)

os.makedirs('dist', exist_ok=True)
with open('dist/tip-top.txt', 'w', encoding='utf-8') as f:
    f.write("El tiempo nunca avanzó en línea recta.\n")
    f.write("Cada capa fue invertida antes de continuar.\n")
    f.write("Solo quien siga el orden correcto podrá recuperar el mensaje original.\n\n")
    f.write(cipher + "\n")

print(f"[build] tip-top.txt generado ({len(FLAG)} chars)")
