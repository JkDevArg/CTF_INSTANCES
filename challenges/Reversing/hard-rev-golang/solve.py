"""
Solucion: hard-rev-golang — GoCrackMe v1.0
=========================================

El binario Go contiene la flag XOR-encoded con 0x42 como un literal
[]byte en el codigo fuente. El compilador Go embebe este array en la
seccion de datos del binario.

Estrategia 1 — Busqueda estatica del patron XOR:
  El array encoded[] contiene los bytes de la flag XOR 0x42.
  Buscamos la secuencia que, al XOR con 0x42, produce "CTF{".

Estrategia 2 — strings + patron:
  Aunque la flag no aparece literal, el array de bytes puede
  aparecer como una secuencia contigua en el binario.

Estrategia 3 — Ghidra + GoReSym:
  Cargar gocrackme en Ghidra.
  Aplicar el plugin GoReSym (Mandiant) para recuperar simbolos Go.
  Buscar la funcion main.deobfuscate y su llamada desde main.main.
  Extraer el argumento (el array encoded[]) y XOR con 0x42.

Estrategia 4 — GDB con bypass (sin anti-debug en este reto):
  gdb ./gocrackme
  b main.main
  run
  x/64xb <direccion del array>
"""

import struct
import sys

BINARY = './gocrackme'
XOR_KEY = 0x42
FLAG_PREFIX = 'CTF{'


def xor_search(data: bytes, key: int, prefix: str) -> list[str]:
    """Busca secuencias que al XOR con key produzcan el prefix dado."""
    target = bytes([ord(c) ^ key for c in prefix])
    results = []
    idx = 0
    while True:
        idx = data.find(target, idx)
        if idx == -1:
            break
        # Extraer hasta encontrar el terminador o un byte no printable
        candidate = []
        i = idx
        while i < len(data) and i < idx + 256:
            decoded = data[i] ^ key
            if decoded < 0x20 or decoded > 0x7e:
                break
            candidate.append(chr(decoded))
            if chr(decoded) == '}':
                break
            i += 1
        if candidate:
            results.append(''.join(candidate))
        idx += 1
    return results


def main():
    print("[*] Solucion: hard-rev-golang")
    print("[*] Binario:", BINARY)
    print()

    try:
        with open(BINARY, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"[!] Binario '{BINARY}' no encontrado.")
        print("[*] Descargalo del servidor y coloca el script en el mismo directorio.")
        sys.exit(1)

    print(f"[*] Tamano del binario: {len(data):,} bytes")
    print(f"[*] Buscando patron XOR 0x{XOR_KEY:02X} para '{FLAG_PREFIX}'...")
    print()

    candidates = xor_search(data, XOR_KEY, FLAG_PREFIX)

    if candidates:
        print(f"[+] {len(candidates)} candidato(s) encontrado(s):")
        for i, c in enumerate(candidates):
            print(f"    [{i}] {c}")
        print()
        # El candidato mas largo con formato CTF{...} es probablemente la flag
        valid = [c for c in candidates if c.startswith('CTF{') and c.endswith('}')]
        if valid:
            best = max(valid, key=len)
            print(f"[+] Flag: {best}")
        else:
            print("[*] Candidatos sin cierre '}':")
            for c in candidates:
                print(f"    {c}")
    else:
        print("[-] Patron XOR no encontrado con busqueda directa.")
        print("[*] El binario puede usar strips adicionales o ASLR.")
        print("[*] Usa Ghidra + GoReSym para analisis profundo:")
        print("    1. File > Import File > gocrackme")
        print("    2. Window > Script Manager > GoReSym.py")
        print("    3. Search > For Strings > 'deobfuscate'")
        print("    4. Extraer bytes del array encoded[] y XOR con 0x42")


if __name__ == '__main__':
    main()
