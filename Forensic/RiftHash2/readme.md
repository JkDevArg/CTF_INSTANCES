Nombre: RiftHash2
Nivel: medium
Flag: HL4{sfd_111_body_rare_spell}

Descripción:
Después de que alguien crackeara su primer sistema RiftHash, nuestro jugador de Riftbound decidió mejorar su seguridad. Ahora presenta RiftHash2, una versión mejorada que incluye más parámetros en la flag para hacerla más resistente a ataques de fuerza bruta.

El único problema es que sigue siendo predecible. A pesar de haber añadido más campos, sigue usando MD5 como función de hash, y el patrón de sus contraseñas sigue siendo fácil de deducir si conoces las cartas.

Su tipo de hash personalizado RiftHash es simplemente:

$rift$<version>$<digest_hex>

Y todas sus contraseñas siguen este esquema:

HL4{<set>_<number>_<domain>_<rarity>_<type>}

Donde:
- <set> es el set de la carta: Origins Proving Grounds, Spiritforged o Unleashed
- <number> es el número de la carta (ejemplos: 001, 095, 110b)
- <domain> es uno de los seis dominios: Fury, Calm, Mind, Body, Chaos, Order
- <rarity> es la rareza de la carta: Common, Uncommon, Rare, Epic
- <type> es el tipo de carta: Champion, Legend, Spell, Unit, Rune, Gear, Battlefield, Token

Han bloqueado el acceso a su mazo secreto con uno de estos hashes. Si logras crackearlo, quizás obtengas algo valioso a cambio, como sobres de cartas exclusivos.

$rift$2$99e31d9f4944ed540545b00d95746a57

**Nota:** Solo se contemplan los valores mencionados anteriormente para cada campo.

## Archivos entregados

- `rifthash2.py`
- `rifthash2.hash`

## Solucion

El hash resuelto fue:

```
$rift$2$ogs-sfd-unl$d5ac90b87b14b8b8c9789bfe1547643f8146f1806b14e05576a5ea8e1e5e9cdf
```

El formato esperado de la flag era:

```
HL4{<set>_<number>_<domain>_<rarity>_<type>}
```

Con ese patron, se puede crear una wordlist combinando:

- `set`: `OGS`, `SFD`, `UNL`
- `number`: valores desde `001` hasta `299`
- `domain`: `Fury`, `Calm`, `Mind`, `Body`, `Chaos`, `Order`
- `rarity`: `Common`, `Uncommon`, `Rare`, `Epic`
- `type`: `Champion`, `Legend`, `Spell`, `Unit`, `Rune`, `Gear`, `Battlefield`, `Token`

Luego se calcula el RiftHash2 de cada candidato usando la sal `ogs-sfd-unl` y se compara contra el digest entregado.

La combinacion correcta corresponde a la carta `Grim Resolve (SFD-111)`, con dominio `Body`, rareza `Rare` y tipo `Spell`.

El candidato encontrado fue:

```
HL4{SFD_111_Body_Rare_Spell}
```
