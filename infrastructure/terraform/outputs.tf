output "s3_bucket_images" {
  description = "S3 bucket name for images"
  value       = aws_s3_bucket.images.id
}

output "s3_bucket_static_assets" {
  description = "S3 bucket name for static assets"
  value       = aws_s3_bucket.static_assets.id
}

output "s3_bucket_ml_models" {
  description = "S3 bucket name for ML models"
  value       = aws_s3_bucket.ml_models.id
}

output "dynamodb_table_vendors" {
  description = "DynamoDB table name for vendors"
  value       = aws_dynamodb_table.vendors.name
}

output "dynamodb_table_transactions" {
  description = "DynamoDB table name for transactions"
  value       = aws_dynamodb_table.transactions.name
}

output "dynamodb_table_market_prices" {
  description = "DynamoDB table name for market prices"
  value       = aws_dynamodb_table.market_prices.name
}

output "dynamodb_table_marketplace_listings" {
  description = "DynamoDB table name for marketplace listings"
  value       = aws_dynamodb_table.marketplace_listings.name
}

output "lambda_execution_role_arn" {
  description = "ARN of Lambda execution role"
  value       = aws_iam_role.lambda_execution.arn
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.frontend.id
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "api_gateway_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.main.api_endpoint
}

output "api_gateway_id" {
  description = "API Gateway ID"
  value       = aws_apigatewayv2_api.main.id
}
