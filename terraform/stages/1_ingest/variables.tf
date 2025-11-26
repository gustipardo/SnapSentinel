# variables.tf
variable "aws_region" {
  description = "Región AWS donde desplegar"
  type        = string
  default     = "us-east-1" # Puede ser cambiada .tfvars o con -var
}

variable "environment" {
  description = "Deployment environment (dev or prod)"
  type        = string
}




