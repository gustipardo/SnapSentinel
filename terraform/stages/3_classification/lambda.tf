resource "aws_lambda_function" "event_classifier" {
  filename      = "./event_classifier.zip"
  function_name = "event_classifier-${var.environment}"
  role          = aws_iam_role.event_classifier_role.arn
  handler       = "event_classifier.lambda_handler"
  runtime       = "python3.9"
  timeout       = 10

  source_code_hash = filebase64sha256("./event_classifier.zip")

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.critical_events.arn
    }
  }
}
