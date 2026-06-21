# RiftHash — Crackme

## Tabla de información

| Campo       | Valor                        |
|-------------|------------------------------|
| ID          | forensic-rifthash            |
| Nombre      | RiftHash                     |
| Categoría   | Forensic                     |
| Dificultad  | Medium                       |
| Puerto      | 80                           |
| Timeout     | 3600 s                       |
| Flag        | HL4{143a_chaos}              |

## Cómo ejecutar (Docker)

```bash
FLAG="HL4{143a_chaos}" docker compose up --build
# Servidor en http://localhost:8080
PORT_80=9090 FLAG="HL4{mi_flag}" docker compose up --build
```

---

Nombre: RiftHash
Nivel: medium
Flag: HL4{143a_chaos}

Descripción:
Un jugador de Riftbound ha estado experimentando con un sistema de contraseñas personalizado para proteger su colección de cartas más valiosa. Lo llama RiftHash, una forma "segura" de generar contraseñas fuertes basadas en sus cartas favoritas.

El único problema es que no es exactamente un experto en criptografía. Solo está usando MD5 como función de hash, y el patrón de sus contraseñas es predecible.

Su tipo de hash personalizado RiftHash es simplemente:

$rift$<versión>$<digest_hex>

Y todas sus contraseñas siguen este esquema:

HL4{<number>_<domain>}

Donde:
- <number> es el número de la carta del set Unleashed (ejemplos: 001, 095, 110b)
- <domain> es uno de los seis dominios: Fury, Calm, Mind, Body, Chaos, Order

Han bloqueado el acceso a su mazo secreto con uno de estos hashes. Si logras crackearlo, quizás obtengas algo valioso a cambio, como sobres de cartas exclusivos.

$rift$1$d57dac6e9f1a91c4e757abdb032997a8

**Nota:** Solo se contemplan los valores mencionados anteriormente para cada campo

## Archivos entregados

- `rifthash.py`
- `rifthash.hash`

## Solucion

El hash resuelto fue:

```
$rift$1$unleashed-lab$ca0fbdf06382365b8bd9ad6e1340778516d9f6c5a3e7135409ffd8f5c23064b8
```

El formato esperado de la flag era:

```
HL4{<number>_<domain>}
```

Con esa informacion, se puede crear una wordlist combinando:

- `number`: valores desde `001` hasta `299`, incluyendo variantes con letra como `143a`
- `domain`: `Fury`, `Calm`, `Mind`, `Body`, `Chaos`, `Order`

Luego se calcula el RiftHash de cada candidato usando la sal `unleashed-lab` y se compara contra el digest entregado.

La combinacion correcta corresponde a la carta `Kha'Zix, Mutating Horror (UNL-143a)`, con dominio `Chaos`.

El candidato encontrado fue:

```
HL4{143a_chaos}
```
