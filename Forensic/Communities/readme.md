Nombre: Communities
Nivel: easy
Flag: HL4{Th@nk$_t0_@ll_f0r_$upp0rt1nG}

Descripción:
He visto a muchas comunidades apoyando este HackerL4bs en su CTF, así que me animé a sacar mis crayolas y dibujar algo conmemorativo. Pero al exportar el proyecto, algo raro sucedió.

Espero puedas ayudarme a volverlo a abrir.

## Archivos entregados

- `communities.zip`

## Solucion

El reto nos entrega un archivo llamado `communities.zip`. Lo primero fue inspeccionarlo para entender si realmente era un ZIP normal.

Al revisar el contenido del archivo se puede notar que no se trata de un ZIP comun, sino de un proyecto de Krita. Estos archivos usan la extension `.kra`, pero internamente tambien funcionan como archivos comprimidos.

Por eso, simplemente cambiamos la extension:

```
mv communities.zip communities.kra
```

Luego abrimos `communities.kra` con Krita. Al revisar el panel de capas, algunas estaban ocultas. Solo fue necesario activar la visibilidad de esas capas para revelar el contenido escondido.

Al hacer visibles las capas ocultas aparece la flag:

```
HL4{Th@nk$_t0_@ll_f0r_$upp0rt1nG}
```
