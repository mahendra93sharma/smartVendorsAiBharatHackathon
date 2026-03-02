# Smart Vendors - AWS Deployment Checklist

## Prerequisites

- [ ] AWS Account with appropriate permissions
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] Docker installed and running
- [ ] Node.js 18+ and npm installed
- [ ] Python 3.11+ installed

## Step 1: Verify AWS Credentials

```bash
aws sts get-caller-identity
```

Expected output should show your AWS account ID and user ARN.

## Step 2: Set Environment Variables

Create a `.env` file in the root directory:

```bash
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your-account-id
S3_BUCKET_STATIC=smart-vendors-static-dev
S3_BUCKET_IMAGES=smart-vendors-images-dev
DYNAMODB_TABLE_PREFIX=smart-vendors-dev
API_GATEWAY_STAGE=dev
```

## Step 3: Create AWS Infrastructure

### 3.1 Create S3 Buckets

```bash
# Static assets bucket
aws s3 mb s3://smart-vendors-static-dev --region us-east-1

# Images bucket
aws s3 mb s3://smart-vendors-images-dev --region us-east-1

# Enable public read for static bucket
aws s3api put-bucket-policy --bucket smart-vendors-static-dev --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::smart-vendors-static-dev/*"
  }]
}'
```

### 3.2 Create DynamoDB Tables

```bash
# Vendors table
aws dynamodb create-table \
  --table-name smart-vendors-dev-vendors \
  --attribute-definitions AttributeName=vendor_id,AttributeType=S \
  --key-schema AttributeName=vendor_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# Transactions table
aws dynamodb create-table \
  --table-name smart-vendors-dev-transactions \
  --attribute-definitions \
    AttributeName=transaction_id,AttributeType=S \
    AttributeName=vendor_id,AttributeType=S \
  --key-schema AttributeName=transaction_id,KeyType=HASH \
  --global-secondary-indexes \
    "IndexName=vendor_id-index,KeySchema=[{AttributeName=vendor_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# Market Prices table
aws dynamodb create-table \
  --table-name smart-vendors-dev-market-prices \
  --attribute-definitions \
    AttributeName=item_name,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=item_name,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1

# Marketplace Listings table
aws dynamodb create-table \
  --table-name smart-vendors-dev-marketplace-listings \
  --attribute-definitions \
    AttributeName=listing_id,AttributeType=S \
    AttributeName=vendor_id,AttributeType=S \
  --key-schema AttributeName=listing_id,KeyType=HASH \
  --global-secondary-indexes \
    "IndexName=vendor_id-index,KeySchema=[{AttributeName=vendor_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### 3.3 Create IAM Role for Lambda

```bash
# Create trust policy
cat > lambda-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF

# Create role
aws iam create-role \
  --role-name smart-vendors-lambda-role \
  --assume-role-policy-document file://lambda-trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name smart-vendors-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name smart-vendors-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

aws iam attach-role-policy \
  --role-name smart-vendors-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-role-policy \
  --role-name smart-vendors-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonTranscribeFullAccess

aws iam attach-role-policy \
  --role-name smart-vendors-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam attach-role-policy \
  --role-name smart-vendors-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
```

## Step 4: Deploy Lambda Functions

### 4.1 Package Lambda Layer (Dependencies)

```bash
cd backend

# Create layer directory
mkdir -p layer/python

# Install dependencies
pip install -r layer_requirements.txt -t layer/python/

# Create layer zip
cd layer
zip -r ../lambda-layer.zip python/
cd ..

# Create Lambda layer
aws lambda publish-layer-version \
  --layer-name smart-vendors-dependencies \
  --zip-file fileb://lambda-layer.zip \
  --compatible-runtimes python3.11 \
  --region us-east-1
```

### 4.2 Deploy Each Lambda Function

Get the Lambda role ARN:
```bash
LAMBDA_ROLE_ARN=$(aws iam get-role --role-name smart-vendors-lambda-role --query 'Role.Arn' --output text)
LAYER_ARN=$(aws lambda list-layer-versions --layer-name smart-vendors-dependencies --query 'LayerVersions[0].LayerVersionArn' --output text)
```

Deploy functions:

```bash
cd lambda_functions

# Function 1: Voice Transcribe
cd voice_transcribe
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-voice-transcribe \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev,S3_BUCKET_IMAGES=smart-vendors-images-dev}" \
  --region us-east-1
cd ..

# Function 2: Create Transaction
cd create_transaction
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-create-transaction \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev}" \
  --region us-east-1
cd ..

# Function 3: Get Transactions
cd get_transactions
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-get-transactions \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev}" \
  --region us-east-1
cd ..

# Function 4: Get Market Prices
cd get_market_prices
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-get-market-prices \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev}" \
  --region us-east-1
cd ..

# Function 5: Classify Freshness
cd classify_freshness
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-classify-freshness \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev,S3_BUCKET_IMAGES=smart-vendors-images-dev}" \
  --region us-east-1
cd ..

# Function 6: Create Marketplace Listing
cd create_marketplace_listing
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-create-marketplace-listing \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev}" \
  --region us-east-1
cd ..

# Function 7: Get Marketplace Buyers
cd get_marketplace_buyers
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-get-marketplace-buyers \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev}" \
  --region us-east-1
cd ..

# Function 8: Notify Marketplace Buyers
cd notify_marketplace_buyers
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-notify-marketplace-buyers \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev}" \
  --region us-east-1
cd ..

# Function 9: Get Trust Score
cd get_trust_score
zip -r function.zip .
aws lambda create-function \
  --function-name smart-vendors-get-trust-score \
  --runtime python3.11 \
  --role $LAMBDA_ROLE_ARN \
  --handler handler.lambda_handler \
  --zip-file fileb://function.zip \
  --layers $LAYER_ARN \
  --timeout 30 \
  --memory-size 256 \
  --environment Variables="{DYNAMODB_TABLE_PREFIX=smart-vendors-dev}" \
  --region us-east-1
cd ..
```

## Step 5: Create API Gateway

```bash
# Create REST API
API_ID=$(aws apigatewayv2 create-api \
  --name smart-vendors-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:us-east-1:$AWS_ACCOUNT_ID:function:smart-vendors-voice-transcribe \
  --query 'ApiId' \
  --output text)

echo "API ID: $API_ID"

# Create routes for each Lambda function
# Voice transcribe
aws apigatewayv2 create-integration \
  --api-id $API_ID \
  --integration-type AWS_PROXY \
  --integration-uri arn:aws:lambda:us-east-1:$AWS_ACCOUNT_ID:function:smart-vendors-voice-transcribe \
  --payload-format-version 2.0

# Add more routes as needed...

# Deploy API
aws apigatewayv2 create-stage \
  --api-id $API_ID \
  --stage-name dev \
  --auto-deploy

# Get API endpoint
API_ENDPOINT=$(aws apigatewayv2 get-api --api-id $API_ID --query 'ApiEndpoint' --output text)
echo "API Endpoint: $API_ENDPOINT"
```

## Step 6: Seed Demo Data

```bash
cd backend
python seed_data.py
```

## Step 7: Build and Deploy Frontend

```bash
cd frontend

# Update API endpoint in .env
echo "VITE_API_BASE_URL=$API_ENDPOINT" > .env

# Build
npm run build

# Deploy to S3
aws s3 sync dist/ s3://smart-vendors-static-dev/ --delete

# Enable website hosting
aws s3 website s3://smart-vendors-static-dev/ \
  --index-document index.html \
  --error-document index.html
```

## Step 8: Create CloudFront Distribution (Optional)

```bash
# Create CloudFront distribution for better performance
aws cloudfront create-distribution \
  --origin-domain-name smart-vendors-static-dev.s3.amazonaws.com \
  --default-root-object index.html
```

## Step 9: Verification

- [ ] All Lambda functions deployed successfully
- [ ] DynamoDB tables created and populated with demo data
- [ ] S3 buckets created and accessible
- [ ] API Gateway configured and returning responses
- [ ] Frontend deployed and accessible
- [ ] Demo credentials work: username "demo_vendor", password "hackathon2024"
- [ ] Voice transcription feature works
- [ ] Price intelligence feature works
- [ ] Freshness scanner feature works
- [ ] Marketplace feature works
- [ ] Trust Score feature works

## Step 10: Get URLs

```bash
# Frontend URL
echo "Frontend: http://smart-vendors-static-dev.s3-website-us-east-1.amazonaws.com"

# API URL
echo "API: $API_ENDPOINT"
```

## Troubleshooting

### Lambda Functions Not Working
- Check CloudWatch Logs: `aws logs tail /aws/lambda/smart-vendors-voice-transcribe --follow`
- Verify IAM permissions
- Check environment variables

### DynamoDB Access Issues
- Verify table names match environment variables
- Check IAM role has DynamoDB permissions

### S3 Upload Failures
- Verify bucket policies allow public read
- Check CORS configuration

### API Gateway 502 Errors
- Check Lambda function logs
- Verify Lambda integration configuration
- Check timeout settings

## Cost Estimation

- Lambda: ~$5-10/month (free tier covers most usage)
- DynamoDB: ~$2-5/month (on-demand pricing)
- S3: ~$1-2/month
- API Gateway: ~$3-5/month
- Total: ~$11-22/month for development

## Cleanup (When Done)

```bash
# Delete Lambda functions
aws lambda delete-function --function-name smart-vendors-voice-transcribe
# ... repeat for all functions

# Delete DynamoDB tables
aws dynamodb delete-table --table-name smart-vendors-dev-vendors
# ... repeat for all tables

# Delete S3 buckets
aws s3 rb s3://smart-vendors-static-dev --force
aws s3 rb s3://smart-vendors-images-dev --force

# Delete API Gateway
aws apigatewayv2 delete-api --api-id $API_ID

# Delete IAM role
aws iam delete-role --role-name smart-vendors-lambda-role
```
