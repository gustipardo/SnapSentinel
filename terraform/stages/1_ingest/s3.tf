resource "aws_s3_bucket" "raw_snapshots" {
  bucket = "snapsentinel-images-${var.environment}"

  tags = {
    Name = "raw_snapshots"
    Env  = var.environment
  }

  force_destroy = true
}

resource "aws_s3_bucket_versioning" "raw_snapshots" {
  bucket = aws_s3_bucket.raw_snapshots.id

  versioning_configuration {
    status = "Enabled"
  }
}
