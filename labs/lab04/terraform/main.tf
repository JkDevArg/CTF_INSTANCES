# ================================================================
# Lab04 Terraform — Infraestructura Cloud (opcional)
# Provider: local (para pruebas sin nube real)
# ================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

provider "local" {}

# Variables del laboratorio
variable "lab_name" {
  default = "lab04-expert"
}

variable "environment" {
  default = "lab"
  validation {
    condition     = var.environment == "lab"
    error_message = "Solo el entorno 'lab' está permitido en este ejercicio."
  }
}

# Genera el archivo kubeconfig del lab
resource "local_file" "lab_config" {
  filename = "${path.module}/output/lab-config.yaml"
  content  = <<-CONFIG
    # Lab04 Configuration
    lab_name: ${var.lab_name}
    environment: ${var.environment}
    cluster: kind-lab-expert
    namespace: lab-expert
    created_at: ${timestamp()}
  CONFIG
}

# Script de setup del cluster
resource "local_file" "setup_script" {
  filename        = "${path.module}/output/setup.sh"
  file_permission = "0755"
  content         = <<-SCRIPT
    #!/usr/bin/env bash
    # Auto-generado por Terraform
    echo "Configurando cluster para ${var.lab_name}..."
    kubectl apply -f ../k8s/ --context kind-lab-expert
    kubectl apply -f ../falco/ --context kind-lab-expert
    echo "✅ Lab04 configurado"
  SCRIPT
}

resource "null_resource" "lab_info" {
  provisioner "local-exec" {
    command = "echo '✅ Terraform: Lab04 infrastructure defined for ${var.lab_name}'"
  }
}

output "lab_name" {
  value = var.lab_name
}

output "next_steps" {
  value = "kubectl get pods -A --context kind-lab-expert"
}
