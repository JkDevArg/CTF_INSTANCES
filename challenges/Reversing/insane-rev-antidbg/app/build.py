"""
build.py — insane-rev-antidbg
Lee la FLAG del entorno, genera flag_data.c con el array XOR 0x1F,
y compila challenge.c + flag_data.c en el binario /app/dist/antidbg.
"""
import os
import subprocess
import shutil

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# Generar el array XOR 0x1F
encoded = [ord(c) ^ 0x1F for c in FLAG]
array_init = ', '.join(f'0x{b:02x}' for b in encoded)

flag_data_src = f"""/* flag_data.c — generado por build.py (no editar manualmente) */
unsigned char encoded_flag[] = {{{array_init}}};
int encoded_flag_len = {len(encoded)};
"""

# Crear directorio temporal de build
build_dir = '/tmp/antidbg_build'
os.makedirs(build_dir, exist_ok=True)
os.makedirs('/app/dist', exist_ok=True)

# Escribir flag_data.c
flag_data_path = os.path.join(build_dir, 'flag_data.c')
with open(flag_data_path, 'w') as f:
    f.write(flag_data_src)

# Copiar challenge.c al directorio de build
challenge_src = '/app/challenge.c'
challenge_dst = os.path.join(build_dir, 'challenge.c')
shutil.copy2(challenge_src, challenge_dst)

# Compilar
print(f"[*] Compilando antidbg...")
print(f"    FLAG length: {len(FLAG)} chars")
print(f"    Encoded bytes: [{', '.join(hex(b) for b in encoded[:6])}{'...' if len(encoded) > 6 else ''}]")

result = subprocess.run(
    [
        'gcc',
        '-O2',
        '-no-pie',
        '-fno-stack-protector',
        '-fno-pic',
        challenge_dst,
        flag_data_path,
        '-o', '/app/dist/antidbg',
    ],
    capture_output=True,
    text=True,
)

if result.returncode != 0:
    print("[!] Compile error:")
    print(result.stderr)
    raise SystemExit(1)

os.chmod('/app/dist/antidbg', 0o555)
size = os.path.getsize('/app/dist/antidbg')
print(f"[+] Binary compiled: /app/dist/antidbg ({size:,} bytes)")

# Verificar que el array esta en el binario
with open('/app/dist/antidbg', 'rb') as f:
    binary_data = f.read()

target = bytes([ord(c) ^ 0x1F for c in 'CTF{'])
if target in binary_data:
    print(f"[+] XOR array verificado en el binario (busqueda estatica posible)")
else:
    print(f"[!] Advertencia: el patron XOR no fue encontrado con busqueda directa")
