# medium-osint-email — CorpMail Email Header Investigation

**Dificultad**: Media
**Categoría**: OSINT
**Puerto**: 80

## Descripción
Un email corporativo interceptado contiene información oculta en sus headers. Los clientes de correo normales no muestran todos los headers — necesitas analizar el archivo .eml directamente.

## Cómo iniciar
```bash
docker-compose up -d
```
Accede en: http://localhost:8080

## Solución
```bash
# Descargar el email
curl -o email.eml http://localhost:8080/email

# Ver todos los headers
cat email.eml | head -30

# Decodificar el header X-Correlation-ID
python3 -c "import base64; print(base64.b64decode('VALOR_AQUI').decode())"

# Automatizado
python3 solve.py
```

## Concepto
Los headers de email (RFC 2822) pueden contener campos personalizados (X-*) con información no visible en clientes de correo convencionales. Herramientas como `email` de Python, `swaks`, o análisis manual del .eml revelan estos datos.
