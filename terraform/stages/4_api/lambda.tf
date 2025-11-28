resource "aws_lambda_function" "api_handler" {
  filename      = "./api_handler.zip"
  function_name = "api_handler-${var.environment}"
  role          = aws_iam_role.api_handler_role.arn
  handler       = "api_handler.lambda_handler"
  runtime       = "python3.9"
  timeout       = 10

  source_code_hash = filebase64sha256("./api_handler.zip")

  environment {
    variables = {
      DYNAMODB_TABLE = data.aws_dynamodb_table.analysis_results.name
    }
  }
}
