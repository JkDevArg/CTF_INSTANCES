# PickleCorp — Pickle Deserialization

Dificultad: Hard | Categoría: Web | Técnica: Python Pickle Deserialization RCE

## Descripción

PickleCorp es un portal de empleados que almacena la sesión del usuario en una cookie serializada con `pickle`. Al iniciar sesión, el servidor crea un objeto `UserSession`, lo serializa con `pickle.dumps()` y lo codifica en base64 para enviarlo como cookie.

En cada petición, la cookie se decodifica y se deserializa con `pickle.loads()` sin verificar su integridad ni autenticidad.

## Vulnerabilidad

**Python Pickle Deserialization** es una vulnerabilidad crítica: `pickle.loads()` puede ejecutar código arbitrario durante la deserialización si el objeto contiene un método `__reduce__`.

Un atacante puede construir un pickle malicioso localmente y enviarlo como cookie, ejecutando cualquier comando en el servidor.

```python
class RCEPayload:
    def __reduce__(self):
        import os
        return (os.system, ('cat /flag.txt',))
```

## Objetivo

Obtener la flag mediante uno de estos métodos:

- **Opción A (simple)**: forjar un objeto `UserSession` con `role='admin'` para que la app muestre la flag en el dashboard.
- **Opción B (RCE)**: usar `__reduce__` para ejecutar comandos en el servidor.

## Levantar el entorno

```bash
docker compose up --build
# Disponible en http://localhost:8080
```

## Ejecutar el solver

```bash
pip install requests
python3 solve.py
```

## Mitigación

Nunca deserializar datos no confiables con pickle. Usar formatos seguros como JSON con validación de esquema, o firmar las cookies con `itsdangerous`/`Flask-Session` y almacenar la sesión en el servidor.
