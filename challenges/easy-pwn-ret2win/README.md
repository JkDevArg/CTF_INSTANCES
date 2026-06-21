# VAULT Corp — ret2win

| Campo       | Valor                      |
|-------------|----------------------------|
| Categoría   | PWN                        |
| Dificultad  | Fácil                      |
| Técnica     | Stack Buffer Overflow / ret2win |
| Docker      | Sí                         |
| Puertos     | 9999 (nc), 80 (web)        |

## Descripción

El binario `vault` lee hasta 128 bytes en un buffer de 64. No hay PIE ni canary.
Existe una función `win()` que abre `/home/ctf/flag.txt` y la imprime.
El reto consiste en redirigir el flujo de ejecución hacia ella.

## Vulnerabilidad

```c
char code[64];
read(STDIN_FILENO, code, 128);   // overflow: 128 bytes into 64
```

Offset a RIP: `64 (buffer) + 8 (saved rbp) = 72 bytes`.

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
