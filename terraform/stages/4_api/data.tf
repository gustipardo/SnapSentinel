data "aws_dynamodb_table" "analysis_results" {
  name = "analysis_results-${var.environment}"
}

data "aws_s3_bucket" "images" {
  bucket = "snapsentinel-images-${var.environment}"
}
