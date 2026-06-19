# Referencia: solución esperada para medium-vigenere-sombra
# La clave es SOMBRA

KEY = "SOMBRA"


def vigenere_decrypt(ciphertext, key):
    result = []
    key = key.upper()
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            if char.isupper():
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            result.append(decrypted)
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)


with open('diario.txt') as f:
    ciphertext = f.read()

plaintext = vigenere_decrypt(ciphertext, KEY)
print(plaintext)

# Extract flag
import re
match = re.search(r'CTF\{[^}]+\}', plaintext)
if match:
    print(f"\nFlag: {match.group()}")
