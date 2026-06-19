# easy-osint-headers — DataAPI Corp HTTP Headers

**Dificultad**: Facil
**Categoria**: OSINT
**Puerto**: 80

## Descripcion

La API corporativa de DataAPI Corp incluye headers HTTP personalizados en todas sus respuestas. Inspecciona los headers de respuesta para encontrar la flag.

## Como iniciar

```bash
docker-compose up -d
```

Accede en: http://localhost:8080

## Solucion

```bash
# Con curl
curl -I http://localhost:8080/
curl -I http://localhost:8080/api/status

# Con Python
python3 solve.py
```

## Concepto

Los headers HTTP de respuesta pueden revelar informacion interna: versiones de software, tokens, configuracion del servidor. Herramientas como `curl -I`, Burp Suite o el tab Network del navegador los muestran.
