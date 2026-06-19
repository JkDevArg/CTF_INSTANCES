# Scary — Writeup
 
**Categoría:** Misc/Stego 
**Dificultad:** Easy
**Herramientas:** `ffmpeg`, `zsteg`
 

## Solución
 
### 1. Extraer los frames
 
El primer paso es reconocer que el archivo es un GIF animado y extraer cada frame individualmente. 
 
```bash
mkdir frames
ffmpeg -i scary.gif frames/frame_%02d.png
```
 
### 2. Encontrar el frame más pesado
 
El enunciado nos dice que hay una silueta que *pesa más*, hint literal al tamaño del archivo:
 
```bash
ls -lS frames/ | head -5
```
 
`frame_45.png` destaca notablemente sobre todos los demás. Al abrirlo se puede ver que no es una cara perturbadora sino un peluche de Oguri Cap de Uma Musume escondido entre los demás frames.
 
### 3. Extraer la flag
 
El enunciado también decía *"trato de no darle importancia"*, hint directo al **LSB** (Least Significant Bit), técnica de esteganografía que oculta información en el bit menos significativo de cada píxel, el bit que menos importa visualmente.
 
```bash
$ zsteg frame_45.png

b1,r,lsb,xy         .. text: "HL4{0gur1_c4p_w31ghs_m0r3_th4n_th3_r3st}"
b1,g,lsb,xy         .. text: "\t(_G~ZVW9"
b2,r,lsb,xy         .. file: OpenPGP Public Key
b2,rgb,msb,xy       .. file: OpenPGP Secret Key
b2,bgr,msb,xy       .. file: OpenPGP Secret Key
```
 
La flag está oculta en el **LSB del canal rojo (R)** del frame_45.
 
Flag: HL4{0gur1_c4p_w31ghs_m0r3_th4n_th3_r3st}