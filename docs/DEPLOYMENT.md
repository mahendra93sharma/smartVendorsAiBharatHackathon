# Deployment Guide

Complete guide for deploying Smart Vendors to AWS.

## Prerequisites

- AWS Account with admin access
- AWS CLI configured
- Terraform 1.0+
- Python 3.11+
- Node.js 18+
- Git

## Step-by-Step Deployment

### 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-vendors.git
cd smart-vendors
```

### 2. Configure AWS Credentials

```bash
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `ap-south-1`
- Default output format: `json`

### 3. Deploy Infrastructure

```bash
cd infrastructure
chmod +x setup.sh
./setup.sh
```

This creates:
- 3 S3 buckets (images, static assets, ML models)
- 4 DynamoDB tables (vendors, transactions, prices, listings)
- Lambda execution role with policies
- CloudFront distribution
- API Gateway

**Expected time**: 5-10 minutes

### 4. Save Environment Variables

```bash
source outputs.env
```

Or manually copy values from Terraform outputs to `.env` file.

### 5. Deploy Backend Lambda Functions

```bash
cd ../backend
pip install -r requirements.txt
chmod +x deploy_lambda.sh
./deploy_lambda.sh
```

This script will:
1. Create Lambda deployment packages with dependencies
2. Upload packages to S3
3. Create or update Lambda functions
4. Configure environment variables
5. Set up Lambda layers for shared code

**Lambda Functions Created**:
- `smart-vendors-voice-transcribe-dev`
- `smart-vendors-create-transaction-dev`
- `smart-vendors-get-transactions-dev`
- `smart-vendors-get-market-prices-dev`
- `smart-vendors-classify-freshness-dev`
- `smart-vendors-create-marketplace-listing-dev`
- `smart-vendors-get-marketplace-buyers-dev`
- `smart-vendors-notify-marketplace-buyers-dev`
- `smart-vendors-get-trust-score-dev`

**Expected time**: 3-5 minutes

**Verify Lambda Deployment**:
```bash
# List all Lambda functions
aws lambda list-functions --query 'Functions[?starts_with(FunctionName, `smart-vendors`)].FunctionName'

# Test a Lambda function
aws lambda invoke \
  --function-name smart-vendors-get-market-prices-dev \
  --payload '{"pathParameters": {"item": "tomatoes"}}' \
  response.json

cat response.json
```

### 6. Build and Deploy Frontend

```bash
cd ../frontend
npm install
npm run build

# Deploy to S3
aws s3 sync dist/ s3://smart-vendors-static-dev/ --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id $(aws cloudfront list-distributions --query "DistributionList.Items[?Comment=='Smart Vendors Frontend Distribution'].Id" --output text) \
  --paths "/*"
```

### 7. Seed Demo Data

```bash
cd ../backend/scripts
python seed_data.py
```

This creates:
- 5 demo vendor accounts
- 20 sample transactions
- 10 market prices
- 5 marketplace listings

### 8. Verify Deployment

```bash
# Get CloudFront URL
cd ../../infrastructure/terraform
terraform output cloudfront_domain_name
```

Open the URL in your browser. You should see the Smart Vendors landing page.

**Demo Credentials:**
- Username: `demo_vendor`
- Password: `hackathon2024`

## CI/CD with GitHub Actions

### Setup GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### Automatic Deployment

Push to `main` branch triggers:
1. Linting and tests
2. Infrastructure deployment
3. Lambda function deployment
4. Frontend build and deployment
5. Demo data seeding

## Monitoring

### CloudWatch Logs

View Lambda logs:

```bash
aws logs tail /aws/lambda/smart-vendors-voice-transcribe-dev --follow
```

### API Gateway Metrics

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiId,Value=<API_ID> \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

### DynamoDB Metrics

Check table metrics in AWS Console:
- Read/Write capacity units
- Throttled requests
- Item count

## Troubleshooting

### Infrastructure Deployment Fails

**Issue**: Terraform apply fails with permission errors

**Solution**: Ensure your AWS user has admin permissions or these specific permissions:
- S3: Full access
- DynamoDB: Full access
- Lambda: Full access
- IAM: Create roles and policies
- CloudFront: Full access
- API Gateway: Full access

**Issue**: Terraform state lock error

**Solution**: 
```bash
# Remove state lock (only if you're sure no other process is running)
cd infrastructure/terraform
terraform force-unlock <LOCK_ID>
```

### Lambda Deployment Issues

**Issue**: Lambda function deployment fails with "InvalidParameterValueException"

**Solution**: 
1. Check Python version: `python --version` (must be 3.11)
2. Verify dependencies are compatible with Lambda runtime
3. Check deployment package size (max 50 MB zipped, 250 MB unzipped)

**Issue**: Lambda function timeout

**Solution**:
```bash
# Increase timeout to 60 seconds
aws lambda update-function-configuration \
  --function-name smart-vendors-voice-transcribe-dev \
  --timeout 60
```

**Issue**: Lambda layer not found

**Solution**:
```bash
# Create Lambda layer manually
cd backend
mkdir -p layer/python
pip install -r layer_requirements.txt -t layer/python/
cd layer
zip -r ../layer.zip .
cd ..

# Upload layer
aws lambda publish-layer-version \
  --layer-name smart-vendors-shared-layer \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.11
```

### Lambda Function Not Found

**Issue**: `deploy_lambda.sh` shows "function not found"

**Solution**: This is expected for initial deployment. The script creates functions if they don't exist. If error persists:
```bash
# Check if function exists
aws lambda get-function --function-name smart-vendors-voice-transcribe-dev

# If not, create manually
aws lambda create-function \
  --function-name smart-vendors-voice-transcribe-dev \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/smart-vendors-lambda-role \
  --handler voice_transcribe.lambda_handler \
  --zip-file fileb://deployment.zip
```

### CloudFront Distribution Not Working

**Issue**: CloudFront URL returns 403 Forbidden

**Solution**: 
1. Check S3 bucket policy allows CloudFront OAI
2. Verify files are uploaded to S3
3. Wait 5-10 minutes for CloudFront distribution to deploy

### Frontend Can't Connect to API

**Issue**: API calls fail with CORS errors

**Solution**:
1. Verify API Gateway CORS is configured
2. Check `VITE_API_BASE_URL` in frontend `.env`
3. Ensure API Gateway is deployed to correct stage

### DynamoDB Access Denied

**Issue**: Lambda functions can't access DynamoDB

**Solution**:
1. Check Lambda execution role has DynamoDB permissions
2. Verify table names in environment variables match Terraform outputs
3. Check table ARNs in IAM policy

### Bedrock Access Denied

**Issue**: Bedrock API calls fail

**Solution**:
1. Enable Bedrock in your AWS account (Console → Bedrock → Model access)
2. Request access to Claude or Titan models
3. Wait for approval (usually instant)

### SageMaker Endpoint Not Found

**Issue**: Freshness classification fails

**Solution**:
1. Deploy SageMaker endpoint (see `docs/SAGEMAKER_ENDPOINT_SETUP.md`)
2. Update `SAGEMAKER_ENDPOINT_NAME` environment variable
3. Ensure Lambda role has `sagemaker:InvokeEndpoint` permission

**Alternative**: Use fallback mode (rule-based classification):
```bash
# Set environment variable to enable fallback
aws lambda update-function-configuration \
  --function-name smart-vendors-classify-freshness-dev \
  --environment Variables={USE_SAGEMAKER_FALLBACK=true}
```

### API Gateway Configuration Issues

**Issue**: API Gateway returns 403 Forbidden

**Solution**:
1. Check API Gateway resource policy
2. Verify Lambda integration is configured
3. Deploy API to correct stage:
```bash
aws apigatewayv2 create-deployment \
  --api-id <API_ID> \
  --stage-name prod
```

**Issue**: API Gateway CORS errors

**Solution**:
```bash
# Update CORS configuration
aws apigatewayv2 update-api \
  --api-id <API_ID> \
  --cors-configuration AllowOrigins="*",AllowMethods="GET,POST,OPTIONS",AllowHeaders="Content-Type,X-Api-Key"
```

### Data Seeding Issues

**Issue**: Seed script fails with "Table not found"

**Solution**:
1. Verify DynamoDB tables exist:
```bash
aws dynamodb list-tables | grep smart-vendors
```
2. Check table names in `backend/seed_data.py` match Terraform outputs
3. Ensure AWS credentials have DynamoDB write permissions

**Issue**: Seed script creates duplicate data

**Solution**:
```bash
# Clear existing data before seeding
cd backend
python -c "
from shared.aws.dynamodb_client import DynamoDBClient
client = DynamoDBClient()
# Delete all items (implement clear_table method)
"
python seed_data.py
```

## Cost Optimization

### Development Environment

- Use DynamoDB on-demand pricing
- Delete CloudFront distribution when not testing
- Stop SageMaker endpoints when not in use
- Use Lambda free tier (1M requests/month)

### Production Environment

- Switch DynamoDB to provisioned capacity
- Enable S3 Intelligent-Tiering
- Use CloudFront reserved capacity
- Implement API Gateway caching

## Cleanup

To destroy all infrastructure:

```bash
cd infrastructure
chmod +x cleanup.sh
./cleanup.sh
```

This will:
1. Empty all S3 buckets
2. Destroy all Terraform resources
3. Clean up local files

**Warning**: This is irreversible. All data will be lost.

## Security Checklist

- [ ] AWS credentials not committed to Git
- [ ] S3 buckets have appropriate access policies
- [ ] Lambda functions use least privilege IAM roles
- [ ] API Gateway has rate limiting enabled
- [ ] CloudFront uses HTTPS only
- [ ] DynamoDB tables have encryption at rest
- [ ] CloudWatch logging enabled for all services

## Next Steps

After successful deployment:

1. Test all features with demo account
2. Create demo video (Task 10)
3. Write project summary (Task 11)
4. Verify submission checklist (Task 14)
5. Submit to hackathon

## Support

For deployment issues:
- Check AWS CloudWatch logs
- Review Terraform state: `terraform show`
- Verify AWS service quotas
- Contact team: your-email@example.com
