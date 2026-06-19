# MateVM

| Field      | Value                        |
|------------|------------------------------|
| Category   | Reversing                    |
| Difficulty | Medium                       |
| Docker     | Yes                          |
| Port       | 80 (host default: 8080)      |

## Description

Un desarrollador creó un sistema de verificación de licencias en Rust. Afirma que nadie puede romperlo porque no hay comparación directa de la flag. Demuéstrale que está equivocado.

El binario implementa una VM personalizada que ejecuta un programa de verificación de licencias. El bytecode de la VM está cifrado con XOR usando la clave `matevm`. Los jugadores deben descifrar el bytecode, comprender las instrucciones de la VM y reconstruir la licencia válida.

## Files

| File          | Description                                   |
|---------------|-----------------------------------------------|
| `reto/matevm` | Binario Rust ELF x86-64 (324,472 bytes)       |
| `reto/README.md` | Descripción original del reto              |
| `solucion/solve.py` | Script de solución de referencia       |
| `solucion/writeup.md` | Writeup detallado                    |

Note: the flag is static — baked into the pre-compiled binary. The FLAG env var is not used during build.

## Vulnerability / Solution

1. Descargar `matevm` (binario Linux ELF x86-64).
2. Abrir en Ghidra o IDA Pro.
3. Localizar el bytecode cifrado embebido.
4. Aplicar XOR con clave `matevm` para descifrar.
5. Analizar las instrucciones de la VM personalizada.
6. Reconstruir la licencia válida a partir de las restricciones.
7. Ejecutar: `echo "H4L{...}" | ./matevm` → `Acceso concedido.`

## How to run

```bash
# Build and start
docker compose up --build -d

# Access
http://localhost:8080

# Stop
docker compose down
```
