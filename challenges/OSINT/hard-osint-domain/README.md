# hard-osint-domain — DomainRecon WHOIS & CT Log Investigation

**Dificultad**: Difícil  
**Categoría**: OSINT  
**Puerto**: 80

## Descripción
El dominio `corpcorp.local` tiene información sensible distribuida entre su registro WHOIS y sus entradas en logs de Certificate Transparency. Cada fuente contiene la mitad del flag, codificada en base64.

## Cómo iniciar
```bash
docker-compose up -d
```
Accede en: http://localhost:8080

## Solución
```bash
# Consultar WHOIS
curl "http://localhost:8080/whois?domain=corpcorp.local"

# Consultar CT Log
curl "http://localhost:8080/ct-log?domain=corpcorp.local"

# Decodificar y concatenar (Python)
python3 solve.py
```

## Concepto
WHOIS y Certificate Transparency logs son fuentes de inteligencia pública fundamentales en OSINT. Crt.sh, Shodan y RDAP usan estos datos. Los registrantes a veces exponen información sensible en campos como email o SAN de certificados.
