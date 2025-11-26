resource "aws_lambda_function" "snapshot_ingestor" {
  function_name = "snap_sentinel_snapshot_ingestor-${var.environment}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "snapshot_ingestor.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30

  filename = "snapshot_ingestor.zip"

  source_code_hash = filebase64sha256("snapshot_ingestor.zip")
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.raw_snapshots.bucket
    }
  }
}
