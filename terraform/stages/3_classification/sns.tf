resource "aws_sns_topic" "critical_events" {
  name = "critical-events-topic-${var.environment}"
}

resource "aws_sns_topic_subscription" "email_target" {
  topic_arn = aws_sns_topic.critical_events.arn
  protocol  = "email"
  endpoint  = var.email_address
}

resource "aws_sns_topic_subscription" "lambda_target" {
  topic_arn = aws_sns_topic.critical_events.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.notification_sender.arn
}
