#!/usr/bin/env python3
"""
Solución de referencia para easy-misc-qr.
Uso: descarga codigo.png del servidor y ejecuta este script.
  python3 solve.py codigo.png

Dependencias:
  pip install pyzbar pillow
  (Linux): apt install libzbar0
"""
import sys

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'codigo.png'

    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
    except ImportError:
        print("[-] Faltan dependencias. Instala con:")
        print("    pip install pyzbar pillow")
        print("    (Linux) apt install libzbar0")
        sys.exit(1)

    img = Image.open(path)
    results = decode(img)

    if not results:
        print("[-] No se pudo decodificar el QR. Intenta con una herramienta online.")
        sys.exit(1)

    for r in results:
        flag = r.data.decode('utf-8')
        print(f"[+] FLAG: {flag}")


if __name__ == '__main__':
    main()
