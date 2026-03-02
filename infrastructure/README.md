# Smart Vendors Infrastructure

This directory contains the Infrastructure-as-Code (IaC) configuration for deploying Smart Vendors to AWS using Terraform.

## Architecture Overview

The infrastructure includes:

- **Amazon S3**: Three buckets for images, static assets (frontend), and ML models
- **Amazon DynamoDB**: Four tables for vendors, transactions, market prices, and marketplace listings
- **AWS Lambda**: Serverless compute with execution role and policies
- **Amazon CloudFront**: CDN for frontend hosting
- **Amazon API Gateway**: HTTP API for Lambda function routing
- **IAM Roles**: Lambda execution role with permissions for Bedrock, S3, DynamoDB, SageMaker, Transcribe, and SNS

## Prerequisites

1. **AWS Account**: Active AWS account with appropriate permissions
2. **AWS CLI**: Installed and configured with credentials
3. **Terraform**: Version 1.0 or higher
4. **Python 3.11**: For Lambda functions
5. **Node.js 18**: For frontend build

## Quick Start

### 1. Configure AWS Credentials

```bash
aws configure
```

Enter your AWS Access Key ID, Secret Access Key, and preferred region (ap-south-1 recommended).

### 2. Initialize Terraform

```bash
cd infrastructure/terraform
terraform init
```

### 3. Create Lambda Layer

```bash
# From project root
mkdir -p python
pip install boto3 -t python/
zip -r lambda_layer.zip python/
mv lambda_layer.zip infrastructure/
```

### 4. Configure Variables

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values
```

### 5. Plan Infrastructure

```bash
terraform plan
```

Review the planned changes to ensure everything looks correct.

### 6. Deploy Infrastructure

```bash
terraform apply
```

Type `yes` when prompted to confirm deployment.

### 7. Get Outputs

```bash
terraform output
```

Save these outputs - you'll need them for configuring the backend and frontend.

## Infrastructure Components

### S3 Buckets

- **Images Bucket**: Stores produce images for freshness classification
- **Static Assets Bucket**: Hosts the React frontend (served via CloudFront)
- **ML Models Bucket**: Stores SageMaker model artifacts

### DynamoDB Tables

- **Vendors**: Stores vendor profiles with phone_number GSI
- **Transactions**: Stores transaction records with vendor_id GSI
- **Market Prices**: Stores market price data with TTL (24 hours)
- **Marketplace Listings**: Stores B-Grade produce listings with vendor_id GSI

### IAM Permissions

The Lambda execution role has permissions for:
- CloudWatch Logs (logging)
- S3 (read/write to all three buckets)
- DynamoDB (full access to all tables)
- AWS Transcribe (voice-to-text)
- Amazon Bedrock (AI/ML inference)
- Amazon SageMaker (ML model inference)
- Amazon SNS (notifications)

### CloudFront Distribution

- Serves frontend from S3 static assets bucket
- HTTPS redirect enabled
- Custom error response for SPA routing (404 → index.html)
- Compression enabled

### API Gateway

- HTTP API (lower latency than REST API)
- CORS enabled for frontend access
- Auto-deploy enabled for rapid iteration

## Environment Variables

After deployment, configure your backend with these environment variables:

```bash
export AWS_REGION=ap-south-1
export S3_BUCKET_IMAGES=<from terraform output>
export S3_BUCKET_STATIC=<from terraform output>
export S3_BUCKET_ML_MODELS=<from terraform output>
export DYNAMODB_TABLE_VENDORS=<from terraform output>
export DYNAMODB_TABLE_TRANSACTIONS=<from terraform output>
export DYNAMODB_TABLE_MARKET_PRICES=<from terraform output>
export DYNAMODB_TABLE_MARKETPLACE_LISTINGS=<from terraform output>
export LAMBDA_EXECUTION_ROLE_ARN=<from terraform output>
export API_GATEWAY_ENDPOINT=<from terraform output>
```

## CI/CD with GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that:

1. Runs linting and tests on pull requests
2. Deploys infrastructure on push to main
3. Packages and deploys Lambda functions
4. Builds and deploys frontend to S3/CloudFront
5. Seeds demo data to DynamoDB

### Required GitHub Secrets

Add these secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

## Cost Estimation

With the hackathon demo workload (minimal traffic):

- **DynamoDB**: Pay-per-request pricing (~$0.25/month)
- **S3**: Storage + requests (~$1-2/month)
- **Lambda**: Free tier covers demo usage
- **CloudFront**: Free tier covers demo usage
- **API Gateway**: Free tier covers demo usage
- **Transcribe/Bedrock/SageMaker**: Pay-per-use (~$5-10 for demo)

**Estimated Total**: $5-15/month for demo/hackathon period

## Cleanup

To destroy all infrastructure and avoid charges:

```bash
cd infrastructure/terraform
terraform destroy
```

Type `yes` when prompted. This will delete all resources except S3 buckets with content (you'll need to empty them first).

## Troubleshooting

### Terraform State Lock

If Terraform gets stuck with a state lock:

```bash
terraform force-unlock <LOCK_ID>
```

### Lambda Layer Too Large

If the Lambda layer exceeds 50MB:

```bash
# Use slim dependencies
pip install --no-deps boto3 -t python/
```

### CloudFront Cache Issues

To invalidate CloudFront cache manually:

```bash
aws cloudfront create-invalidation \
  --distribution-id <DISTRIBUTION_ID> \
  --paths "/*"
```

### DynamoDB Throttling

If you see throttling errors, switch to provisioned capacity:

```hcl
billing_mode = "PROVISIONED"
read_capacity = 5
write_capacity = 5
```

## Security Best Practices

1. **Never commit AWS credentials** - Use environment variables or AWS CLI profiles
2. **Enable MFA** on your AWS account
3. **Use least privilege** - The Lambda role has broad permissions for demo purposes; restrict in production
4. **Enable CloudTrail** for audit logging
5. **Use S3 bucket versioning** for important data
6. **Enable DynamoDB point-in-time recovery** for production

## Next Steps

After infrastructure deployment:

1. Deploy Lambda functions (Task 2)
2. Build and deploy frontend (Task 6)
3. Seed demo data (Task 2.3)
4. Test end-to-end functionality
5. Configure custom domain (optional)

## Support

For issues or questions:
- Check Terraform documentation: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- AWS documentation: https://docs.aws.amazon.com/
- Project repository: [Add your GitHub URL]
