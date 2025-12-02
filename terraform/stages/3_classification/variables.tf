variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "email_address" {
  description = "Email address for SNS subscription"
  type        = string
  default     = "sandbox17201@gmail.com"
}

variable "environment" {
  description = "Deployment environment (dev or prod)"
  type        = string
}

variable "fcm_client_email" {
  description = "FCM Client Email"
  type        = string
  sensitive   = true
}

variable "fcm_private_key" {
  description = "FCM Private Key"
  type        = string
  sensitive   = true
}

variable "fcm_project_id" {
  description = "FCM Project ID"
  type        = string
}
