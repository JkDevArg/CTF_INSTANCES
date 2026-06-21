import os
import base64

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')
KEY = "2010"


def xor_encrypt(text: str, key: str) -> bytes:
    return bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])


cipher_bytes = xor_encrypt(FLAG, KEY)
cipher_b64 = base64.b64encode(cipher_bytes).decode()

os.makedirs('dist', exist_ok=True)
with open('dist/wak.txt', 'w', encoding='utf-8') as f:
    f.write("Una nota antigua acompaña un archivo protegido.\n")
    f.write("Habla de una voz colombiana, un ritmo africano y un canto que unió al mundo.\n")
    f.write("El número no está escrito: está en el momento en que todo ocurrió.\n\n")
    f.write("Mensaje:\n")
    f.write(cipher_b64 + "\n")

print(f"[build] wak.txt generado ({len(FLAG)} chars)")
