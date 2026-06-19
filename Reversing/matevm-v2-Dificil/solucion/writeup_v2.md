# Writeup — matevm2 (Hard) - by p0mb3r0

Reto de reversing. Un binario Rust valida una licencia con formato `H4L{...}`.
El validador es una VM custom que ejecuta bytecode propio. Esta vez la
historia es distinta a V1: cada byte de la flag NO se resuelve aislado.

Flag: `H4L{STATEFUL_VM_BYTECODE_2026}`

---

## 1. Triage del binario

```bash
$ file matevm2
ELF 64-bit LSB pie executable, x86-64, ..., stripped
$ ./matevm2
=== MateVM2 License Checker ===
Ingrese licencia: foo
Licencia invalida.
```

Lo primero que cualquier reverser intenta:

```bash
$ strings matevm2 | grep -E 'H4L|MateVM|licencia|Acceso'
(vacío)
```

Vacío. Las strings de banner, prompt y mensajes no están en `.rodata`. Tampoco
encontramos la flag literal, ni siquiera fragmentos. Esto descarta los enfoques
fáciles (`grep`, `strings -n 8`, búsqueda por `H4L{`).

> **Pista 1**: Las strings están encriptadas. Hay rutinas de decoding que las
> rehidratan en runtime. Buscar funciones que devuelvan `String`/`Vec<u8>` cerca
> de los `println!`.

---

## 2. Localizar el dispatcher

Carguemos en Ghidra. Ir a `main`. Encontramos:

- Lectura de stdin con `read_line`.
- Llamada a `check_license` (nombre inventado — está stripped).
- `check_license` arma una struct opaca y entra en un loop con un `match` sobre un byte.

El loop tiene la pinta clásica de un intérprete de VM:

```c
while (pc < program_len) {
    byte op = fetch(pc) ^ keystream(pc, seed);
    pc += 1;
    switch (op) {
        case 0x01: pc = program_len; break;        // HALT_OK
        case 0x02: ok = false; pc = program_len; break;
        case 0x05: ok &= input_len == imm8; pc += 1; break;
        case 0x06: ok &= input[pos] == val; pc += 2; break;
        ...
    }
}
return ok;
```

A simple vista hay ~30 ramas distintas. Estamos ante una VM completa.

> **Pista 2**: cada rama tiene un tamaño de operandos distinto (incrementos de
> `pc` variables). La ISA tiene **instrucciones de longitud variable**.

---

## 3. Decoder por XOR keystream

La función `fetch(pc)` no es una simple lectura. Tiene esta pinta:

```c
byte fetch(usize pc) {
    pc = volatile_or_blackbox(pc);           // hint de obfuscación
    int k = pc & 0x3;
    uint32_t j = pc >> 2;
    int s = PERM[k];
    (coeff, off) = COEFFS[s];
    int pos = (j * coeff + off) % SHARD_LEN;
    switch (s) {
        case 0: return SHARD_0[pos];
        case 1: return SHARD_1[pos];
        case 2: return SHARD_2[pos];
        default: return SHARD_3[pos];
    }
}
```

Entonces el bytecode NO vive como un único buffer contiguo. Está distribuido
en **4 shards** + tablas `PERM` y `COEFFS`. El offset dentro de cada shard se
calcula con `(j * coeff + off) % SHARD_LEN` — un módulo lineal con coeficientes
coprimos a `SHARD_LEN` (por eso es una permutación bijectiva).

> **Pista 3**: si te tomás el trabajo de detectar el modulo y los coeficientes
> en cada `case` del switch, podés escribir un `materialize(pc)` propio en
> Python. Lo único que falta es la tabla `PERM` (4 enteros) y los pares `COEFFS`
> (4 pares de u32).

El XOR con `keystream(pc, seed)` está justo después del fetch:

```c
op = fetch(pc) ^ keystream(pc, seed);
```

La función `keystream` es un finalizer estándar tipo FxHash:

```c
uint8_t keystream(uint64_t pc, uint32_t seed) {
    uint32_t x = pc + seed;
    x *= 0x9E3779B1;
    x ^= x >> 13;
    x *= 0x85EBCA77;
    x ^= x >> 16;
    return x & 0xFF;
}
```

Reconocible por las constantes `0x9E3779B1` y `0x85EBCA77`.

> **Pista 4**: Hay dos seeds distintos en el binario: uno para el bytecode y
> uno para las strings. Buscarlos como constantes inmediatas de 32 bits
> referenciadas en la zona del dispatcher y en la zona de decoding de strings.

---

## 4. Hay decoys

En las shards aparece data plausible pero NUNCA referenciada por
`materialize`. Son shards de decoy (`DECOY_A`, `DECOY_B`). Si te ponés a
desensamblar shards sin chequear `PERM`, vas a perder tiempo.

Lo mismo con las strings: hay 7 decoy strings (`H4L{FAKE_FLAG_...}`,
`debug mode disabled`, `vm checksum mismatch`, etc.) que existen en `.rodata`
pero nunca se decodifican. Están marcadas `#[used]` para que el linker no las
elimine.

> **Pista 5**: Sólo confiar en lo que referencia el código. Si un shard nunca
> aparece como destino del `switch` de `materialize`, ignorarlo.

---

## 5. Reconstruir el stream de instrucciones

Una vez que tenés `materialize(pc)` y `keystream(pc, seed)`, podés extraer el
bytecode completo iterando `pc` de `0` a `PROGRAM_LEN`:

```python
program = bytes(
    materialize(pc) ^ keystream(pc, SEED)
    for pc in range(PROGRAM_LEN)
)
```

Ahora tenés ~1.5 KB de bytecode en claro. Es hora de desensamblar.

### ISA

Con paciencia (o con un disassembler propio) identificás:

| Op | Mnem | Operandos | Tamaño |
|----|------|-----------|--------|
| 0x01 | HALT_OK | — | 1 |
| 0x02 | HALT_FAIL | — | 1 |
| 0x04 | ASRT | — | 1 |
| 0x05 | CHKLEN | imm8 | 2 |
| 0x06 | CHKBYTE | pos, val | 3 |
| 0x07 | CHKCSET | pos | 2 |
| 0x08 | LDB | rd, pos | 3 |
| 0x0A | LDI32 | rd, imm32 | 6 |
| 0x0B | STATEB | rd, lane | 3 |
| 0x0C | MOV | rd, rs | 3 |
| 0x0D | XORR | rd, rs | 3 |
| 0x0E | XORI | rd, imm8 | 3 |
| 0x0F-0x16 | ADD/SUB/MUL/ROL/ROR/AND | rd, rs/imm8 | 2-3 |
| 0x18 | CMPI | rd, imm8 | 3 |
| 0x19 | FOLD | rs | 2 |
| 0x1A | FINST | imm8 | 2 |
| 0x1B | CRCFEED | rs | 2 |
| 0x1C | CRCINIT | imm32 | 5 |
| 0x1D | CRCCHK | imm32 | 5 |
| 0x21 | INITST | imm32 | 5 |

Recursos:
- 8 registros u32 (`r0..r7`), ops byte-level operan sobre los low 8 bits
- `state`: u32 rolling
- `crc`: u32 checksum
- `ok`: flag boolean

---

## 6. El modelo de validación

Desensamblando el bytecode encontramos esta estructura:

```
INITST 0xC0DEC0DE
CHKLEN 30
CHKBYTE 0, 'H'
CHKBYTE 1, '4'
CHKBYTE 2, 'L'
CHKBYTE 3, '{'
CHKBYTE 29, '}'
CHKCSET 4
CHKCSET 5
...
CHKCSET 28
ASRT
; --- constraints ---
LDB r0, 17
LDB r1, 9
LDB r2, 25
MOV r4, r0
ROLI r4, 3
MOV r5, r1
ROLI r5, 5
XORR r4, r5
XORR r4, r2
STATEB r5, 2
XORR r4, r5
TRNC8 r4
CMPI r4, 0xAB
ASRT
FOLD r0
FOLD r1
FOLD r2
FINST 0xAB
; ... otra constraint ...
; --- checksum ---
CRCINIT 0xCAFEBABE
LDB r0, 4
CRCFEED r0
...
LDB r0, 28
CRCFEED r0
CRCCHK 0xC6BC90AF
ASRT
HALT_OK
```

Patrón claro: por cada **constraint**, hay un bloque con:

1. `LDB` de 2-3 posiciones del body.
2. Una mezcla de ops (`XORR`, `ROLI`, `MULI`, `STATEB`, `ADDR`, etc.).
3. `CMPI` contra un valor objetivo → marca `ok = false` si no coincide.
4. `ASRT` aborta si `ok` ya cayó.
5. `FOLD` por cada arg + `FINST target` que actualiza el `state`.

### Operaciones identificables

Cada bloque calcula una de:

```
xor2(a, b)     = a ^ b ^ state_byte0
win2(a, b)     = a*37 + b*211 + state_byte0          (mod 256)
sum3(a, b, c)  = (a + b + c) ^ state_byte1           (mod 256)
mix3(a, b, c)  = rotl8(a,3) ^ rotl8(b,5) ^ c ^ state_byte2
tri(a, b, c)   = a ^ rotl8(b,4) ^ ((c*5+11) & 0xFF) ^ state_byte3
```

### Rolling state

Después de cada CMP exitoso, el state se actualiza:

```
para cada arg byte v:
    state = rotl32(state ^ v, 7)
    state = state + (v << 16)
state = rotl32(state, 13) ^ (target << 8) ^ 0x9E3779B9
```

### Checksum

Al final:

```
crc = 0xCAFEBABE
para cada body[i]:
    crc = rotl32(crc, 5) ^ body[i]
    crc = crc + 0x9E3779B9
    crc = rotl32(crc, 11) ^ (body[i] << 17)
assert crc == TARGET_CHECKSUM
```

---

## 7. Por qué V1 no sirve acá

En V1 cada bloque era:

```
LOAD body[i]
op imm
op imm
op imm
CMP target
```

Sólo dependía de `body[i]`. Invertible.

En V2:

- Cada constraint toca **2 o 3 posiciones distintas** del body.
- Cada body[i] aparece en **2+ constraints diferentes**.
- El **rolling state** mezcla los bytes anteriores en cada operación futura.
- El **checksum final** cubre todos los bytes.

Si quisieras enumerar `body[5]` solo, no sabés qué target esperar en
constraint N porque depende del state, que depende de constraints
anteriores que tocan otros bytes que aún no comprometiste.

> **Pista 6**: este es un problema CSP. Hay que resolverlo como sistema, no
> byte por byte.

---

## 8. Solver con Z3

Una vez que extrajiste:

- La lista de constraints `(op, idxs, target)`,
- El `initial_state` (0xC0DEC0DE),
- El `checksum_target` (0xC6BC90AF en este build),

podés codificar todo en Z3 con BitVec(8) y BitVec(32). Ver `solve_v2.py`.

```python
from z3 import BitVec, BitVecVal, Solver, Or, sat, ...

body = [BitVec(f"b{i}", 8) for i in range(25)]

s = Solver()
for v in body:
    s.add(Or(*[v == c for c in CHARSET_BYTES]))

state = BitVecVal(0xC0DEC0DE, 32)
for c in constraints:
    args = [body[i] for i in c['idxs']]
    val = eval_sym(c['op'], args, state)
    s.add(val == c['target'])
    state = update_sym(state, args, c['target'])

# checksum
crc = BitVecVal(0xCAFEBABE, 32)
for v in body:
    crc = rotl32(crc, 5) ^ ZeroExt(24, v)
    crc = crc + 0x9E3779B9
    crc = rotl32(crc, 11) ^ (ZeroExt(24, v) << 17)
s.add(crc == CHECKSUM_TARGET)

assert s.check() == sat
m = s.model()
flag = "H4L{" + "".join(chr(m[v].as_long()) for v in body) + "}"
print(flag)
```

Tiempo de cómputo: ~1 segundo.

```
$ python3 solve_v2.py
flag: H4L{STATEFUL_VM_BYTECODE_2026}
solved in 0.88s
```

---

## 9. Backtracking sin SMT

Si no querés usar Z3, podés hacer backtracking ingenuo siguiendo el orden de
las constraints. Funciona en teoría (cada constraint sólo añade restricciones
locales), pero la rama inicial tiene 3 vars libres en un charset de 37
elementos → `37²·N` caminos antes de podar.

Tiempos medidos con la versión naive de `solve_constraints.py`: no converge
en 45 segundos. Implementando AC-3 + forward checking y enumerando primero
las variables con mayor restricción podés bajarlo a minutos.

> **Pista 7**: ahorrate el dolor, usá Z3.

---

## 10. Resumen del flujo de resolución

```
binario stripped
   │
   │ 1. triage: file, strings (vacío), entropy
   ▼
identificar dispatcher (loop con switch grande)
   │
   │ 2. detectar XOR keystream y materialize(pc)
   ▼
extraer bytecode (~1.5 KB) por emulación o re-impl
   │
   │ 3. mapear ISA (33 opcodes, longitud variable 1..6)
   ▼
desensamblar bytecode → assembly legible
   │
   │ 4. identificar patrones LDB → op → CMPI → ASRT → FOLD → FINST
   ▼
extraer (op, idxs, target) por cada constraint
   │
   │ 5. identificar update del rolling state
   │ 6. identificar el checksum final
   ▼
codificar como CSP en Z3 con BitVec(8/32)
   │
   ▼
flag recuperada en ~1 segundo
```

---

## 11. Tiempo estimado

| Perfil | Tiempo |
|--------|--------|
| Reverser profesional (Ghidra + Z3 fluido) | 4–8 h |
| Reverser intermedio | 1–2 días |
| Sin Z3, sólo backtracking serio | varias horas adicionales |

El reto es honesto: todo está en el binario, no hay red, no hay anti-debug, el
charset es chico, la solución es única.

Lo que cambia respecto a V1 es que el atajo "una ecuación por carácter"
ya no funciona. Hay que entender la VM, el rolling state, y resolverlo
como sistema.

---

## 12. Mitigaciones implementadas

Por si te quedaste con la duda de por qué algunas cosas son tan tediosas:

| Mitigación | Defensa |
|------------|---------|
| Bytecode XOR-encoded con keystream(pc, seed) | Un solo breakpoint no dumpea bytecode legible |
| Shards 4× con permutación + módulo lineal | No hay un buffer contiguo en `.rodata` |
| 2 shards decoy con `#[used]` | Confunden al reverser que dumpea todas las arrays grandes |
| `read_volatile` en seeds críticas | LTO no puede const-fold la decodificación y filtrar cleartext en `.rodata` |
| Strings encriptadas con keystream distinto | `strings(1)` no da landmarks |
| 7 strings decoy también encriptadas | Más ruido |
| `black_box(pc)` dentro de materialize | LTO no puede enumerar pc y reconstituir el buffer encoded |
| Charset reducido a `A-Z 0-9 _` | Permite backtracking razonable y a la vez deja entropía justa |

---

## 13. Cierre

V1 enseñaba "qué es una VM". V2 enseña "por qué constraints cruzadas vencen
inversión algebraica".
