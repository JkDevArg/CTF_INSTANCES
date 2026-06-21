# medium-osint-username — SocialTrack Username Chain

**Dificultad**: Media
**Categoria**: OSINT
**Puerto**: 80

## Descripcion

El objetivo usa diferentes usernames en distintas plataformas sociales. Empieza con el perfil conocido en "GitHub" y sigue las pistas entre plataformas. Una bio codificada en ROT13 revela el siguiente paso.

## Como iniciar

```bash
docker-compose up -d
```

Accede en: http://localhost:8080

## Cadena

1. `/github/h4ck3r_jc` — perfil con link a ByteGram
2. `/bytegram/jc_2024` — bio codificada en ROT13 revela `/twitter/elite_jc`
3. `/twitter/elite_jc` — perfil con la flag en el post fijado

## Solucion

```bash
python3 solve.py
# Requiere: pip install requests beautifulsoup4
```

## Concepto

El rastreo de usernames entre plataformas (Sherlock, WhatsMyName) es una tecnica OSINT fundamental. Las personas reusan usernames y dejan pistas cross-platform. ROT13 es un encoding clasico usado como ofuscacion ligera.
