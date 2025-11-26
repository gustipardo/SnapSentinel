# provider.tf
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws" // Who maintains the provider
      version = "~> 5.0"        // This indicates any version of the AWS provider that is compatible with version 5.x.x
    }
  }

  backend "s3" {
    bucket = "snapsentinel-terraform-state"
    # Actually, the user asked for: "Configurar claves de estado separadas: env/dev/terraform.tfstate y env/prod/terraform.tfstate."
    # Terraform backends do not support variables. We usually use `terraform init -backend-config="key=env/dev/..."` or separate backend config files.
    # However, for simplicity in this task, I might set a default here and override it, or just leave it empty and force passing it?
    # The user said: "Configurar claves de estado separadas".
    # If I hardcode `env/dev/...` then `terraform init` for prod will need `-backend-config="key=env/prod/..."`.
    # I'll stick to hardcoding the bucket and region.
    region         = "us-east-1"
    dynamodb_table = "snapsentinel-terraform-lock"
    encrypt        = true
  }
}

# Provider config 
provider "aws" {
  region = var.aws_region # we use a variable define in variables.tf
}
