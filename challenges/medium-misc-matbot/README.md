# medium-misc-matbot

**Categoria:** Misc  
**Dificultad:** Media  
**Puertos:** 9999 (quiz interactivo) | 80 (info web)

---

## Descripcion

Un servidor envia 50 operaciones aritméticas aleatorias (suma, resta,
multiplicación con operandos entre 1 y 999) y el jugador tiene 30 segundos para
responderlas todas correctamente.

La velocidad requerida hace imposible resolverlo manualmente. El jugador debe
escribir un script que se conecte, parsee cada problema, calcule la respuesta
y la envie automaticamente.

---

## Formato del protocolo

```
==================================================
  MathBot Corp — Verificacion Automatizada
==================================================
Resuelve 50 operaciones en 30 segundos.
Si eres mas rapido que un humano, la flag es tuya.

[01/50] 342 + 187 = <respuesta_del_jugador>
[02/50] 901 - 456 = <respuesta_del_jugador>
...
[50/50] 213 * 77  = <respuesta_del_jugador>

==================================================
[+] 50/50 — Perfecto! Eres una maquina.
[+] FLAG: CTF{...}
```

Si alguna respuesta es incorrecta, el bot muestra el valor correcto pero
continua. Si el puntaje final no es 50/50, no entrega la flag.

---

## Solucion

### Opcion 1: script con pwntools (recomendado)

```bash
pip install pwntools
python3 solve.py HOST=<ip> PORT=9999
```

### Opcion 2: script manual con socket

```python
import socket, re

s = socket.socket()
s.connect(('<host>', 9999))
data = b''

def recvuntil(sock, needle):
    global data
    while needle not in data:
        data += sock.recv(4096)
    idx = data.index(needle) + len(needle)
    chunk, data = data[:idx], data[idx:]
    return chunk

# Consumir encabezado
recvuntil(s, b'la flag es tuya.\n\n')

for _ in range(50):
    chunk = recvuntil(s, b'= ').decode()
    m = re.search(r'(\d+)\s*([+\-*])\s*(\d+)', chunk)
    a, op, b = int(m.group(1)), m.group(2), int(m.group(3))
    result = eval(f"{a}{op}{b}")
    s.sendall(f"{result}\n".encode())

print(s.recv(512).decode())
s.close()
```

---

## Logica clave del solve

1. Conectar por TCP al puerto 9999
2. Consumir el encabezado hasta la linea en blanco
3. Loop de 50 iteraciones:
   - Recibir hasta `= ` (el prompt de cada pregunta)
   - Parsear los dos operandos y el operador con regex
   - Calcular el resultado y enviarlo seguido de `\n`
4. Leer la respuesta final con la flag

---

## Despliegue

```bash
docker-compose up --build
```

La FLAG es inyectada via variable de entorno. `socat` despacha una instancia
separada de `bot.py` por cada conexion TCP al puerto 9999.

---

## Conceptos cubiertos

- Automatizacion de protocolos TCP con scripts Python
- Parseo de texto con expresiones regulares
- Uso basico de `pwntools` para CTF scripting
- Manejo de timeouts en comunicacion de red
