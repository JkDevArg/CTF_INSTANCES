"""
Solucion: hard-misc-polyglot

El archivo artifact-7734.png es simultaneamente:
- Un PNG valido (el formato ZIP no rompe PNG, los parsers ignoran datos extra al final)
- Un ZIP valido (ZIP lee desde el FINAL del archivo — End of Central Directory record)

Por que funciona:
  - PNG: lee desde el inicio, para en el chunk IEND, ignora el resto
  - ZIP: busca la firma del End of Central Directory desde el final del archivo

Extraccion:
  Opcion A (linea de comandos): unzip artifact-7734.png
  Opcion B (Python): zipfile module
  Opcion C (herramienta): binwalk artifact-7734.png -e
"""
import zipfile, sys

filename = 'artifact-7734.png'

print(f"[*] Intentando leer {filename} como ZIP...")
try:
    with zipfile.ZipFile(filename) as zf:
        print(f"[*] Archivos en el ZIP: {zf.namelist()}")
        flag = zf.read('flag.txt').decode().strip()
        print(f"[+] Flag: {flag}")
except zipfile.BadZipFile:
    print("[-] No es un ZIP valido")
    sys.exit(1)

# Tambien funciona desde la linea de comandos:
# unzip artifact-7734.png
# python3 -c "import zipfile; print(zipfile.ZipFile('artifact-7734.png').read('flag.txt').decode())"
