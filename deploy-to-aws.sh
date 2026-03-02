#!/bin/bash

# Smart Vendors - Full AWS Deployment Script
# Deploys both frontend and backend to AWS

set -e

echo "🚀 Smart Vendors - Full AWS Deployment"
echo "======================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get AWS info
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "us-east-1")

echo -e "${BLUE}AWS Account: ${AWS_ACCOUNT_ID}${NC}"
echo -e "${BLUE}AWS Region: ${AWS_REGION}${NC}"
echo ""

# Generate unique suffix
SUFFIX=$(date +%s)
PROJECT_NAME="smart-vendors"

# Resource names
S3_FRONTEND_BUCKET="${PROJECT_NAME}-frontend-${SUFFIX}"
S3_IMAGES_BUCKET="${PROJECT_NAME}-images-${SUFFIX}"
DYNAMODB_PREFIX="${PROJECT_NAME}"

echo "📋 Deployment Plan:"
echo "-------------------"
echo "Frontend Bucket: ${S3_FRONTEND_BUCKET}"
echo "Images Bucket: ${S3_IMAGES_BUCKET}"
echo "DynamoDB Prefix: ${DYNAMODB_PREFIX}"
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 1
fi

echo ""
echo "🗄️  Step 1: Creating S3 Buckets"
echo "--------------------------------"

# Create frontend bucket
echo "Creating frontend bucket..."
aws s3 mb s3://${S3_FRONTEND_BUCKET} --region ${AWS_REGION}
echo -e "${GREEN}✅ Frontend bucket created${NC}"

# Create images bucket
echo "Creating images bucket..."
aws s3 mb s3://${S3_IMAGES_BUCKET} --region ${AWS_REGION}
echo -e "${GREEN}✅ Images bucket created${NC}"

# Configure frontend bucket for website hosting
echo "Configuring website hosting..."
aws s3 website s3://${S3_FRONTEND_BUCKET}/ \
  --index-document index.html \
  --error-document index.html

# Set bucket policy for public read
cat > /tmp/bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::${S3_FRONTEND_BUCKET}/*"
  }]
}
EOF

aws s3api put-bucket-policy \
  --bucket ${S3_FRONTEND_BUCKET} \
  --policy file:///tmp/bucket-policy.json

echo -e "${GREEN}✅ Website hosting configured${NC}"
echo ""

echo "📊 Step 2: Creating DynamoDB Tables"
echo "------------------------------------"

# Create Vendors table
echo "Creating Vendors table..."
aws dynamodb create-table \
  --table-name ${DYNAMODB_PREFIX}-vendors \
  --attribute-definitions AttributeName=vendor_id,AttributeType=S \
  --key-schema AttributeName=vendor_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ${AWS_REGION} \
  --no-cli-pager || echo "Table may already exist"

echo -e "${GREEN}✅ Vendors table created${NC}"

# Create Transactions table
echo "Creating Transactions table..."
aws dynamodb create-table \
  --table-name ${DYNAMODB_PREFIX}-transactions \
  --attribute-definitions \
    AttributeName=transaction_id,AttributeType=S \
    AttributeName=vendor_id,AttributeType=S \
  --key-schema AttributeName=transaction_id,KeyType=HASH \
  --global-secondary-indexes \
    "IndexName=vendor_id-index,KeySchema=[{AttributeName=vendor_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
  --billing-mode PAY_PER_REQUEST \
  --region ${AWS_REGION} \
  --no-cli-pager || echo "Table may already exist"

echo -e "${GREEN}✅ Transactions table created${NC}"

# Create Market Prices table
echo "Creating Market Prices table..."
aws dynamodb create-table \
  --table-name ${DYNAMODB_PREFIX}-market-prices \
  --attribute-definitions \
    AttributeName=item_name,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=item_name,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region ${AWS_REGION} \
  --no-cli-pager || echo "Table may already exist"

echo -e "${GREEN}✅ Market Prices table created${NC}"

# Create Marketplace Listings table
echo "Creating Marketplace Listings table..."
aws dynamodb create-table \
  --table-name ${DYNAMODB_PREFIX}-marketplace-listings \
  --attribute-definitions \
    AttributeName=listing_id,AttributeType=S \
    AttributeName=vendor_id,AttributeType=S \
  --key-schema AttributeName=listing_id,KeyType=HASH \
  --global-secondary-indexes \
    "IndexName=vendor_id-index,KeySchema=[{AttributeName=vendor_id,KeyType=HASH}],Projection={ProjectionType=ALL}" \
  --billing-mode PAY_PER_REQUEST \
  --region ${AWS_REGION} \
  --no-cli-pager || echo "Table may already exist"

echo -e "${GREEN}✅ Marketplace Listings table created${NC}"

echo ""
echo "⏳ Waiting for tables to be active (30 seconds)..."
sleep 30

echo ""
echo "🌐 Step 3: Building and Deploying Frontend"
echo "-------------------------------------------"

cd frontend

# Build frontend
echo "Building frontend..."
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Frontend built successfully${NC}"
else
    echo -e "${RED}❌ Frontend build failed${NC}"
    exit 1
fi

# Upload to S3
echo "Uploading to S3..."
aws s3 sync dist/ s3://${S3_FRONTEND_BUCKET}/ --delete

echo -e "${GREEN}✅ Frontend deployed to S3${NC}"

cd ..

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo -e "${GREEN}Frontend URL:${NC}"
echo "http://${S3_FRONTEND_BUCKET}.s3-website-${AWS_REGION}.amazonaws.com"
echo ""
echo -e "${BLUE}Resources Created:${NC}"
echo "- S3 Bucket (Frontend): ${S3_FRONTEND_BUCKET}"
echo "- S3 Bucket (Images): ${S3_IMAGES_BUCKET}"
echo "- DynamoDB Table: ${DYNAMODB_PREFIX}-vendors"
echo "- DynamoDB Table: ${DYNAMODB_PREFIX}-transactions"
echo "- DynamoDB Table: ${DYNAMODB_PREFIX}-market-prices"
echo "- DynamoDB Table: ${DYNAMODB_PREFIX}-marketplace-listings"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. Test your frontend URL above"
echo "2. Optionally deploy Lambda functions (see backend/deploy_lambda.sh)"
echo "3. Optionally seed demo data (python backend/seed_data.py)"
echo "4. Add URL to SUBMISSION_CHECKLIST.md"
echo ""
echo -e "${YELLOW}💰 Cost Estimate:${NC}"
echo "- S3: ~\$0.50/month"
echo "- DynamoDB: Free tier (25GB)"
echo "- Total: ~\$0.50-1/month"
echo ""
echo -e "${GREEN}🎯 Your prototype is now live on AWS!${NC}"
echo ""

# Save deployment info
cat > deployment-info.txt << EOF
Smart Vendors - AWS Deployment Info
====================================

Deployment Date: $(date)
AWS Account: ${AWS_ACCOUNT_ID}
AWS Region: ${AWS_REGION}

Frontend URL:
http://${S3_FRONTEND_BUCKET}.s3-website-${AWS_REGION}.amazonaws.com

Resources:
- Frontend Bucket: ${S3_FRONTEND_BUCKET}
- Images Bucket: ${S3_IMAGES_BUCKET}
- DynamoDB Prefix: ${DYNAMODB_PREFIX}

DynamoDB Tables:
- ${DYNAMODB_PREFIX}-vendors
- ${DYNAMODB_PREFIX}-transactions
- ${DYNAMODB_PREFIX}-market-prices
- ${DYNAMODB_PREFIX}-marketplace-listings

To update frontend:
cd frontend && npm run build && aws s3 sync dist/ s3://${S3_FRONTEND_BUCKET}/ --delete

To delete resources:
aws s3 rb s3://${S3_FRONTEND_BUCKET} --force
aws s3 rb s3://${S3_IMAGES_BUCKET} --force
aws dynamodb delete-table --table-name ${DYNAMODB_PREFIX}-vendors
aws dynamodb delete-table --table-name ${DYNAMODB_PREFIX}-transactions
aws dynamodb delete-table --table-name ${DYNAMODB_PREFIX}-market-prices
aws dynamodb delete-table --table-name ${DYNAMODB_PREFIX}-marketplace-listings
EOF

echo "Deployment info saved to: deployment-info.txt"
echo ""
