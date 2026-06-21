# ObfCorp — Python Layers

**Categoría:** Reversing  
**Dificultad:** Insane  
**ID:** insane-rev-obfuscated

---

## Descripción

Un script Python verifica si el input del usuario es la flag correcta. El problema: el código fuente ha sido procesado a través de tres capas de ofuscación anidadas usando `base64`, `zlib`, `marshal` y `exec`.

Los jugadores deben desenvolver cada capa manualmente para llegar al núcleo que contiene la lógica real de comparación.

---

## Arquitectura de capas

```
checker.py  (descargable)
│
└── Capa 0: exec(compile(marshal.loads(zlib.decompress(base64.b64decode(_)))))
    │
    └── Capa 1: exec(compile(marshal.loads(zlib.decompress(base64.b64decode(_d)))))
        │
        └── Capa 2: exec(compile(marshal.loads(zlib.decompress(base64.b64decode(_d)))))
            │
            └── Capa 3 (núcleo):
                  _s = FLAG[::-1]     # flag invertida como literal
                  if input()[::-1] == _s: print("[+] Correcto!")
```

La flag real está guardada **invertida** como string literal en el bytecode de la capa 3.

---

## Estructura

```
insane-rev-obfuscated/
├── app/
│   ├── build.py        # Genera checker.py con 3 capas de ofuscación
│   ├── server.py       # Servidor Flask (tema terminal violeta/verde)
│   └── entrypoint.sh   # build.py → server.py
├── Dockerfile          # python:3.11-slim + flask
├── docker-compose.yaml
├── challenge.yaml
├── README.md           # Este archivo
└── solve.py            # Script de solución (para autores)
```

---

## Deploy

```bash
export FLAG="CTF{py7h0n_0bfusc4t10n_15_p33l4bl3}"
docker-compose up --build
```

El servidor escucha en `http://localhost:8081`.

---

## Solución resumida

```python
# Método 1: interceptar exec() en runtime
import builtins
original_exec = builtins.exec
def fake_exec(code, *args, **kwargs):
    print("exec interceptado:", getattr(code, 'co_filename', '?'))
    import dis; dis.dis(code)
    return original_exec(code, *args, **kwargs)
builtins.exec = fake_exec
exec(open('checker.py').read())

# Método 2: script automatizado
python3 solve.py
```

El solve.py desempaqueta las 3 capas automáticamente y extrae el string invertido de los co_consts del bytecode de la capa 3.

---

## Notas de autor

- La flag se almacena invertida (`FLAG[::-1]`) en el literal del código fuente de la capa 3
- El checker compara `input()[::-1] == _s`, por lo que ingresar la flag normal funciona
- Los jugadores deben usar `dis.dis()` sobre el code object de la capa 3 para encontrar el `LOAD_CONST` del string invertido
- Nivel insane justificado: hay que entender `marshal`, `code objects`, `co_consts`, y el patrón de inversión
