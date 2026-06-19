import os
import base64
from PIL import Image, ImageDraw

FLAG = os.environ.get('FLAG', 'H4L{LSB_ESCONDIDO_EN_AZUL}')
KEY = b"mate"
MARKER = b"::END::"


def xor_bytes(data, key):
    return bytes(byte ^ key[i % len(key)] for i, byte in enumerate(data))


def bits_from_bytes(data):
    bits = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def build_cover(width=320, height=320):
    img = Image.new("RGB", (width, height), (16, 18, 28))
    draw = ImageDraw.Draw(img)
    tile = 20
    colors = [(214, 80, 118), (236, 178, 45), (54, 145, 140), (94, 112, 201)]
    for y in range(0, height, tile):
        for x in range(0, width, tile):
            idx = ((x // tile) + (y // tile)) % len(colors)
            draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=colors[idx])
    for offset in range(0, width, 16):
        draw.line((offset, 0, width - offset // 2, height), fill=(255, 255, 255), width=1)
    return img


os.makedirs('dist', exist_ok=True)
cover = build_cover()
payload = xor_bytes(base64.b64encode(FLAG.encode()) + MARKER, KEY)
bits = bits_from_bytes(payload)
img = cover.copy().convert("RGB")
pixels = list(img.getdata())
new_pixels = []
for idx, (r, g, b) in enumerate(pixels):
    if idx < len(bits):
        b = (b & 0xFE) | bits[idx]
    new_pixels.append((r, g, b))
img.putdata(new_pixels)
img.save('dist/mural.png')
print(f'[build] mural.png creado, {len(payload)} bytes embebidos en LSB azul')
