# variables.tf
variable "aws_region" {
  description = "Región AWS donde desplegar"
  type        = string
  default     = "us-east-1" # Puede ser cambiada .tfvars o con -var
}

variable "bucket_name" { // Como no tiene default es obligatorio definirlo en terraform.tfvar
  description = "Nombre del bucket S3 (debe ser único a nivel mundial)"
  type        = string
}


variable "lambda_function_name" {
  type    = string
  default = "SnapshotIngestor"
}

