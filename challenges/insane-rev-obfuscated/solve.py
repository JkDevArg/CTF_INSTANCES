"""
Solucion: insane-rev-obfuscated — ObfCorp Python Layers
========================================================

El checker.py tiene 3 capas de ofuscacion:
  Capa 0 → Capa 1 → Capa 2 → Capa 3 (nucleo)

Cada capa: base64 decode → zlib decompress → marshal.loads → code object

El nucleo (capa 3) contiene:
  _s = FLAG[::-1]    # flag invertida como string literal
  if input()[::-1] == _s: ...

Para obtener la flag: extraer _s de co_consts y revertir.

Tecnicas alternativas:
  1. Parchear exec() en tiempo de ejecucion para loggear code objects
  2. Analisis estatico del bytecode con dis.dis()
  3. Este script automatizado
"""

import zlib
import marshal
import base64
import dis
import re
import sys
import types

SCRIPT = './checker.py'


def extract_b64_payload(source: str) -> str | None:
    """Extrae el string base64 de una asignacion _=... o _d=..."""
    # Buscar patrones: _='...' o _d='...' o _="..."
    patterns = [
        r"^_\s*=\s*'([A-Za-z0-9+/=\n]+)'",
        r'^_\s*=\s*"([A-Za-z0-9+/=\n]+)"',
        r"^_d\s*=\s*'([A-Za-z0-9+/=\n]+)'",
        r'^_d\s*=\s*"([A-Za-z0-9+/=\n]+)"',
    ]
    for pat in patterns:
        m = re.search(pat, source, re.MULTILINE)
        if m:
            return m.group(1).replace('\n', '')
    return None


def unpack_layer(b64_data: str) -> types.CodeType:
    """Decodifica base64 → zlib → marshal → code object."""
    raw = base64.b64decode(b64_data)
    decompressed = zlib.decompress(raw)
    code = marshal.loads(decompressed)
    return code


def find_flag_in_consts(code: types.CodeType, depth: int = 0) -> str | None:
    """
    Busca recursivamente en co_consts de un code object
    un string que al invertirse tenga formato CTF{...}.
    """
    indent = "  " * depth
    for const in code.co_consts:
        if isinstance(const, str) and len(const) > 5:
            # Verificar si es la flag invertida
            reversed_candidate = const[::-1]
            if reversed_candidate.startswith('CTF{') and reversed_candidate.endswith('}'):
                print(f"{indent}[+] String invertido encontrado: {const!r}")
                print(f"{indent}[+] Flag: {reversed_candidate}")
                return reversed_candidate
            # Tambien verificar si el string mismo es la flag (por si no esta invertido)
            if const.startswith('CTF{') and const.endswith('}'):
                print(f"{indent}[+] Flag encontrada directamente: {const}")
                return const
        # Recursion sobre code objects anidados
        if isinstance(const, types.CodeType):
            result = find_flag_in_consts(const, depth + 1)
            if result:
                return result
    return None


def disassemble_and_search(code: types.CodeType, layer: int) -> str | None:
    """Desensambla un code object y busca la flag en sus constantes."""
    print(f"\n[*] === Capa {layer} ===")
    print(f"    co_filename: {code.co_filename}")
    print(f"    co_consts count: {len(code.co_consts)}")

    # Buscar flag en constantes de esta capa
    flag = find_flag_in_consts(code)
    if flag:
        return flag

    # Intentar extraer el payload de la siguiente capa desde co_consts
    for const in code.co_consts:
        if isinstance(const, str) and len(const) > 100:
            # Puede ser un payload base64 de la siguiente capa
            try:
                next_code = unpack_layer(const)
                print(f"[*] Payload base64 desempaquetado en capa {layer} -> capa {layer + 1}")
                result = disassemble_and_search(next_code, layer + 1)
                if result:
                    return result
            except Exception:
                pass

    return None


def method_intercept():
    """
    Metodo alternativo: ejecutar el script interceptando exec() en builtins.
    Captura todos los code objects que exec() recibe y los analiza.
    """
    print("\n[*] Metodo alternativo: interceptar exec() en runtime")
    captured_codes = []
    original_exec = __builtins__.__dict__['exec'] if isinstance(__builtins__, dict) else exec

    def fake_exec(code, globs=None, locs=None):
        if isinstance(code, types.CodeType):
            captured_codes.append(code)
        if globs is None:
            globs = {}
        if locs is None:
            locs = globs
        try:
            original_exec(code, globs, locs)
        except Exception:
            pass

    import builtins
    builtins.exec = fake_exec

    try:
        with open(SCRIPT) as f:
            src = f.read()
        # Ejecutar parcialmente para capturar las capas (sin llegar al input())
        exec(compile(src.replace('input(', '_STOP_('), '<checker>', 'exec'), {'_STOP_': lambda p: (_ for _ in ()).throw(StopIteration())})
    except (StopIteration, Exception):
        pass

    builtins.exec = original_exec

    print(f"[*] exec() interceptado {len(captured_codes)} veces")
    for i, code in enumerate(captured_codes):
        print(f"\n[*] Code object #{i}: filename={code.co_filename}")
        flag = find_flag_in_consts(code)
        if flag:
            return flag
    return None


def main():
    print("[*] Solucion: insane-rev-obfuscated")
    print("[*] Script:", SCRIPT)
    print()

    try:
        with open(SCRIPT) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[!] '{SCRIPT}' no encontrado.")
        print("[*] Descargalo del servidor y coloca solve.py en el mismo directorio.")
        sys.exit(1)

    print(f"[*] Script cargado: {len(content)} bytes")
    print()

    # ── Metodo 1: analisis estatico capa por capa ────────────────────────────
    print("[*] Metodo 1: analisis estatico (desempaquetar capas)")

    b64_payload = extract_b64_payload(content)
    if not b64_payload:
        print("[-] No se pudo extraer payload base64 de la capa 0.")
        print("[*] Intentando metodo de intercepcion...")
        flag = method_intercept()
    else:
        print(f"[*] Payload capa 0 extraido: {len(b64_payload)} chars")
        try:
            layer1_code = unpack_layer(b64_payload)
            flag = disassemble_and_search(layer1_code, layer=1)
        except Exception as e:
            print(f"[-] Error al desempaquetar capa 0: {e}")
            flag = None

    if not flag:
        print("\n[*] Metodo 1 no encontro la flag. Intentando intercepcion de exec()...")
        flag = method_intercept()

    if flag:
        print(f"\n[+] ==========================================")
        print(f"[+] FLAG: {flag}")
        print(f"[+] ==========================================")
    else:
        print("\n[-] Analisis automatico no pudo extraer la flag.")
        print("[*] Sugerencias manuales:")
        print("    python3 -c \"")
        print("    import zlib,marshal,base64,dis")
        print("    # Extraer el string _ del checker.py y:")
        print("    code = marshal.loads(zlib.decompress(base64.b64decode(_)))")
        print("    dis.dis(code)  # buscar LOAD_CONST con string largo")
        print("    \"")


if __name__ == '__main__':
    main()
