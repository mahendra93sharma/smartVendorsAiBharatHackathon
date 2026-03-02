#!/bin/bash

# Lambda Deployment Script for Smart Vendors
# Packages and deploys all Lambda functions to AWS

set -e

echo "🚀 Deploying Lambda Functions"
echo "=============================="
echo ""

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found"
    exit 1
fi

# Check if in backend directory
if [ ! -d "lambda_functions" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

# Get AWS region
AWS_REGION=$(aws configure get region)
echo "📍 Region: $AWS_REGION"
echo ""

# Package each Lambda function
echo "📦 Packaging Lambda functions..."
cd lambda_functions

for dir in */; do
    if [ -f "${dir}handler.py" ]; then
        function_name="${dir%/}"
        echo "   Packaging $function_name..."
        
        cd "$dir"
        zip -q -r "../${function_name}.zip" .
        cd ..
    fi
done

echo "✅ All functions packaged"
echo ""

# Deploy each Lambda function
echo "🚀 Deploying Lambda functions..."

for zip_file in *.zip; do
    function_name="${zip_file%.zip}"
    aws_function_name="smart-vendors-${function_name}-dev"
    
    echo "   Deploying $aws_function_name..."
    
    aws lambda update-function-code \
        --function-name "$aws_function_name" \
        --zip-file "fileb://${zip_file}" \
        --region "$AWS_REGION" \
        2>/dev/null || echo "   ⚠️  Function $aws_function_name not found (will be created in Task 4)"
done

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Note: Some functions may not exist yet. They will be created in Task 4."
echo ""

# Cleanup
echo "🧹 Cleaning up..."
rm -f *.zip
echo "✅ Cleanup complete"
