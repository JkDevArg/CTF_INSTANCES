# MateVM v2

| Field      | Value                        |
|------------|------------------------------|
| Category   | Reversing                    |
| Difficulty | Hard                         |
| Docker     | Yes                          |
| Port       | 80 (host default: 8080)      |

## Description

El desarrollador aprendió de sus errores. Esta vez no hay reversión byte a byte. El estado es continuo y los checkpoints comprueban consistencia global. Esta vez necesitarás más que paciencia.

VM Rust con operaciones con estado continuo (rolling state) y checkpoints de consistencia global. El charset del cuerpo de la flag está restringido. Requiere Z3 o similar para extraer y resolver las restricciones.

## Files

| File               | Description                                    |
|--------------------|------------------------------------------------|
| `reto/matevm2`     | Binario Rust ELF x86-64 stripped (331 KB)      |
| `reto/README.md`   | Descripción original del reto                  |
| `solucion/solve_v2.py` | Script de solución de referencia (Z3)      |
| `solucion/writeup_v2.md` | Writeup detallado                        |

Note: the flag is static — baked into the pre-compiled binary. The FLAG env var is not used during build.

## Vulnerability / Solution

1. Descargar `matevm2` (binario Linux ELF x86-64, stripped).
2. Abrir en Ghidra o IDA Pro.
3. Identificar el loop de la VM y las operaciones con estado continuo.
4. Localizar los checkpoints de consistencia global.
5. Modelar las restricciones con Z3.
6. Resolver: `python3 solve_v2.py` → obtiene la licencia válida.
7. Verificar: `echo "H4L{...}" | ./matevm2` → `Acceso concedido.`

## How to run

```bash
# Build and start
docker compose up --build -d

# Access
http://localhost:8080

# Stop
docker compose down
```
