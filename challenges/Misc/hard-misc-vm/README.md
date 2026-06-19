# hard-misc-vm

**Categoria:** Misc  
**Dificultad:** Hard  
**Puerto:** 80 (descarga de archivos)

## Descripcion

Reto de reversing de maquina virtual. Se provee:
- `vm.py` — interprete de MateVM v1.0 (codigo fuente completo, dado al jugador)
- `program.bin` — programa compilado en bytecode de MateVM
- `isa.md` — documentacion del ISA

Al ejecutar `python3 vm.py program.bin`, la salida es caracteres ininteligibles (garbled). El jugador debe analizar el interprete para entender por que y recuperar la flag.

## Mecanismo

La VM tiene una instruccion `PRINT` que aplica XOR con un LFSR antes de imprimir:

```python
def lfsr_next(state):
    return ((state << 1) | (state >> 7)) & 0xFF  # rotate-left 8-bit

# En PRINT:
lfsr = lfsr_next(lfsr)
out.append(chr(regs[rd] ^ lfsr))  # valor real XOR lfsr = basura
```

El bytecode almacena los bytes reales de la flag en instrucciones `LOAD`. El `PRINT` solo corrompe la salida; el valor en el registro sigue siendo correcto.

## Solucion

### Metodo 1: Analisis estatico (sin ejecutar)
Parsear el bytecode y extraer los inmediatos de las instrucciones `LOAD` que van seguidas de `PRINT`.

### Metodo 2: Ejecutar y revertir
1. Ejecutar la VM para obtener la salida garbled
2. Simular el LFSR con seed `0x42`
3. XOR cada byte garbled con el LFSR correspondiente

```python
lfsr = 0x42
recovered = []
for b in garbled:
    lfsr = lfsr_next(lfsr)
    recovered.append(b ^ lfsr)
flag = bytes(recovered).decode()
```

## Setup local

```bash
docker-compose up --build
# Descargar desde http://localhost/download/vm.py
# Descargar desde http://localhost/download/program.bin
python3 solve.py
```

## Archivos

- `app/build.py` — compila la flag en bytecode MateVM y genera vm.py + isa.md
- `app/server.py` — pagina informativa con enlaces de descarga
- `solve.py` — dos metodos de solucion con explicacion detallada
