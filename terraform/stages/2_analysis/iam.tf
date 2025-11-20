resource "aws_iam_role" "analyzer_lambda_role" {
  name = "analyzer_lambda_role"

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

resource "aws_iam_role_policy_attachment" "analyzer_lambda_basic_execution" {
  role       = aws_iam_role.analyzer_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Add S3 read permissions if needed later, but for now basic execution is enough for logging.
# The trigger permission is resource-based on the Lambda, not IAM role based.
# However, if the lambda needs to read the object content (which it will), it needs s3:GetObject.

resource "aws_iam_policy" "analyzer_s3_read_policy" {
  name        = "analyzer_s3_read_policy"
  description = "Allow Analyzer Lambda to read from raw snapshots bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::${var.bucket_name}/*"
      }
    ]
  })
}

resource "aws_iam_policy" "analyzer_rekognition_policy" {
  name        = "analyzer_rekognition_policy"
  description = "Allow Analyzer Lambda to call Rekognition"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "rekognition:DetectLabels"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "analyzer_rekognition_attachment" {
  role       = aws_iam_role.analyzer_lambda_role.name
  policy_arn = aws_iam_policy.analyzer_rekognition_policy.arn
}

resource "aws_iam_policy" "analyzer_dynamodb_policy" {
  name        = "analyzer_dynamodb_policy"
  description = "Allow Analyzer Lambda to write to DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.analysis_results.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "analyzer_dynamodb_attachment" {
  role       = aws_iam_role.analyzer_lambda_role.name
  policy_arn = aws_iam_policy.analyzer_dynamodb_policy.arn
}

resource "aws_iam_role_policy_attachment" "analyzer_s3_read_attachment" {
  role       = aws_iam_role.analyzer_lambda_role.name
  policy_arn = aws_iam_policy.analyzer_s3_read_policy.arn
}
