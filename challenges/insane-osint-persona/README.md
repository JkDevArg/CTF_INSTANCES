# insane-osint-persona — Project TURING Full Persona Investigation

**Dificultad**: Insane
**Categoria**: OSINT
**Puerto**: 80

## Descripcion

Investigacion completa de un whistleblower conocido como "Alex Turing". La flag esta oculta al final de una cadena de 5 pasos a traves de plataformas simuladas, con encoding en dos capas al final.

## Como iniciar

```bash
docker-compose up -d
```

Accede en: http://localhost:8080

## Cadena de investigacion

1. `/` — articulo de noticias sobre Alex Turing
2. `/linkedin/alex-turing` — perfil LinkedIn con pista al GitLab y metodo de cifrado
3. `/gitlab/a_turing` — perfil GitLab con repo personal
4. `/gitlab/a_turing/personal-backup` — README menciona `/paste/b4ckup_2024`
5. `/paste/b4ckup_2024` — contenido codificado: ROT13(base64(FLAG))

## Decodificacion

```python
import base64, codecs
encoded = "..."  # contenido del paste
b64 = codecs.decode(encoded, 'rot13')  # deshacer ROT13 primero
flag = base64.b64decode(b64).decode()  # luego base64
```

## Solucion

```bash
python3 solve.py
```

## Concepto

La investigacion de personas digitales (persona OSINT) requiere rastrear huellas digitales a traves de multiples plataformas. El encoding en capas (base64 + ROT13) representa tecnicas rudimentarias de ofuscacion que aparecen en contextos reales de OSINT.

## Encoding detalle

- Aplicado: `base64(FLAG)` -> luego `ROT13(resultado)`
- Para invertir: `ROT13(paste)` -> obtiene base64 -> `base64decode()` -> FLAG
- La pista esta en el LinkedIn: "siempre uso ROT para mis memos"
- El hint en el paste: "dos capas, el ultimo primero" confirma deshacer ROT13 antes que base64
