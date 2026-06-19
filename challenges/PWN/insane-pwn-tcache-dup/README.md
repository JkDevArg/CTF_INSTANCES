# AllocatorCorp — Tcache Double-Free

| Campo       | Valor                                              |
|-------------|----------------------------------------------------|
| Categoría   | PWN                                                |
| Dificultad  | Insane                                             |
| Técnica     | Heap — Tcache double-free + key leak + GOT/ptr write |
| Docker      | Sí                                                 |
| Puertos     | 9999 (nc), 80 (web)                               |

## Descripción

El binario `allocator` implementa un sistema de notas con operaciones de alloc/free/read/write.

**Bug**: Al liberar un chunk, el puntero **no se borra** del array `chunks[]`. Esto permite:
1. Liberar el mismo chunk dos veces (double-free).
2. Leer el chunk liberado para obtener el `fd` del tcache (que contiene la clave de protección de glibc 2.35).
3. Envenenar el next pointer del tcache para hacer que `malloc()` devuelva una dirección arbitraria.
4. Sobrescribir el global `action` con la dirección de `flag_handler()`.

## Análisis de la vulnerabilidad

```c
free(chunks[s]);
// BUG: chunks[s] no es NULL → double-free posible
```

## Técnica: Tcache Poisoning (glibc 2.35)

En glibc 2.35, el fd de un chunk liberado en tcache es `XOR(next_ptr, tcache_key)`.
Para envenenar el tcache, necesitamos la clave. Esta se puede obtener leyendo el chunk liberado.

```
1. alloc(0), alloc(1)
2. free(0)           → tcache: [chunk0]
3. show(0)           → leaked tcache key del fd
4. free(0)           → double-free: tcache: [chunk0 → chunk0]
5. write(0, XOR(target, key))  → corrompe next ptr
6. alloc(2)          → obtiene chunk0
7. alloc(3)          → obtiene chunk en target (&action)
8. write(3, flag_handler_addr) → sobrescribe action
9. call_action()     → ejecuta flag_handler()
```

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
