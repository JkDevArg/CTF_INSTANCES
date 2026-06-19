"""
Solucion: insane-rev-antidbg — AntiDbg Corp v2
===============================================

El binario tiene dos protecciones anti-debug:
  1. ptrace(PTRACE_TRACEME) self-check
  2. timing check (busy-loop de 1M iter, umbral 500ms)

La flag esta codificada con XOR 0x1F en encoded_flag[]
en la seccion .data del binario ELF x86-64 compilado con -no-pie.

Estrategia 1 — Analisis estatico (sin ejecutar el binario):
  Buscar en el binario la secuencia de bytes que XOR 0x1F produce "CTF{".
  No requiere bypass de anti-debug.

Estrategia 2 — LD_PRELOAD ptrace bypass:
  Compilar una libreria que overridea ptrace() para siempre retornar 0.
  LD_PRELOAD=./bypass_ptrace.so ./antidbg
  (No usar single-step para evitar el timing check)

Estrategia 3 — NOP patching:
  Abrir el binario en un editor hex.
  Buscar el call a ptrace y parchear el je/jne que sigue al check.
  Con pwntools: elf.write(offset, b'\\x90\\x90') para NOP los saltos.

Estrategia 4 — objdump:
  objdump -s -j .data antidbg | grep -A 4 'Contents of section'
  Extraer los bytes y XOR con 0x1F manualmente.
"""

import sys
import subprocess

BINARY = './antidbg'
XOR_KEY = 0x1F
FLAG_PREFIX = 'CTF{'


def xor_search(data: bytes, key: int, prefix: str) -> list[str]:
    """Busca en data secuencias que XOR key produzcan prefix."""
    target = bytes([ord(c) ^ key for c in prefix])
    results = []
    idx = 0
    while True:
        idx = data.find(target, idx)
        if idx == -1:
            break
        candidate = []
        i = idx
        while i < len(data) and i < idx + 512:
            decoded = data[i] ^ key
            # Acepta caracteres ASCII printable
            if decoded < 0x20 or decoded > 0x7e:
                break
            candidate.append(chr(decoded))
            if chr(decoded) == '}':
                break
            i += 1
        if len(candidate) > len(prefix):
            results.append(''.join(candidate))
        idx += 1
    return results


def generate_ld_preload_bypass():
    """Genera y compila una libreria LD_PRELOAD que bypasea ptrace."""
    bypass_c = """
#include <sys/ptrace.h>
#include <stdarg.h>

/* Override ptrace: siempre retorna 0 (exito) para que el check no active */
long ptrace(enum __ptrace_request request, ...) {
    return 0;
}
"""
    bypass_src = '/tmp/bypass_ptrace.c'
    bypass_so  = '/tmp/bypass_ptrace.so'

    try:
        with open(bypass_src, 'w') as f:
            f.write(bypass_c)

        result = subprocess.run(
            ['gcc', '-shared', '-fPIC', '-o', bypass_so, bypass_src],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"[+] Libreria LD_PRELOAD compilada: {bypass_so}")
            print(f"[*] Para usar (no usar single-step para evitar timing check):")
            print(f"    LD_PRELOAD={bypass_so} {BINARY}")
            return bypass_so
        else:
            print(f"[-] No se pudo compilar la libreria: {result.stderr}")
    except FileNotFoundError:
        print("[-] gcc no encontrado. Instalar con: sudo apt install gcc")
    return None


def objdump_analysis():
    """Usa objdump para ver la seccion .data del binario."""
    try:
        result = subprocess.run(
            ['objdump', '-s', '-j', '.data', BINARY],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("[*] objdump .data output:")
            print(result.stdout[:2000])

            # Extraer bytes hexadecimales de objdump
            import re
            hex_bytes = []
            for line in result.stdout.splitlines():
                # Formato: " addr  xx xx xx xx xx xx xx xx xx xx xx xx xx xx xx xx  ................"
                m = re.match(r'\s+[0-9a-f]+\s+((?:[0-9a-f]{2} )+)', line)
                if m:
                    hex_str = m.group(1).strip().replace(' ', '')
                    hex_bytes.extend(bytes.fromhex(hex_str))

            if hex_bytes:
                data = bytes(hex_bytes)
                candidates = xor_search(data, XOR_KEY, FLAG_PREFIX)
                if candidates:
                    print(f"[+] Flag encontrada en .data via objdump:")
                    for c in candidates:
                        print(f"    {c}")
                    return candidates[0] if candidates else None
        else:
            print(f"[-] objdump error: {result.stderr[:200]}")
    except FileNotFoundError:
        print("[-] objdump no encontrado.")
    return None


def main():
    print("[*] Solucion: insane-rev-antidbg")
    print("[*] Binario:", BINARY)
    print()

    try:
        with open(BINARY, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"[!] '{BINARY}' no encontrado.")
        print("[*] Descargalo del servidor y coloca solve.py en el mismo directorio.")
        sys.exit(1)

    print(f"[*] Tamano del binario: {len(data):,} bytes")
    print()

    # ── Estrategia 1: busqueda estatica XOR ─────────────────────────────────
    print("[*] Estrategia 1: busqueda estatica XOR 0x1F para 'CTF{'")
    candidates = xor_search(data, XOR_KEY, FLAG_PREFIX)

    if candidates:
        valid = [c for c in candidates if c.startswith('CTF{') and c.endswith('}')]
        print(f"[+] {len(candidates)} candidato(s) encontrado(s):")
        for c in candidates:
            closed = " (completo)" if c.endswith('}') else " (sin cierre)"
            print(f"    {c}{closed}")

        if valid:
            best = max(valid, key=len)
            print(f"\n[+] ==========================================")
            print(f"[+] FLAG: {best}")
            print(f"[+] ==========================================")
            return
    else:
        print("[-] Patron XOR no encontrado con busqueda directa en el binario completo.")
        print("[*] Intentando via objdump (.data solamente)...")
        flag = objdump_analysis()
        if flag:
            return

    # ── Estrategia 2: LD_PRELOAD ─────────────────────────────────────────────
    print()
    print("[*] Estrategia 2: generar libreria LD_PRELOAD para bypass de ptrace")
    bypass_so = generate_ld_preload_bypass()

    # ── Estrategia 3: instrucciones manuales ─────────────────────────────────
    print()
    print("[*] Estrategia 3: analisis manual con Ghidra / radare2")
    print("    1. Cargar el binario en Ghidra (File > Import > antidbg)")
    print("    2. Buscar la funcion check_flag (Symbol Tree > Functions)")
    print("    3. En check_flag, localizar la referencia a encoded_flag[]")
    print("    4. Ver el valor de encoded_flag[] en la ventana de datos")
    print("    5. Copiar los bytes y XOR con 0x1F:")
    print(f"       python3 -c \"")
    print(f"       encoded = [0x5c, 0x5b, 0x4f, ...]  # bytes de encoded_flag[]")
    print(f"       print(''.join(chr(b ^ 0x{XOR_KEY:02X}) for b in encoded))\"")
    print()
    print("[*] Estrategia 4: radare2")
    print("    r2 antidbg")
    print("    [0x]> aaa          # analizar")
    print("    [0x]> iz           # strings en seccion de datos")
    print("    [0x]> pd @ sym.check_flag  # disassembly de check_flag")


if __name__ == '__main__':
    main()
