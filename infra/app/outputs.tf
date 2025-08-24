output "bucket_name" {
  description = "Nombre del bucket creado"
  value       = aws_s3_bucket.raw_snapshots.bucket
}

output "bucket_arn" {
  description = "ARN del bucket"
  value       = aws_s3_bucket.raw_snapshots.arn
}
