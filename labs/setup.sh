#!/usr/bin/env bash
# ================================================================
#  setup.sh — Script maestro de despliegue
#  Uso: bash setup.sh [lab01|lab02|lab03|lab04|all]
# ================================================================
set -euo pipefail
C='\033[0;36m'; G='\033[0;32m'; Y='\033[1;33m'; R='\033[0;31m'; B='\033[1m'; N='\033[0m'
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB="${1:-help}"

printf "${C}\n  ╔══════════════════════════════════════════════╗\n"
printf "  ║       ETHICAL HACKING LAB SUITE  v4.0       ║\n"
printf "  ╚══════════════════════════════════════════════╝${N}\n\n"

case "$LAB" in
  lab01|1)
    printf "${B}🚀 Lab 01 — Beginner (DVWA + Splunk + Flask API)${N}\n"
    bash "$DIR/common/scripts/check-deps.sh"
    cd "$DIR/lab01" && docker compose --env-file .env up -d --build
    printf "\n${G}✅ Lab 01 activo:${N}\n"
    printf "   🌐 DVWA       → http://localhost:8080  (admin/password)\n"
    printf "   📊 Splunk     → http://localhost:8000  (admin/lab2024!)\n"
    printf "   🐍 Flask API  → http://localhost:5000\n"
    printf "   💡 DVWA: ve a Setup/Reset DB → Create/Reset Database\n"
    ;;
  lab02|2)
    printf "${B}🚀 Lab 02 — Intermediate (JWT + SSRF + Forense)${N}\n"
    bash "$DIR/common/scripts/check-deps.sh"
    cd "$DIR/lab02" && docker compose --env-file .env up -d --build
    printf "\n${G}✅ Lab 02 activo:${N}\n"
    printf "   🔐 API Gateway   → https://localhost:9443\n"
    printf "   🔬 Forensics     → http://localhost:9090\n"
    printf "   📦 Volatility    → http://localhost:8888\n"
    ;;
  lab03|3)
    printf "${B}🚀 Lab 03 — Advanced (PWN + Reversing + AI Security)${N}\n"
    bash "$DIR/common/scripts/check-deps.sh"
    cd "$DIR/lab03" && docker compose --env-file .env up -d --build
    printf "\n${G}✅ Lab 03 activo:${N}\n"
    printf "   💣 PWN x64    → nc localhost 4444\n"
    printf "   💣 PWN ARM32  → nc localhost 4445\n"
    printf "   🤖 AI Gateway → http://localhost:8181\n"
    printf "   📊 Kibana     → http://localhost:5601\n"
    ;;
  lab04|4)
    printf "${B}🚀 Lab 04 — Expert (Kubernetes + Falco + Terraform)${N}\n"
    bash "$DIR/common/scripts/check-deps.sh"
    bash "$DIR/lab04/setup-k8s.sh"
    ;;
  all)
    bash "$0" lab01; bash "$0" lab02; bash "$0" lab03
    printf "${Y}⚠️  Lab04 requiere Kind+Terraform: bash setup.sh lab04${N}\n"
    ;;
  *)
    printf "Uso: bash setup.sh [lab01|lab02|lab03|lab04|all]\n\n"
    printf "  lab01  Beginner      DVWA, Splunk, Flask API\n"
    printf "  lab02  Intermediate  JWT bypass, SSRF, Forense RAM\n"
    printf "  lab03  Advanced      PWN, Reversing, AI Security\n"
    printf "  lab04  Expert        Kubernetes, Falco, Terraform\n"
    printf "  all    Labs 1-3 automático\n"
    ;;
esac
