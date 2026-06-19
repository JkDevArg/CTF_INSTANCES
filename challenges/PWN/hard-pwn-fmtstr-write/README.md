# LogSys Corp — Format String Write

| Campo       | Valor                                   |
|-------------|-----------------------------------------|
| Categoría   | PWN                                     |
| Dificultad  | Hard                                    |
| Técnica     | Format String → arbitrary write → GOT overwrite |
| Docker      | Sí                                      |
| Puertos     | 9999 (nc), 80 (web)                    |

## Descripción

El binario `logger` pasa directamente el input del usuario a `printf()` sin formato.
No es un overflow de stack — es una vulnerabilidad de format string que permite escritura arbitraria en memoria.

Existe una función `win()` en el binario. La GOT entry de `exit()` es escribible (RELRO=partial).
Sobrescribe `exit@GOT` con la dirección de `win()` usando `%n` de format string.

## Vulnerabilidad

```c
printf(log);   // FORMAT STRING — sin segundo argumento
exit(0);       // Llama a exit() → si GOT fue sobrescrito, llama a win()
```

## Técnica

1. Determinar el offset del stack donde está el buffer del format string (típicamente 6-8).
2. Usar `fmtstr_payload(offset, {exit_got: win_addr})` de pwntools.
3. Enviar el payload — printf escribe a `exit@GOT`.
4. Cuando `exit(0)` es llamado, ejecuta `win()` en su lugar.

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
