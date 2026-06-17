Nombre: OverDS
Nivel: easy
Flag: HL4{overpwnz_DS}

Descripción:
Estaba en clase de la universidad y, entre apuntes y distracciones, me puse a jugar un rato con algo antiguo que encontré. Era solo una imagen, o al menos eso parecía.

## Archivos entregados

- `bajando_pepa.jpg`

## Solucion

El reto nos entrega una imagen llamada `bajando_pepa.jpg`. Aunque a simple vista parece ser solo una imagen, lo primero fue inspeccionarla para buscar datos ocultos o archivos embebidos.

Al analizar el archivo se puede encontrar un archivo `.nds` dentro de la imagen. Esta extension corresponde a una ROM de Nintendo DS.

Una vez extraida la ROM, solo necesitamos abrirla con un emulador de Nintendo DS. En este caso use `melonDS`.

Al cargar el archivo `.nds` en el emulador, el programa muestra directamente la flag en pantalla:

```
HL4{overpwnz_DS}
```
