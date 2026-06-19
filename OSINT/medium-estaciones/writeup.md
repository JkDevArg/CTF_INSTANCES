# Estaciones — Writeup

**Categoría:** OSINT
**Dificultad:** Medium


## Solución

### 1. Identificar el lugar

En la imagen se observa un letrero con el texto **"Embarque Norte 1"**, y también es visible una letra **"B"** en la estructura. Junto a esto, la imagen muestra elementos arquitectónicos característicos: cubierta metálica, barandas y baldosas podotáctiles amarillas, propios de un sistema de transporte.

El siguiente paso es buscar en Google Imágenes:
 
```
"embarque norte 1" "B" estación
```
 
Los resultados devuelven fotos de varias estaciones, buscando a fondo se encuentran fotos con señalización idéntica (mismo diseño de letrero, misma tipografía, misma "B" en fondo celeste), correspondientes al **Metropolitano de Lima**, sistema de transporte BRT de Lima, Perú.



### 2. Determinar la fecha y las estaciones candidatas

La descripción menciona que la fuga ocurrió "un día de diciembre, cuando la ciudad inauguró nuevas estaciones en el norte". Buscando palabras clave:

```
Metropolitano "estaciones" "norte" "diciembre"
```

Los resultados entre noticias y anuncios propios del Metropolitano, apuntan a la inauguración del **15 de diciembre de 2023** de la Ampliación Norte del Metropolitano, donde entraron en funcionamiento **cuatro nuevas estaciones**:

1. Estación Universidad
2. Estación 22 de Agosto
3. Estación Andrés Belaunde
4. Estación Los Incas

### 3. Triangular la estación correcta

Tomando en cuenta esta parte del reto: "fue a descansar a algún lugar reconocible desde lejos"
En la foto, ligeramente borrosa, se distingue una **letra "H" iluminada** en el lateral izquierdo del encuadre.

Ubicando cada una de las cuatro estaciones en Google Maps / Street View para después comparar la perspectiva con la de la foto y revisar si la infraestructura de la estación coincide, se determina que la única estación desde la cual se ve esa "H" en esa posición es **Estación Andrés Belaunde**.

La "H" corresponde al letrero de un hostal cercano: **Hotel Eros Spa**.

### 4. Encontrar el rastro

Siguiendo la pista de "fue a descansar a algún lugar reconocible desde lejos" y "nunca pasa por ningún sitio sin dejar rastro", se revisan las **reseñas de Google Maps del Hotel Eros Spa**.

Entre las reseñas aparece una que contiene la flag:

```
Tranqui, limpio, buena ubicación cerca del Metropolitano. Vine después de una noche movida y dormí como bebé. HL4{3r05_5p4_n0rt3}
```

## Flag

```
HL4{3r05_5p4_n0rt3}
```

La reseña con la flag la colocare horas antes de que empiece el ctf para que Google no me la borre :v