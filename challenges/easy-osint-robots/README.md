# easy-osint-robots — CorpSite Robots.txt Recon

**Dificultad**: Fácil  
**Categoría**: OSINT  
**Puerto**: 80

## Descripción
El sitio corporativo de CorpSite tiene un archivo `robots.txt` que revela rutas internas no indexadas. Una de esas rutas lleva directamente a información sensible.

## Cómo iniciar
```bash
docker-compose up -d
```
Accede en: http://localhost:8080

## Solución
```bash
# Revisar robots.txt
curl http://localhost:8080/robots.txt

# Acceder al path oculto
curl http://localhost:8080/admin/vault/
```

## Concepto
El archivo `robots.txt` es público por diseño. Al listar rutas con `Disallow:`, inadvertidamente se revela la estructura interna del sitio. Una ruta listada como prohibida para bots puede contener información sensible accesible para humanos.
