# Ecos Ocultos: Postal

## Tabla de información

| Campo       | Valor                          |
|-------------|--------------------------------|
| ID          | forensic-stego-postal          |
| Nombre      | Ecos Ocultos: Postal           |
| Categoría   | Forensic                       |
| Dificultad  | Easy                           |
| Puerto      | 80                             |
| Timeout     | 3600 s                         |
| Flag        | H4L{METADATA_NO_ES_BASURA}     |

## Descripción

Una postal digital fue capturada. A simple vista no revela nada. Pero las imágenes guardan más de lo que muestran. La flag está oculta en los metadatos PNG del archivo `postal.png`.

## Vulnerabilidad

El archivo PNG contiene un campo de texto `Comment` con la flag codificada en Base64. Las herramientas estándar de análisis de metadatos (ExifTool, `pnginfo`, strings) revelan el campo directamente.

## Solución

```bash
# Opción 1 — ExifTool
exiftool postal.png | grep Comment
# → Comment: SDRMe1NUQUNLT0FOT19FU19CQVNVUEF9  (base64)
echo "SDRMe1NUQUNLT0FOT19FU19CQVNVUEF9" | base64 -d

# Opción 2 — Python
python3 -c "
from PIL import Image
img = Image.open('postal.png')
import base64
print(base64.b64decode(img.info['Comment']).decode())
"

# Opción 3 — strings
strings postal.png | grep -i comment
```

## Cómo ejecutar

```bash
FLAG="H4L{METADATA_NO_ES_BASURA}" docker compose up --build
# Servidor en http://localhost:8080
PORT_80=9092 FLAG="H4L{mi_flag}" docker compose up --build
```
