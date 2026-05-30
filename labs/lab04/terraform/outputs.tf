output "cluster_name" {
  description = "Nombre del cluster Kind"
  value       = "kind-lab-expert"
}

output "namespace" {
  description = "Namespace de Kubernetes del lab"
  value       = "lab-expert"
}

output "access_command" {
  description = "Comando para acceder a la API vulnerable"
  value       = "kubectl port-forward svc/vulnerable-api 8282:80 -n lab-expert --context kind-lab-expert"
}
