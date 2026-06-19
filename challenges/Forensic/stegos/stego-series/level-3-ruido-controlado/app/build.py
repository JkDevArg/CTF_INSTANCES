import os
import binascii
import hashlib
import random
import struct
import zlib
from PIL import Image

FLAG = os.environ.get('FLAG', 'H4L{NO_TODO_RUIDO_ES_AZAR}')
MAGIC = b"H4LSTEG2"
SIZE = (320, 320)


def xor_stream(data, key_material):
    stream = bytearray()
    counter = 0
    while len(stream) < len(data):
        block = hashlib.sha256(key_material + counter.to_bytes(4, "big")).digest()
        stream.extend(block)
        counter += 1
    return bytes(a ^ b for a, b in zip(data, stream))


def bits_from_bytes(data):
    bits = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def build_cover(width, height):
    rng = random.Random(0xEC05)
    img = Image.new("RGB", (width, height))
    pixels = []
    for y in range(height):
        for x in range(width):
            base = int(90 + 60 * ((x ^ y) % 17) / 16)
            pixels.append((
                (base + rng.randrange(0, 96)) % 256,
                (base + rng.randrange(32, 160)) % 256,
                (base + rng.randrange(64, 192)) % 256,
            ))
    img.putdata(pixels)
    return img


os.makedirs('dist', exist_ok=True)
width, height = SIZE
cover = build_cover(width, height)
key = f"mate{width}{height}".encode()
key_material = hashlib.sha256(key).digest()
seed = int.from_bytes(key_material[:8], "big")
compressed = zlib.compress(FLAG.encode())
crc = binascii.crc32(compressed) & 0xFFFFFFFF
payload = MAGIC + struct.pack(">I", len(compressed)) + compressed + struct.pack(">I", crc)
encrypted = xor_stream(payload, key_material)
bits = bits_from_bytes(encrypted)
img = cover.copy().convert("RGB")
pixels = list(img.getdata())
indices = list(range(len(pixels)))
rng = random.Random(seed)
rng.shuffle(indices)
for bit_index, pixel_index in enumerate(indices[:len(bits)]):
    r, g, b = pixels[pixel_index]
    pixels[pixel_index] = ((r & 0xFE) | bits[bit_index], g, b)
img.putdata(pixels)
img.save('dist/ruido.png')
with open('dist/nota.txt', 'w', encoding='utf-8') as f:
    f.write("No mires la imagen de izquierda a derecha.\n")
    f.write("El orden correcto nace de: mate + dimensiones.\n")
print(f'[build] ruido.png y nota.txt creados')
