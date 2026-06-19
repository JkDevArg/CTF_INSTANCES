# MateVM — Reversing Challenge

Un desarrollador escribió su propio sistema de licencias en Rust.
Dice que nadie puede romperlo porque no hay ninguna comparación directa de la flag.

¿Podés recuperar la licencia válida?

**Formato de flag:** `H4L{...}`

## Instrucciones de ejecución

1. Compilá el binario usando la receta del Makefile:
   ```bash
   make dist
   ```
2. Ejecutá el validador:
   ```bash
   ./dist/matevm
   ```

El binario esperará que ingreses la licencia correcta por la entrada estándar (`stdin`).
Si la licencia ingresada es la correcta, imprimirá `Acceso concedido.`, de lo contrario imprimirá `Licencia inválida.`.
