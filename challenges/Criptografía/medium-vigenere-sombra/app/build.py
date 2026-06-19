import os

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')
KEY = "SOMBRA"


def vigenere_encrypt(text: str, key: str) -> str:
    result = []
    key = key.upper()
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            if char.isupper():
                encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(encrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)


PLAINTEXT_TEMPLATE = """PROLOGO: Los archivos del Ministerio de Sombras
Clasificacion: Maximo Secreto

En los archivos sellados del antiguo Ministerio de Sombras yace un documento
que nadie deberia leer en voz alta. El agente conocido solo como La Sombra
paso decadas enteras operando en las grietas oscuras del poder, silenciando
verdades incomodas y borrando rastros de quienes osaban cuestionar el orden.

Su metodo era elegante en su simpleza: un cifrado antiguo recuperado de los
pergaminos de la Europa medieval, una clave personal que solo el conocia,
y un legado de secretos que se extendia por tres continentes.

La ultima comunicacion que envio antes de desvanecerse contiene lo siguiente:
{flag}

Quien logre descifrar estas palabras habra caminado la senda que recorrio.
La clave siempre estuvo en su nombre, en su apodo, en lo que siempre fue.
Busca en la sombra. La respuesta siempre estuvo ahi, esperando en silencio.
"""

plaintext = PLAINTEXT_TEMPLATE.format(flag=FLAG)
ciphertext = vigenere_encrypt(plaintext, KEY)

os.makedirs('dist', exist_ok=True)
with open('dist/diario.txt', 'w', encoding='utf-8') as f:
    f.write(ciphertext)

print(f"[build] diario.txt generado ({len(plaintext)} chars, flag embebida)")
