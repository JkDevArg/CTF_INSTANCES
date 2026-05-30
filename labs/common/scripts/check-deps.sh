#!/usr/bin/env bash
set -euo pipefail
G='\033[0;32m'; R='\033[0;31m'; Y='\033[1;33m'; N='\033[0m'
FAIL=0
ok()   { printf "  ${G}✓${N} %s\n" "$1"; }
warn() { printf "  ${Y}⚠${N}  %s\n" "$1"; }
fail() { printf "  ${R}✗${N} %s\n" "$1"; FAIL=1; }

echo ""
echo "════════════════════════════════════════"
echo "  Verificando dependencias del sistema  "
echo "════════════════════════════════════════"

command -v docker &>/dev/null \
  && ok "Docker $(docker --version | awk '{print $3}' | tr -d ',')" \
  || fail "Docker no encontrado → https://docs.docker.com/get-docker/"

docker compose version &>/dev/null 2>&1 \
  && ok "Docker Compose (plugin)" \
  || { command -v docker-compose &>/dev/null \
    && ok "docker-compose (standalone)" \
    || fail "Docker Compose no encontrado"; }

docker info &>/dev/null 2>&1 \
  && ok "Docker daemon activo" \
  || fail "Docker daemon no corre → sudo systemctl start docker"

command -v git &>/dev/null && ok "Git $(git --version | awk '{print $3}')" || warn "Git no encontrado (opcional)"
command -v curl &>/dev/null && ok "curl disponible" || warn "curl no encontrado"
command -v python3 &>/dev/null && ok "Python $(python3 --version | awk '{print $2}')" || warn "Python3 no encontrado"

command -v kind &>/dev/null \
  && ok "Kind disponible — Lab04 listo" \
  || warn "Kind no encontrado — Lab04 no disponible → https://kind.sigs.k8s.io"

command -v kubectl &>/dev/null && ok "kubectl disponible" || warn "kubectl no encontrado (solo Lab04)"
command -v terraform &>/dev/null && ok "Terraform disponible" || warn "Terraform no encontrado (solo Lab04)"

RAM=$(free -g 2>/dev/null | awk '/^Mem:/{print $2}' || echo 0)
[ "$RAM" -ge 8 ] 2>/dev/null && ok "RAM: ${RAM}GB" || warn "RAM: ${RAM}GB — se recomiendan 8GB+"

echo ""
[ "$FAIL" -eq 0 ] && printf "${G}✅ Sistema listo${N}\n\n" || { printf "${R}❌ Faltan dependencias críticas${N}\n\n"; exit 1; }
