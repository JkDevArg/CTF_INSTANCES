# NetSec Corp — ret2libc

| Campo       | Valor                              |
|-------------|------------------------------------|
| Categoría   | PWN                                |
| Dificultad  | Hard                               |
| Técnica     | ret2libc — ROP chain con leak de libc |
| Docker      | Sí                                 |
| Puertos     | 9999 (nc), 80 (web)               |

## Descripción

El binario `target` tiene un buffer overflow clásico. No existe función `win()`.
NX está habilitado, por lo que no se puede ejecutar shellcode en el stack.
El reto requiere construir un ROP chain en dos etapas:

1. **Stage 1**: Llamar `puts(got['puts'])` para filtrar la dirección real de `puts` en libc.
2. **Stage 2**: Calcular la base de libc, luego llamar `system("/bin/sh")`.

## Vulnerabilidad

```c
char buf[64];
read(STDIN_FILENO, buf, 256);  // overflow: 256 bytes into 64
```

Offset a RIP: `64 (buffer) + 8 (saved rbp) = 72 bytes`.

## Archivos disponibles

- `target` — binario ELF 64-bit (PIE=off, NX=on, sin canary)
- `libc.so.6` — la misma libc del servidor (Ubuntu 22.04 glibc 2.35)

## Solución rápida

```bash
python3 solve.py REMOTE <host> <port_9999>
```

## Cómo ejecutar

```bash
FLAG="CTF{test_flag}" docker compose up --build
```

Acceder al panel de descargas en `http://localhost:8080`.
Conectar al servicio con `nc localhost 9999`.
