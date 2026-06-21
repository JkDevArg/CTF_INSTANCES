# MINIMALIST Corp — Raw Syscall ROP

| Campo       | Valor                                      |
|-------------|--------------------------------------------|
| Categoría   | PWN                                        |
| Dificultad  | Insane                                     |
| Técnica     | ROP chain con syscall directo (execve)     |
| Docker      | Sí                                         |
| Puertos     | 9999 (nc), 80 (web)                       |

## Descripción

El binario `minimalist` está compilado de forma **estática** — no hay libc dinámica.
No existe `system()`, no hay `gets()`, no hay PLT de libc.

Sin embargo, un binario estático contiene **miles de gadgets** de glibc compilada adentro.
El reto es construir un ROP chain que ejecute `execve("/bin/sh", NULL, NULL)` usando syscalls directas del kernel Linux.

## Vulnerabilidad

```c
char buf[64];
read(STDIN_FILENO, buf, 256);  // overflow: 256 bytes into 64
```

Offset a RIP: `64 (buffer) + 8 (saved rbp) = 72 bytes`.

## Técnica

### syscall execve (Linux x86-64)
```
rax = 59         ; SYS_execve
rdi = &"/bin/sh" ; path
rsi = 0          ; argv = NULL
rdx = 0          ; envp = NULL
syscall
```

### Pasos
1. Usar `ROPgadget --binary minimalist` para encontrar gadgets `pop rax; ret`, `pop rdi; ret`, `pop rsi; ret`, `pop rdx; ret`, `syscall`.
2. Escribir `/bin/sh` en la sección BSS (dirección fija — PIE=off).
3. Configurar registros con los gadgets y ejecutar `syscall`.

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
