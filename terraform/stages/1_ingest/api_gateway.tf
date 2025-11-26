resource "aws_api_gateway_rest_api" "snapshot_api" {
  name        = "snapshot-api-${var.environment}"
  description = "API para recibir snapshots"
}

// Resource, means endpoint in API Gateway, in this case /snapshot
resource "aws_api_gateway_resource" "snapshot_resource" {
  rest_api_id = aws_api_gateway_rest_api.snapshot_api.id
  parent_id   = aws_api_gateway_rest_api.snapshot_api.root_resource_id
  path_part   = "snapshot"
}

// Method, means HTTP method for the endpoint, in this case POST
resource "aws_api_gateway_method" "post_snapshot" {
  rest_api_id   = aws_api_gateway_rest_api.snapshot_api.id
  resource_id   = aws_api_gateway_resource.snapshot_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

// Integration, means how the method connects to the backend, in this case Lambda
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.snapshot_api.id
  resource_id             = aws_api_gateway_resource.snapshot_resource.id
  http_method             = aws_api_gateway_method.post_snapshot.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.snapshot_ingestor.invoke_arn
}

// Allow API Gateway to invoke the Lambda function
resource "aws_lambda_permission" "apigw_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.snapshot_ingestor.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.snapshot_api.execution_arn}/*/*"
}


resource "aws_api_gateway_deployment" "snapshot_deployment" {
  rest_api_id = aws_api_gateway_rest_api.snapshot_api.id

  depends_on = [
    aws_api_gateway_integration.lambda_integration
  ]
}

resource "aws_api_gateway_stage" "dev" {
  stage_name    = "dev"
  rest_api_id   = aws_api_gateway_rest_api.snapshot_api.id
  deployment_id = aws_api_gateway_deployment.snapshot_deployment.id
}

output "api_invoke_url" {
  value = aws_api_gateway_stage.dev.invoke_url
}
