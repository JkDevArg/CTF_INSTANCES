# Ecos Ocultos: Bit por Bit

## Tabla de información

| Campo       | Valor                          |
|-------------|--------------------------------|
| ID          | forensic-stego-bit-por-bit     |
| Nombre      | Ecos Ocultos: Bit por Bit      |
| Categoría   | Forensic                       |
| Dificultad  | Medium                         |
| Puerto      | 80                             |
| Timeout     | 3600 s                         |
| Flag        | H4L{LSB_ESCONDIDO_EN_AZUL}     |

## Descripción

Un mural digital fue interceptado. Visualmente parece normal. La flag está oculta en el bit menos significativo (LSB) del canal azul, XOR-cifrada con la clave `mate` y terminada en el marcador `::END::`.

## Vulnerabilidad

Esteganografía LSB clásica, pero solo en el canal azul (no en rojo ni verde). El payload está XOR-cifrado con una clave corta (`mate`) y codificado en Base64 antes de la incrustación. Sin conocer el canal correcto y la clave, las herramientas automáticas fallan.

## Solución

```python
from PIL import Image
import base64

KEY = b"mate"
MARKER = b"::END::"

img = Image.open("mural.png").convert("RGB")
pixels = list(img.getdata())

# Extraer LSB del canal azul
bits = [(b & 1) for (r, g, b) in pixels]

# Reconstruir bytes
raw = bytearray()
for i in range(0, len(bits) - 7, 8):
    byte = 0
    for bit in bits[i:i+8]:
        byte = (byte << 1) | bit
    raw.append(byte)

# XOR con clave
decrypted = bytes(raw[i] ^ KEY[i % len(KEY)] for i in range(len(raw)))

# Cortar en marcador y decodificar Base64
end = decrypted.find(MARKER)
if end != -1:
    flag = base64.b64decode(decrypted[:end]).decode()
    print("FLAG:", flag)
```

## Cómo ejecutar

```bash
FLAG="H4L{LSB_ESCONDIDO_EN_AZUL}" docker compose up --build
# Servidor en http://localhost:8080
PORT_80=9093 FLAG="H4L{mi_flag}" docker compose up --build
```
