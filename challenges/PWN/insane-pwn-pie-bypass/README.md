# SafeBox Corp — PIE Partial Overwrite

| Campo       | Valor                                    |
|-------------|------------------------------------------|
| Categoría   | PWN                                      |
| Dificultad  | Insane                                   |
| Técnica     | PIE partial overwrite (2-byte brute force) |
| Docker      | Sí                                       |
| Puertos     | 9999 (nc), 80 (web)                     |

## Descripción

El binario `safebox` tiene PIE habilitado — las direcciones base del binario cambian con cada ejecución (ASLR).

Sin embargo, el buffer overflow permite exactamente **2 bytes** de sobrescritura sobre la dirección de retorno.

**Clave**: Los últimos 12 bits de cualquier dirección son deterministas (alineación de página). Solo el nibble superior de esos 2 bytes es aleatorio (4 bits = 16 posibles valores).

**Estrategia**: Brute force de los 16 posibles valores del nibble superior. En promedio, ~8 intentos para conseguir la flag.

## Vulnerabilidad

```c
char input[40];
read(STDIN_FILENO, input, 42);  // 42 bytes: 40 buffer + 2 bytes overwrite
```

Los 2 bytes extra sobreescriben la dirección de retorno guardada (parcialmente).

## Técnica

1. Analizar `safebox` con `objdump` o `ghidra` para encontrar el offset de `win()` dentro del binario (los últimos 12 bits son fijos).
2. Enviar 40 bytes de padding + 2 bytes de la dirección de `win()` (con los últimos 12 bits fijos y brute-force del nibble superior).
3. Repetir hasta obtener `SAFE OPENED`.

## Solución rápida

```bash
python3 solve.py              # local
python3 solve.py REMOTE <ip> <port>
```

## Cómo ejecutar

```bash
FLAG="CTF{test_flag}" docker compose up --build
```

Acceder al panel de descargas en `http://localhost:8080`.
Conectar al servicio con `nc localhost 9999`.
