# GoCorp — GoCrackMe v1.0

**Categoría:** Reversing  
**Dificultad:** Hard  
**ID:** hard-rev-golang

---

## Descripción

GoCorp desplegó su validador de acceso compilado en Go. El binario recibe un input por stdin y verifica si coincide con el secreto interno. Sin source code, sin símbolos de debug.

Go compila estáticamente — el binario resultante incluye el runtime completo, lo que lo hace grande y aparentemente opaco. Sin embargo, las cadenas y la lógica de comparación siempre dejan rastro en las secciones de datos.

---

## Concepto técnico

El binario contiene la flag codificada con XOR 0x42. Al iniciarse, la decodifica en memoria y compara con el input del usuario.

Capas de análisis:
1. `strings gocrackme` — recupera cadenas visibles, pero la flag está XOR-encoded
2. Análisis de bytecode Go con **GoReSym** — recupera nombres de funciones
3. Búsqueda del array XOR en las secciones de datos con Ghidra o radare2
4. XOR manual del array `encoded[]` con 0x42

---

## Estructura

```
hard-rev-golang/
├── app/
│   ├── build.py        # Genera main.go desde FLAG env, compila con go build
│   ├── server.py       # Servidor Flask (tema terminal verde)
│   └── entrypoint.sh   # build.py → server.py
├── Dockerfile          # Ubuntu 22.04 + golang-go + python3 + flask
├── docker-compose.yaml
├── challenge.yaml
├── README.md           # Este archivo
└── solve.py            # Script de solución (para autores)
```

---

## Deploy

```bash
export FLAG="CTF{g0_r3v3rs1ng_1s_n0t_s0_s1l3nt}"
docker-compose up --build
```

El servidor escucha en `http://localhost:8080`.

---

## Solución resumida

```bash
# Método 1: strings directo (la flag está XOR-encoded, no aparecerá literal)
strings gocrackme | grep -i ctf

# Método 2: extraer el array encoded[] y XOR con 0x42
python3 solve.py

# Método 3: Ghidra + GoReSym plugin
# Cargar gocrackme, aplicar GoReSym, buscar main.deobfuscate
# Extraer los bytes del literal []byte{...} y XOR con 0x42
```

---

## Notas de autor

- El flag se embebe en el source Go como array de bytes XOR 0x42 en tiempo de build
- `-ldflags=-s -w` elimina la tabla de símbolos y la info DWARF
- Los jugadores con Ghidra pueden recuperar la función `deobfuscate` y sus argumentos
- GoReSym (plugin Ghidra de Mandiant) es la herramienta canónica para binarios Go
