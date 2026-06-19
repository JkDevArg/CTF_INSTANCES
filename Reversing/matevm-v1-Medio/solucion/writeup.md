# Writeup — MateVM Reversing Challenge - by p0mb3r0

Este documento contiene la solución detallada paso a paso para resolver el reto `matevm`.

---

## 1. Identificación del binario

Lo primero que hace cualquier analista al enfrentarse a un reto es verificar el tipo de archivo utilizando la herramienta `file`:

```bash
$ file matevm
matevm: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=..., for GNU/Linux 3.2.0, stripped
```

Es un binario ejecutable ELF de 64 bits para Linux, y se encuentra **stripped** (sin símbolos de depuración ni nombres de funciones internas).

---

## 2. Análisis Estático Inicial con `strings`

Ejecutamos `strings` para ver si hay texto en claro de interés:

```bash
$ strings matevm
```

Entre la basura habitual de la biblioteca estándar de Rust y de inicialización de libc, vemos strings como:

```txt
=== MateVM License Checker ===
Ingrese licencia: 
Acceso concedido.
Licencia inválida.
H4L{FAKE_FLAG_DO_NOT_SUBMIT}
debug mode disabled
invalid checksum
vm panic
wrong serial
```

Vemos varias flags falsas (decoy) como `H4L{FAKE_FLAG_DO_NOT_SUBMIT}`, pero no hay rastros de la flag real `H4L{RUST_VM_BYT3C0D3}`. Esto confirma que el binario no valida la flag mediante una simple comparación de strings directa.

---

## 3. Análisis en Ghidra / IDA Pro

Al abrir el binario en un descompilador, nos dirigimos al punto de entrada (`main` o el punto de inicio de Rust a través de `entry` -> `std::rt::lang_start`).

### Reconocimiento de la VM
A pesar de estar stripped, la estructura de la función principal de validación es característica de una máquina virtual (VM interpreter):
1. **Inicialización del estado**: Hay variables locales que actúan como registros:
   - Un contador de programa (`pc`, inicialmente `0`).
   - Un acumulador (`acc`, inicialmente `0`).
   - Un flag booleano de validez (`ok`, inicialmente `1` o `true`).
2. **Bucle de interpretación**: Un bucle `while` (o `loop` compilado) que lee bytes de un array embebido de 3 en 3 (alineación a 3 bytes).
3. **Decodificación (`match opcode`)**: Una estructura switch/case gigante (o bloques `if/else` encadenados) basada en el primer byte de la instrucción (el opcode).
4. **Mutación de registros**: Cada rama modifica el acumulador o realiza operaciones aritméticas y saltos lógicos.

---

## 4. Identificación del Bytecode Cifrado

Buscando en la sección `.rodata` o a través de las referencias del bucle interpretador, localizamos un buffer estático de 381 bytes. Al examinar el código decompilado de la función que lo carga, observamos un bucle XOR simple en runtime contra la clave estática `"matevm"`.

El código en Rust que realiza esta carga es:
```rust
let key = b"matevm";
let decrypted = ENCRYPTED_PROGRAM
    .iter()
    .enumerate()
    .map(|(i, &b)| b ^ key[i % key.len()])
    .collect::<Vec<u8>>();
```

Extrayendo ese buffer y descifrándolo con el XOR correspondiente, obtenemos el bytecode en claro.

---

## 5. Análisis de Opcodes

A partir del decompilador, mapeamos el switch/case a los siguientes comportamientos:

- `0x01` (`LOAD_INPUT`): Lee el byte del input del usuario en el índice dado por el argumento 1 (`input[arg1]`) y lo carga en el acumulador.
- `0x02` (`XOR`): Hace un XOR del acumulador con el argumento 1.
- `0x03` (`ADD`): Suma al acumulador el argumento 1 (con wrapping de 8 bits).
- `0x04` (`SUB`): Resta al acumulador el argumento 1 (con wrapping de 8 bits).
- `0x05` (`ROL`): Rota los bits del acumulador a la izquierda.
- `0x06` (`ROR`): Rota los bits del acumulador a la derecha.
- `0x07` (`CMP`): Compara el acumulador con el argumento 1. Si no coinciden, marca el estado `ok = false`.
- `0x08` (`JNZ_FAIL`): Termina de inmediato la ejecución con fallo si `ok` es `false`.
- `0x09` (`HALT_OK`): Termina con éxito si `ok` sigue siendo `true`.
- `0x0A` (`HALT_FAIL`): Termina la VM con fallo inmediato.

---

## 6. Reconstrucción de la Flag (Solución Automática)

Cada carácter del input se procesa de forma individual y desordenada mediante un bloque de bytecode estructurado como este:
1. `LOAD_INPUT index`
2. Tres operaciones secuenciales (mezcla de `XOR`, `ADD`, `SUB`, `ROL`, `ROR`).
3. `CMP expected_value`
4. `JNZ_FAIL`

Para recuperar la flag, podemos escribir un script en Python que realice el camino inverso para cada carácter:
1. Extraer los bloques del bytecode para cada `index`.
2. Comenzar desde el valor esperado (`expected_value` del `CMP`).
3. Aplicar las operaciones inversas en orden opuesto:
   - La inversa de `ROL` es `ROR`.
   - La inversa de `ROR` es `ROL`.
   - La inversa de `XOR` es `XOR`.
   - La inversa de `ADD` es `SUB` (módulo 256).
   - La inversa de `SUB` es `ADD` (módulo 256).
4. El valor resultante es el carácter original en esa posición.

Ejecutamos el solver:

```bash
$ python3 solve.py
H4L{RUST_VM_BYT3C0D3}
```

¡Flag recuperada con éxito!
