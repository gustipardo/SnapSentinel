data "archive_file" "analyzer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../../lambdas/analyzer"
  output_path = "${path.module}/analyzer.zip"
  excludes    = ["__pycache__", "*.pyc"]
}

resource "aws_lambda_function" "analyzer" {
  filename         = data.archive_file.analyzer_zip.output_path
  function_name    = "snap_sentinel_analyzer"
  role             = aws_iam_role.analyzer_lambda_role.arn
  handler          = "analyzer.lambda_handler"
  source_code_hash = data.archive_file.analyzer_zip.output_base64sha256
  runtime          = "python3.9"
  timeout          = 30

  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }
}
