resource "aws_dynamodb_table" "analysis_results" {
  name         = "analysis_results-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "image_id"
  range_key    = "timestamp"

  attribute {
    name = "image_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = {
    Name = "analysis_results"
    Env  = var.environment
  }

  stream_enabled   = true
  stream_view_type = "NEW_IMAGE"
}
