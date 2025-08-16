# outputs.tf Info that Terraform will output after running `terraform apply`
output "bucket_name" {
  description = "Nombre del bucket creado"
  value       = aws_s3_bucket.raw_snapshots.bucket // Terraform remembers the bucket by this name
}

output "bucket_arn" {
  description = "ARN del bucket"
  value       = aws_s3_bucket.raw_snapshots.arn
}
