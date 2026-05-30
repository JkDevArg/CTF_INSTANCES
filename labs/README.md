# Ethical Hacking Lab Suite v4.0

Suite completa de laboratorios de ciberseguridad progresivos.
Diseñada para aprendizaje práctico en entornos 100% aislados.

## Requisitos del sistema

| Herramienta | Versión mínima | Labs que la usan |
|-------------|----------------|-----------------|
| Docker Engine | 24.0+ | Lab01–Lab03 |
| Docker Compose | v2 (plugin) | Lab01–Lab03 |
| Kind | 0.20+ | Lab04 |
| kubectl | 1.28+ | Lab04 |
| Terraform | 1.5+ | Lab04 (opcional) |
| RAM | 8 GB | Suite completa |
| Disco | 20 GB | Suite completa |

## Inicio rápido

```bash
# 1. Verificar dependencias
bash setup.sh

# 2. Desplegar un lab específico
bash setup.sh lab01     # Beginner
bash setup.sh lab02     # Intermediate
bash setup.sh lab03     # Advanced
bash setup.sh lab04     # Expert

# 3. O usar Make
make lab01
make all
```

## Estructura del proyecto

```
ethical-hacking-labs/
├── setup.sh              ← Script maestro
├── Makefile              ← Targets de despliegue
├── README.md             ← Este archivo
├── common/
│   └── scripts/
│       └── check-deps.sh ← Verificación de dependencias
├── lab01/                ← Beginner: DVWA + Splunk + Flask
├── lab02/                ← Intermediate: JWT + SSRF + Forense
├── lab03/                ← Advanced: PWN + Reversing + AI Security
├── lab04/                ← Expert: Kubernetes + Falco + Terraform
└── web/                  ← Portal web navegable
    └── index.html        ← Abre en el navegador
```

## Flujo de aprendizaje

```
Lab01 BEGINNER    → Reconocimiento, SQLi, Brute Force, Splunk SPL
       ↓
Lab02 INTERMEDIATE → JWT bypass, SSRF, Forense RAM, Criptoanálisis
       ↓
Lab03 ADVANCED    → Buffer Overflow, Reversing, AI Security
       ↓
Lab04 EXPERT      → Container Escape, K8s Takeover, Falco Hunting
```

## Detener y limpiar

```bash
make stop     # Detiene todos los labs
make clean    # Detiene + elimina volúmenes e imágenes
```

## Aviso legal

Estos laboratorios son para uso educativo en entornos aislados.
No usar las técnicas aprendidas contra sistemas sin autorización escrita.
