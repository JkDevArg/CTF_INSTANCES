# Banco HACKL4BS Vault

Portal privado de transferencias para HACKL4BS 2026.

## Levantar el entorno

```bash
docker compose up --build
```

## Abrir

```txt
http://localhost:8080
```

## Variables principales

La bandera se configura desde el entorno de despliegue. No se incluye ningún valor real en este README.


```txt
INITIAL_BALANCE=20000
MAX_TRANSFER_AMOUNT=100
WINDOW_SECONDS=60
```

## Restaurar estado

Usar el botón `Restaurar entorno` dentro del portal o reiniciar los contenedores con base de datos limpia.
