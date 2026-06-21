# Writeup — bit_por_bit

## Idea

La flag está en el bit menos significativo del canal azul. El payload no es la flag directa: primero se aplica `base64(flag)` y luego XOR con la clave `mate`.

## Resolución esperada

1. Extraer LSB del canal azul.
2. Reagrupar los bits en bytes.
3. Aplicar XOR con `mate`.
4. Cortar en `::END::`.
5. Decodificar base64.

## Script mínimo

```python
from PIL import Image
import base64

img = Image.open("player/mural.png").convert("RGB")
key = b"mate"
raw = bytearray()
bits = [b & 1 for _, _, b in img.getdata()]

for i in range(0, len(bits), 8):
    chunk = bits[i:i+8]
    if len(chunk) < 8:
        break
    value = 0
    for bit in chunk:
        value = (value << 1) | bit
    raw.append(value)

decoded = bytes(c ^ key[i % len(key)] for i, c in enumerate(raw))
payload = decoded.split(b"::END::", 1)[0]
print(base64.b64decode(payload).decode())
```
