#!/usr/bin/env bash
# ================================================================
#  Lab 04 — Setup Kubernetes con Kind + Terraform
# ================================================================
set -euo pipefail
G='\033[0;32m'; R='\033[0;31m'; Y='\033[1;33m'; N='\033[0m'
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "🔍 Verificando Kind y kubectl..."
command -v kind    &>/dev/null || { echo -e "${R}❌ Kind no encontrado → https://kind.sigs.k8s.io${N}"; exit 1; }
command -v kubectl &>/dev/null || { echo -e "${R}❌ kubectl no encontrado${N}"; exit 1; }

echo "☸️  Creando cluster Kind 'lab-expert'..."
kind create cluster --name lab-expert --config "$DIR/k8s/kind-config.yaml" 2>/dev/null \
  && echo -e "${G}✅ Cluster creado${N}" \
  || echo -e "${Y}⚠️  Cluster ya existe — continuando${N}"

echo "📦 Aplicando manifiestos Kubernetes..."
kubectl apply -f "$DIR/k8s/" --context kind-lab-expert

echo "🦅 Instalando Falco..."
kubectl apply -f "$DIR/falco/" --context kind-lab-expert

echo ""
echo -e "${G}✅ Lab04 Expert activo:${N}"
echo "   kubectl get pods -A --context kind-lab-expert"
echo "   kubectl port-forward svc/vulnerable-api 8282:80 -n lab-expert"
echo ""
if command -v terraform &>/dev/null && [ -d "$DIR/terraform" ]; then
  echo "🌍 Para despliegue cloud (opcional):"
  echo "   cd lab04/terraform && terraform init && terraform plan"
fi
