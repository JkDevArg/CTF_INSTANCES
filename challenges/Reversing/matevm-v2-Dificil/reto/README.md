# matevm2 — Reversing Challenge - by p0mb3r0

Un desarrollador escribió su propio sistema de licencias en Rust.
Dice que aprendió del fiasco anterior (matevm v1) y que esta vez
no hay forma de invertirlo byte por byte.

¿Podés recuperar la licencia válida?

**Formato de flag:** `H4L{...}`

## Ejecución

```bash
./matevm2
```

El binario espera la licencia por `stdin`. Si es correcta imprime
`Acceso concedido.`, si no `Licencia invalida.`.

## Notas

- Es un ELF 64-bit Linux x86-64, dinámicamente linkeado contra `libc`.
- Está stripped. No hay símbolos.
- No usa red, no toca el disco, no escribe archivos.
- El charset interno del cuerpo de la flag está restringido — explorá
  el binario para descubrir cuál.
- El reto se puede resolver con herramientas estándar: Ghidra/IDA + un
  poco de Python (Z3 ayuda bastante al final).

¡Suerte!
