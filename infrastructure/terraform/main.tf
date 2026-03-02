terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 Buckets
resource "aws_s3_bucket" "images" {
  bucket = "${var.project_name}-images-${var.environment}"
  
  tags = {
    Name        = "Smart Vendors Images"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_s3_bucket" "static_assets" {
  bucket = "${var.project_name}-static-${var.environment}"
  
  tags = {
    Name        = "Smart Vendors Static Assets"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_s3_bucket" "ml_models" {
  bucket = "${var.project_name}-ml-models-${var.environment}"
  
  tags = {
    Name        = "Smart Vendors ML Models"
    Environment = var.environment
    Project     = var.project_name
  }
}

# S3 Bucket Public Access Configuration for Static Assets
resource "aws_s3_bucket_public_access_block" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "static_assets" {
  bucket = aws_s3_bucket.static_assets.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.static_assets.arn}/*"
      }
    ]
  })

  depends_on = [aws_s3_bucket_public_access_block.static_assets]
}

# S3 Bucket CORS Configuration
resource "aws_s3_bucket_cors_configuration" "images" {
  bucket = aws_s3_bucket.images.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

# DynamoDB Tables
resource "aws_dynamodb_table" "vendors" {
  name           = "${var.project_name}-vendors-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "vendor_id"

  attribute {
    name = "vendor_id"
    type = "S"
  }

  attribute {
    name = "phone_number"
    type = "S"
  }

  global_secondary_index {
    name            = "phone_number_index"
    hash_key        = "phone_number"
    projection_type = "ALL"
  }

  tags = {
    Name        = "Smart Vendors - Vendors"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "transactions" {
  name           = "${var.project_name}-transactions-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "transaction_id"

  attribute {
    name = "transaction_id"
    type = "S"
  }

  attribute {
    name = "vendor_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  global_secondary_index {
    name            = "vendor_id_index"
    hash_key        = "vendor_id"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  tags = {
    Name        = "Smart Vendors - Transactions"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "market_prices" {
  name           = "${var.project_name}-market-prices-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "item_name"
  range_key      = "timestamp"

  attribute {
    name = "item_name"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Name        = "Smart Vendors - Market Prices"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "marketplace_listings" {
  name           = "${var.project_name}-marketplace-listings-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "listing_id"

  attribute {
    name = "listing_id"
    type = "S"
  }

  attribute {
    name = "vendor_id"
    type = "S"
  }

  attribute {
    name = "created_at"
    type = "S"
  }

  global_secondary_index {
    name            = "vendor_id_index"
    hash_key        = "vendor_id"
    range_key       = "created_at"
    projection_type = "ALL"
  }

  tags = {
    Name        = "Smart Vendors - Marketplace Listings"
    Environment = var.environment
  }
}

# IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_execution" {
  name = "${var.project_name}-lambda-execution-${var.environment}"

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

  tags = {
    Name        = "Smart Vendors Lambda Execution Role"
    Environment = var.environment
  }
}

# IAM Policy for Lambda to access AWS services
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy-${var.environment}"
  role = aws_iam_role.lambda_execution.id

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
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "${aws_s3_bucket.images.arn}/*",
          "${aws_s3_bucket.static_assets.arn}/*",
          "${aws_s3_bucket.ml_models.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem"
        ]
        Resource = [
          aws_dynamodb_table.vendors.arn,
          aws_dynamodb_table.transactions.arn,
          aws_dynamodb_table.market_prices.arn,
          aws_dynamodb_table.marketplace_listings.arn,
          "${aws_dynamodb_table.vendors.arn}/index/*",
          "${aws_dynamodb_table.transactions.arn}/index/*",
          "${aws_dynamodb_table.marketplace_listings.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "transcribe:StartTranscriptionJob",
          "transcribe:GetTranscriptionJob"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "sagemaker:InvokeEndpoint"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = "*"
      }
    ]
  })
}

# CloudFront Origin Access Identity
resource "aws_cloudfront_origin_access_identity" "static_assets" {
  comment = "OAI for Smart Vendors static assets"
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "frontend" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  price_class         = "PriceClass_100"

  origin {
    domain_name = aws_s3_bucket.static_assets.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.static_assets.id}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.static_assets.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.static_assets.id}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name        = "Smart Vendors Frontend Distribution"
    Environment = var.environment
  }
}

# API Gateway
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.project_name}-api-${var.environment}"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["*"]
    max_age       = 300
  }

  tags = {
    Name        = "Smart Vendors API Gateway"
    Environment = var.environment
  }
}

resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = var.environment
  auto_deploy = true

  tags = {
    Name        = "Smart Vendors API Stage"
    Environment = var.environment
  }
}

# Lambda Layer for shared dependencies
resource "aws_lambda_layer_version" "dependencies" {
  filename            = var.lambda_layer_path
  layer_name          = "${var.project_name}-dependencies-${var.environment}"
  compatible_runtimes = ["python3.11"]
  
  lifecycle {
    create_before_destroy = true
  }
}

# SageMaker Execution Role
resource "aws_iam_role" "sagemaker_execution" {
  name = "${var.project_name}-sagemaker-execution-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "Smart Vendors SageMaker Execution Role"
    Environment = var.environment
  }
}

# SageMaker Execution Policy
resource "aws_iam_role_policy" "sagemaker_policy" {
  name = "${var.project_name}-sagemaker-policy-${var.environment}"
  role = aws_iam_role.sagemaker_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.images.arn}/*",
          "${aws_s3_bucket.ml_models.arn}/*",
          aws_s3_bucket.images.arn,
          aws_s3_bucket.ml_models.arn
        ]
      },
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
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = "*"
      }
    ]
  })
}

# Note: SageMaker Model and Endpoint resources are commented out
# For hackathon demo, use DEMO_MODE=true to bypass SageMaker
# Uncomment and configure these resources when deploying a real model

# resource "aws_sagemaker_model" "produce_classifier" {
#   name               = "${var.project_name}-produce-classifier-${var.environment}"
#   execution_role_arn = aws_iam_role.sagemaker_execution.arn
#
#   primary_container {
#     image          = "your-ecr-image-uri"  # Replace with actual model image
#     model_data_url = "s3://${aws_s3_bucket.ml_models.id}/model.tar.gz"
#   }
#
#   tags = {
#     Name        = "Smart Vendors Produce Classifier"
#     Environment = var.environment
#   }
# }
#
# resource "aws_sagemaker_endpoint_configuration" "produce_classifier" {
#   name = "${var.project_name}-produce-classifier-config-${var.environment}"
#
#   production_variants {
#     variant_name           = "AllTraffic"
#     model_name            = aws_sagemaker_model.produce_classifier.name
#     initial_instance_count = 1
#     instance_type         = "ml.t2.medium"
#   }
#
#   tags = {
#     Name        = "Smart Vendors Endpoint Config"
#     Environment = var.environment
#   }
# }
#
# resource "aws_sagemaker_endpoint" "produce_classifier" {
#   name                 = "${var.project_name}-produce-classifier-${var.environment}"
#   endpoint_config_name = aws_sagemaker_endpoint_configuration.produce_classifier.name
#
#   tags = {
#     Name        = "Smart Vendors Produce Classifier Endpoint"
#     Environment = var.environment
#   }
# }
