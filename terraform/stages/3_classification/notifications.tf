resource "aws_lambda_function" "notification_sender" {
  filename      = "./notification_sender.zip"
  function_name = "notification_sender-${var.environment}"
  role          = aws_iam_role.notification_sender_role.arn
  handler       = "notification_sender.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30

  source_code_hash = filebase64sha256("./notification_sender.zip")

  layers = [aws_lambda_layer_version.google_auth_layer.arn]

  environment {
    variables = {
      FCM_CLIENT_EMAIL = var.fcm_client_email
      FCM_PRIVATE_KEY  = var.fcm_private_key
      FCM_PROJECT_ID   = var.fcm_project_id
    }
  }
}

resource "aws_lambda_permission" "sns_invoke" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.notification_sender.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.critical_events.arn
}

resource "aws_lambda_layer_version" "google_auth_layer" {
  filename   = "google_auth_layer.zip"
  layer_name = "google-auth-layer-${var.environment}"

  compatible_runtimes = ["python3.12"]
}
