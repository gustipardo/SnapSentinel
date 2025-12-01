resource "aws_iam_role" "api_handler_role" {
  name = "api_handler_role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "api_handler_policy" {
  name = "api_handler_policy-${var.environment}"
  role = aws_iam_role.api_handler_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Query",
          "dynamodb:GetItem"
        ]
        Resource = [
          data.aws_dynamodb_table.analysis_results.arn,
          "${data.aws_dynamodb_table.analysis_results.arn}/index/AlertsByIndex"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject"
        ]
        Resource = [
          "${data.aws_s3_bucket.images.arn}/*"
        ]
      }
    ]
  })
}
