resource "aws_s3_bucket" "raw_snapshots" {
  bucket = var.bucket_name

  tags = {
    Name = "raw_snapshots"
    Env  = "dev"
  }

  force_destroy = true
}

resource "aws_s3_bucket_versioning" "raw_snapshots" {
  bucket = aws_s3_bucket.raw_snapshots.id

  versioning_configuration {
    status = "Enabled"
  }
}
