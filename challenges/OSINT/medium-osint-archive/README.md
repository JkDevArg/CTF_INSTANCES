# medium-osint-archive — CorpArchive Web Cache Investigation

**Dificultad**: Media
**Categoría**: OSINT
**Puerto**: 80

## Descripción
NovaCorp mantiene un archivo histórico de su sitio para cumplimiento normativo. La versión actual del sitio no contiene información sensible, pero una versión archivada de julio 2024 tiene una página eliminada con datos comprometidos.

## Cómo iniciar
```bash
docker-compose up -d
```
Accede en: http://localhost:8080

## Solución
```bash
# Explorar el archivo
curl http://localhost:8080/archive/
curl http://localhost:8080/archive/2024-07/
curl http://localhost:8080/archive/2024-07/announcements

# Automatizado
python3 solve.py
```

## Concepto
El Wayback Machine y otros archivos web conservan páginas eliminadas. En investigaciones OSINT, el historial archivado puede revelar credenciales, emails o información que fue "borrada" del sitio actual pero persiste en cachés.
