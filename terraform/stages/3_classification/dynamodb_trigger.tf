resource "aws_lambda_event_source_mapping" "dynamodb_trigger" {
  event_source_arn  = data.aws_dynamodb_table.analysis_results.stream_arn
  function_name     = aws_lambda_function.event_classifier.arn
  starting_position = "LATEST"
  batch_size        = 1
  enabled           = true

  depends_on = [
    aws_iam_role_policy.event_classifier_policy
  ]
}
