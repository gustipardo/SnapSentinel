resource "aws_sns_topic" "critical_events" {
  name = "critical-events-topic-${var.environment}"
}

resource "aws_sns_topic_subscription" "email_target" {
  topic_arn = aws_sns_topic.critical_events.arn
  protocol  = "email"
  endpoint  = var.email_address
}
