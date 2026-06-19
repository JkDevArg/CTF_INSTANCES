# hard-osint-chain — CorpLeak Multi-Step OSINT Chain

**Dificultad**: Difícil
**Categoría**: OSINT
**Puerto**: 80

## Descripción

Una cadena de pistas conecta un blog de noticias, un repositorio de GitHub y un paste anónimo. La flag está codificada en hexadecimal al final de la cadena.

## Cómo iniciar

```bash
docker-compose up -d
```

Accede en: http://localhost:8080

## Cadena de pistas

1. `/` — artículo de TechLeaks sobre filtración en CorpCorp
2. `/blog/post/leaked-config` — menciona el repositorio `corpcorp/configs` en GitHub
3. `/github/corpcorp/configs` — commit message urgente revela URL del paste: `/paste/abc123`
4. `/paste/abc123` — FLAG codificada en hexadecimal

## Solución

```bash
python3 solve.py
# o con host remoto:
python3 solve.py http://<ip>:<puerto>
```

## Concepto educativo

El rastreo multi-plataforma (blog → GitHub commits → paste) es una técnica avanzada de OSINT. Los mensajes de commit de Git son permanentes e indexados por motores de búsqueda — nunca incluir URLs, tokens o credenciales en mensajes de commit, aunque el archivo sea eliminado posteriormente.

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `FLAG`   | Flag a entregar. Ejemplo: `CTF{git_commits_never_lie_abc123}` |
| `PORT_80`| Puerto externo (default: `8080`) |
