#!/bin/bash

# Setup CloudFront with HTTPS for S3 Static Website
# This fixes the microphone permission issue using AWS CloudFront

set -e

echo "🚀 Setting up CloudFront with HTTPS for Smart Vendors..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
S3_BUCKET="smart-vendors-frontend-1772474994"
S3_WEBSITE_ENDPOINT="${S3_BUCKET}.s3-website.ap-south-1.amazonaws.com"
REGION="ap-south-1"

echo -e "${BLUE}📋 Configuration:${NC}"
echo "  S3 Bucket: $S3_BUCKET"
echo "  S3 Website: http://$S3_WEBSITE_ENDPOINT"
echo "  Region: $REGION"
echo ""

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not configured${NC}"
    echo "Run: aws configure"
    exit 1
fi

echo -e "${BLUE}📦 Creating CloudFront distribution...${NC}"
echo ""

# Create CloudFront distribution configuration
cat > /tmp/cloudfront-config.json <<EOF
{
  "CallerReference": "smart-vendors-$(date +%s)",
  "Comment": "Smart Vendors Frontend with HTTPS",
  "Enabled": true,
  "DefaultRootObject": "index.html",
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-Website-${S3_BUCKET}",
        "DomainName": "${S3_WEBSITE_ENDPOINT}",
        "CustomOriginConfig": {
          "HTTPPort": 80,
          "HTTPSPort": 443,
          "OriginProtocolPolicy": "http-only",
          "OriginSslProtocols": {
            "Quantity": 1,
            "Items": ["TLSv1.2"]
          }
        }
      }
    ]
  },
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-Website-${S3_BUCKET}",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"],
      "CachedMethods": {
        "Quantity": 2,
        "Items": ["GET", "HEAD"]
      }
    },
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": {
        "Forward": "none"
      }
    },
    "MinTTL": 0,
    "DefaultTTL": 86400,
    "MaxTTL": 31536000,
    "Compress": true
  },
  "CustomErrorResponses": {
    "Quantity": 2,
    "Items": [
      {
        "ErrorCode": 403,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200",
        "ErrorCachingMinTTL": 300
      },
      {
        "ErrorCode": 404,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200",
        "ErrorCachingMinTTL": 300
      }
    ]
  },
  "PriceClass": "PriceClass_100",
  "ViewerCertificate": {
    "CloudFrontDefaultCertificate": true,
    "MinimumProtocolVersion": "TLSv1.2_2021"
  }
}
EOF

# Create CloudFront distribution
echo "Creating distribution (this takes 15-20 minutes)..."
DISTRIBUTION_OUTPUT=$(aws cloudfront create-distribution \
  --distribution-config file:///tmp/cloudfront-config.json \
  --region us-east-1 \
  --output json)

# Extract distribution ID and domain
DISTRIBUTION_ID=$(echo $DISTRIBUTION_OUTPUT | jq -r '.Distribution.Id')
CLOUDFRONT_DOMAIN=$(echo $DISTRIBUTION_OUTPUT | jq -r '.Distribution.DomainName')

echo ""
echo -e "${GREEN}✅ CloudFront Distribution Created!${NC}"
echo ""
echo -e "${BLUE}📊 Distribution Details:${NC}"
echo "  Distribution ID: $DISTRIBUTION_ID"
echo "  CloudFront Domain: $CLOUDFRONT_DOMAIN"
echo "  HTTPS URL: https://$CLOUDFRONT_DOMAIN"
echo ""
echo -e "${YELLOW}⏳ Status: Deploying (15-20 minutes)${NC}"
echo ""
echo "Your distribution is being deployed to CloudFront edge locations worldwide."
echo "This process takes 15-20 minutes to complete."
echo ""

# Save distribution info
cat > cloudfront-distribution.txt <<EOF
CloudFront Distribution Information
====================================

Distribution ID: $DISTRIBUTION_ID
CloudFront Domain: $CLOUDFRONT_DOMAIN
HTTPS URL: https://$CLOUDFRONT_DOMAIN

Status: Deploying (check status below)

Check Status:
  aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'Distribution.Status'

Wait for Deployment:
  aws cloudfront wait distribution-deployed --id $DISTRIBUTION_ID

Open in Browser:
  open https://$CLOUDFRONT_DOMAIN

Update Frontend:
  After deployment completes, test the microphone feature at:
  https://$CLOUDFRONT_DOMAIN

Invalidate Cache (after updates):
  aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"

Delete Distribution (cleanup):
  aws cloudfront delete-distribution --id $DISTRIBUTION_ID --if-match \$(aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'ETag' --output text)
EOF

echo -e "${GREEN}✅ Distribution info saved to: cloudfront-distribution.txt${NC}"
echo ""

# Check deployment status
echo -e "${BLUE}📊 Checking deployment status...${NC}"
STATUS=$(aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'Distribution.Status' --output text)
echo "  Current Status: $STATUS"
echo ""

if [ "$STATUS" == "InProgress" ]; then
    echo -e "${YELLOW}⏳ Distribution is deploying...${NC}"
    echo ""
    echo "Options:"
    echo "  1. Wait here (15-20 minutes):"
    echo "     aws cloudfront wait distribution-deployed --id $DISTRIBUTION_ID"
    echo ""
    echo "  2. Check status later:"
    echo "     aws cloudfront get-distribution --id $DISTRIBUTION_ID --query 'Distribution.Status'"
    echo ""
    echo "  3. Continue working and check back later"
    echo ""
    
    read -p "Wait for deployment to complete? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Waiting for deployment..."
        aws cloudfront wait distribution-deployed --id $DISTRIBUTION_ID
        echo ""
        echo -e "${GREEN}✅ Deployment Complete!${NC}"
        echo ""
        echo "Your HTTPS URL: https://$CLOUDFRONT_DOMAIN"
        echo ""
        echo "Test the microphone feature now!"
    fi
fi

echo ""
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo "Next Steps:"
echo "  1. Wait for deployment to complete (15-20 minutes)"
echo "  2. Open: https://$CLOUDFRONT_DOMAIN"
echo "  3. Test microphone feature"
echo "  4. Update submission with HTTPS URL"
echo ""
echo "Your microphone permission issue will be fixed once deployment completes!"

# Cleanup
rm /tmp/cloudfront-config.json
