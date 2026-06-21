# AntiDbg Corp — Anti-Debug Crackme

**Categoría:** Reversing  
**Dificultad:** Insane  
**ID:** insane-rev-antidbg

---

## Descripción

Un crackme C con protecciones anti-debugging activas. El binario verifica si el input del usuario es la clave correcta, pero primero pasa por dos capas de protección que detectan la presencia de debuggers.

La flag está codificada con XOR 0x1F en la sección `.data` del binario como el array `encoded_flag[]`.

---

## Protecciones

### Check 1: ptrace self-check
```c
static int is_debugged(void) {
    return ptrace(PTRACE_TRACEME, 0, 0, 0) == -1 ? 1 : 0;
}
```
Un proceso puede llamar `ptrace(PTRACE_TRACEME)` solo una vez. Si un debugger ya está adjunto, la llamada falla (retorna -1). El check detecta esto y termina con `"[!] Debugger detected."`.

### Check 2: timing check
```c
static int timing_check(void) { /* busy-loop de 1M iteraciones */ }
```
Mide cuánto tarda un busy-loop. En ejecución normal: < 5ms. Con breakpoints o single-step: puede superar 500ms. Si supera el umbral, termina con `"[!] Execution anomaly detected."`.

---

## Estrategias de solución

### Estrategia 1 (más fácil): Análisis estático
La flag XOR 0x1F está en `.data`. No requiere ejecutar el binario:
```bash
python3 solve.py
```

### Estrategia 2: LD_PRELOAD bypass
```bash
# Compilar librería que overridea ptrace()
gcc -shared -fPIC -o bypass_ptrace.so bypass_ptrace.c
LD_PRELOAD=./bypass_ptrace.so ./antidbg
```
Bypasea el check 1. El timing check aún debe sortearse (no usar single-step).

### Estrategia 3: NOP patching
Con un editor hex o pwntools, parchear los `je`/`jne` que siguen a los checks de anti-debug para que salten a la lógica principal incondicionalmente.

### Estrategia 4: Ghidra / radare2
Cargar el binario, identificar `check_flag()` y `encoded_flag[]`, extraer los bytes de la sección `.data` y XOR con 0x1F.

---

## Estructura

```
insane-rev-antidbg/
├── app/
│   ├── challenge.c     # Código C principal con anti-debug checks
│   ├── build.py        # Genera flag_data.c y compila el binario
│   ├── server.py       # Servidor Flask (tema terminal rojo/verde)
│   └── entrypoint.sh   # build.py → server.py
├── Dockerfile          # Ubuntu 22.04 + gcc + python3 + flask
├── docker-compose.yaml
├── challenge.yaml
├── README.md           # Este archivo
└── solve.py            # Script de solución estática (para autores)
```

---

## Deploy

```bash
export FLAG="CTF{4nt1_d3bug_1s_n0t_4_w4ll}"
docker-compose up --build
```

El servidor escucha en `http://localhost:8082`.

---

## Notas de autor

- `-no-pie` facilita el análisis estático al tener direcciones fijas
- `-fno-stack-protector` simplifica el análisis del stack en Ghidra
- El array `encoded_flag[]` en `.data` es accesible con `objdump -s -j .data antidbg`
- El solve.py usa búsqueda binaria de la secuencia XOR 0x1F de "CTF{" — solución de 10 segundos
- Nivel insane justificado: requiere entender ptrace, timing side-channels y análisis de binarios C
