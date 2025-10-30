resource "aws_lambda_function" "snapshot_ingestor" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "snapshot_ingestor.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30

  filename      = "lambda_function.zip"

  source_code_hash = filebase64sha256("lambda_function.zip")
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.raw_snapshots.bucket
    }
  }
}
