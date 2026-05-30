variable "lab_name" {
  description = "Nombre del laboratorio"
  type        = string
  default     = "lab04-expert"
}

variable "environment" {
  description = "Entorno de despliegue (solo 'lab' permitido)"
  type        = string
  default     = "lab"
}
