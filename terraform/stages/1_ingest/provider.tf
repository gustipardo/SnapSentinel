# provider.tf
terraform {
  required_version = ">= 1.0.0" 
  required_providers {
    aws = {
      source  = "hashicorp/aws" // Who maintains the provider
      version = "~> 5.0" // This indicates any version of the AWS provider that is compatible with version 5.x.x
    }
  }
}

# Provider config 
provider "aws" {
  region = var.aws_region # we use a variable define in variables.tf
}
