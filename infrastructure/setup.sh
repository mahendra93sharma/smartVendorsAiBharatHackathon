#!/bin/bash

# Smart Vendors Infrastructure Setup Script
# This script helps set up the AWS infrastructure for the Smart Vendors project

set -e

echo "🚀 Smart Vendors Infrastructure Setup"
echo "======================================"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi
echo "✅ AWS CLI found"

# Check Terraform
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Please install it first:"
    echo "   https://developer.hashicorp.com/terraform/downloads"
    exit 1
fi
echo "✅ Terraform found"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python 3 found"

# Check AWS credentials
echo ""
echo "🔐 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run 'aws configure' first."
    exit 1
fi
echo "✅ AWS credentials configured"

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
echo "   Account ID: $AWS_ACCOUNT_ID"
echo "   Region: $AWS_REGION"

# Create Lambda layer
echo ""
echo "📦 Creating Lambda layer..."
cd "$(dirname "$0")"
mkdir -p python
pip install boto3 -t python/ -q
zip -r lambda_layer.zip python/ > /dev/null
echo "✅ Lambda layer created"

# Initialize Terraform
echo ""
echo "🔧 Initializing Terraform..."
cd terraform
terraform init

# Create terraform.tfvars if it doesn't exist
if [ ! -f terraform.tfvars ]; then
    echo ""
    echo "📝 Creating terraform.tfvars..."
    cp terraform.tfvars.example terraform.tfvars
    echo "✅ terraform.tfvars created"
    echo "   You can edit this file to customize your deployment"
fi

# Plan infrastructure
echo ""
echo "📊 Planning infrastructure deployment..."
terraform plan -out=tfplan

# Ask for confirmation
echo ""
read -p "🤔 Do you want to deploy this infrastructure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Deployment cancelled"
    rm -f tfplan
    exit 0
fi

# Apply infrastructure
echo ""
echo "🚀 Deploying infrastructure..."
terraform apply tfplan
rm -f tfplan

# Get outputs
echo ""
echo "📤 Infrastructure deployed successfully!"
echo ""
echo "📋 Important outputs:"
echo "===================="
terraform output

# Save outputs to file
echo ""
echo "💾 Saving outputs to ../outputs.env..."
cat > ../outputs.env << EOF
# AWS Infrastructure Outputs
# Generated on $(date)

AWS_REGION=$AWS_REGION
S3_BUCKET_IMAGES=$(terraform output -raw s3_bucket_images)
S3_BUCKET_STATIC=$(terraform output -raw s3_bucket_static_assets)
S3_BUCKET_ML_MODELS=$(terraform output -raw s3_bucket_ml_models)
DYNAMODB_TABLE_VENDORS=$(terraform output -raw dynamodb_table_vendors)
DYNAMODB_TABLE_TRANSACTIONS=$(terraform output -raw dynamodb_table_transactions)
DYNAMODB_TABLE_MARKET_PRICES=$(terraform output -raw dynamodb_table_market_prices)
DYNAMODB_TABLE_MARKETPLACE_LISTINGS=$(terraform output -raw dynamodb_table_marketplace_listings)
LAMBDA_EXECUTION_ROLE_ARN=$(terraform output -raw lambda_execution_role_arn)
API_GATEWAY_ENDPOINT=$(terraform output -raw api_gateway_endpoint)
CLOUDFRONT_DOMAIN=$(terraform output -raw cloudfront_domain_name)
EOF

echo "✅ Outputs saved to ../outputs.env"
echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Source the environment variables: source ../outputs.env"
echo "2. Deploy Lambda functions (Task 2)"
echo "3. Build and deploy frontend (Task 6)"
echo "4. Seed demo data (Task 2.3)"
echo ""
echo "Frontend URL: https://$(terraform output -raw cloudfront_domain_name)"
echo "API Endpoint: $(terraform output -raw api_gateway_endpoint)"
echo ""
