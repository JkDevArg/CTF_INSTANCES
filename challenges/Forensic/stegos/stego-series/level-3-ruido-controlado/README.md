# Ecos Ocultos: Ruido Controlado

## Tabla de información

| Campo       | Valor                              |
|-------------|------------------------------------|
| ID          | forensic-stego-ruido               |
| Nombre      | Ecos Ocultos: Ruido Controlado     |
| Categoría   | Forensic                           |
| Dificultad  | Hard                               |
| Puerto      | 80                                 |
| Timeout     | 3600 s                             |
| Flag        | H4L{NO_TODO_RUIDO_ES_AZAR}         |

## Descripción

La imagen parece ruido aleatorio. No lo es. La flag está oculta en el LSB del canal rojo, pero los píxeles están desordenados (shuffled) según una semilla derivada de `mate320320`. El payload está comprimido con zlib, tiene un magic header `H4LSTEG2` y CRC32, y está XOR-cifrado con un keystream SHA-256.

## Vulnerabilidad

Combinación de tres capas de ofuscación:
1. **Orden de píxeles aleatorio** — los bits no están en posición secuencial sino en un orden determinado por `random.Random(seed).shuffle(indices)` donde `seed = sha256("mate320320")[:8]`.
2. **XOR stream cipher** — keystream generado por bloques SHA-256 con contador.
3. **Compresión zlib + estructura binaria** con magic, longitud, CRC32.

## Solución

```python
import binascii, hashlib, random, struct, zlib
from PIL import Image

img = Image.open("ruido.png").convert("RGB")
pixels = list(img.getdata())
width, height = img.size  # 320, 320

key = f"mate{width}{height}".encode()
key_material = hashlib.sha256(key).digest()
seed = int.from_bytes(key_material[:8], "big")

# Reconstruir orden de indices
indices = list(range(len(pixels)))
rng = random.Random(seed)
rng.shuffle(indices)

# Extraer LSB del canal rojo en el orden correcto
bits = []
for pixel_index in indices:
    r, g, b = pixels[pixel_index]
    bits.append(r & 1)

# Reconstruir bytes del payload cifrado
raw = bytearray()
for i in range(0, len(bits) - 7, 8):
    byte = 0
    for bit in bits[i:i+8]:
        byte = (byte << 1) | bit
    raw.append(byte)

# XOR stream descifrado
def xor_stream(data, km):
    stream = bytearray()
    c = 0
    while len(stream) < len(data):
        stream.extend(hashlib.sha256(km + c.to_bytes(4, "big")).digest())
        c += 1
    return bytes(a ^ b for a, b in zip(data, stream))

decrypted = xor_stream(bytes(raw), key_material)

# Parsear estructura
MAGIC = b"H4LSTEG2"
assert decrypted[:8] == MAGIC
length = struct.unpack(">I", decrypted[8:12])[0]
compressed = decrypted[12:12+length]
crc_stored = struct.unpack(">I", decrypted[12+length:16+length])[0]
assert binascii.crc32(compressed) & 0xFFFFFFFF == crc_stored
flag = zlib.decompress(compressed).decode()
print("FLAG:", flag)
```

## Cómo ejecutar

```bash
FLAG="H4L{NO_TODO_RUIDO_ES_AZAR}" docker compose up --build
# Servidor en http://localhost:8080
PORT_80=9094 FLAG="H4L{mi_flag}" docker compose up --build
```
