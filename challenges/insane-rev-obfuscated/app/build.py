"""
build.py — insane-rev-obfuscated
Genera checker.py: un script Python con 3 capas de ofuscacion.

Capa 0 (visible): variable _ con datos base64, llama a exec(compile(marshal.loads(zlib...)))
Capa 1 (dentro): otro exec(compile(marshal.loads(zlib...))) con base64 distinto
Capa 2 (adentro): otro exec(compile(marshal.loads(zlib...)))
Capa 3 (nucleo): codigo Python que verifica input == FLAG invertido

Los jugadores deben:
  1. Extraer el string base64 de la capa 0
  2. Decodificar con base64 + zlib + marshal
  3. Ver el bytecode (dis.dis) o el source de capa 1
  4. Repetir para capa 2
  5. En la capa 3 descubrir la logica: inp[::-1] == secret
  6. Invertir secret para obtener la flag
"""
import os
import sys
import zlib
import marshal
import base64

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# ── CAPA 3 (nucleo): logica real ──────────────────────────────────────────────
# La flag se almacena invertida como string literal
# El checker pide input y compara inp[::-1] con el string invertido

inner_src = f'''import sys
_s = {repr(FLAG[::-1])}
_i = input("ObfCorp Checker > ")
if _i[::-1] == _s:
    print("[+] Correcto! Acceso concedido.")
else:
    print("[-] Incorrecto. Sigue intentando.")
'''

# Compilar nucleo a bytecode
layer3_code = compile(inner_src, '<layer3>', 'exec')
layer3_bytes = marshal.dumps(layer3_code)

# ── CAPA 2: zlib + base64 del nucleo ─────────────────────────────────────────
layer2_payload = base64.b64encode(zlib.compress(layer3_bytes, 9)).decode()

layer2_src = (
    "import zlib,marshal,base64\n"
    f"_d={repr(layer2_payload)}\n"
    "exec(compile(marshal.loads(zlib.decompress(base64.b64decode(_d))),'<layer3>','exec'))\n"
)

layer2_code = compile(layer2_src, '<layer2>', 'exec')
layer2_bytes = marshal.dumps(layer2_code)

# ── CAPA 1: zlib + base64 de capa 2 ──────────────────────────────────────────
layer1_payload = base64.b64encode(zlib.compress(layer2_bytes, 9)).decode()

layer1_src = (
    "import zlib,marshal,base64\n"
    f"_d={repr(layer1_payload)}\n"
    "exec(compile(marshal.loads(zlib.decompress(base64.b64decode(_d))),'<layer2>','exec'))\n"
)

layer1_code = compile(layer1_src, '<layer1>', 'exec')
layer1_bytes = marshal.dumps(layer1_code)

# ── CAPA 0 (archivo final): zlib + base64 de capa 1 ──────────────────────────
layer0_payload = base64.b64encode(zlib.compress(layer1_bytes, 9)).decode()

# Dividir el payload en lineas de 76 chars para mayor confusion visual
chunks = [layer0_payload[i:i+76] for i in range(0, len(layer0_payload), 76)]
payload_repr = repr(layer0_payload)

final_src = (
    "# CryptoCheck v3 -- Secure Validation Engine\n"
    "# (c) ObfCorp 2024 -- All rights reserved\n"
    "#\n"
    "# WARNING: This file is protected by ObfCorp IP layer.\n"
    "# Unauthorized decompilation is prohibited.\n"
    "#\n"
    "import zlib,marshal,base64 as _b\n"
    f"_={payload_repr}\n"
    "exec(compile(marshal.loads(zlib.decompress(_b.b64decode(_))),'<layer1>','exec'))\n"
)

os.makedirs('/app/dist', exist_ok=True)
out_path = '/app/dist/checker.py'
with open(out_path, 'w') as f:
    f.write(final_src)

print(f"[+] checker.py generado: {out_path} ({len(final_src)} bytes)")
