# easy-misc-qr — Lab 404

## Descripción
El servidor genera un código QR (PNG) que codifica el FLAG directamente. El jugador descarga la imagen y la decodifica con cualquier escáner QR.

## Mecánica
- `build.py` usa `qrcode` con corrección de error alta (`ERROR_CORRECT_H`) para mayor robustez.
- La imagen resultante `codigo.png` se sirve para descarga vía Flask.

## Cómo decodificar

### Opción A — Herramientas online
Sube `codigo.png` a cualquier decoder QR en línea:
- https://zxing.org/w/decode.jspx
- https://qr-scanner.org/

### Opción B — Python con pyzbar
```bash
pip install pyzbar pillow
# Linux también requiere: apt install libzbar0
python3 solve.py codigo.png
```

### Opción C — Escáner de smartphone
Abre la cámara y apunta al código QR de la imagen.

## Dificultad
Fácil — el único reto es encontrar una herramienta de decodificación QR.
