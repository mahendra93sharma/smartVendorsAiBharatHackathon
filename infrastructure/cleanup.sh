#!/bin/bash

# Smart Vendors Infrastructure Cleanup Script
# This script destroys all AWS infrastructure to avoid charges

set -e

echo "🧹 Smart Vendors Infrastructure Cleanup"
echo "========================================"
echo ""
echo "⚠️  WARNING: This will destroy all infrastructure and data!"
echo ""

# Ask for confirmation
read -p "Are you sure you want to destroy all infrastructure? (type 'yes' to confirm): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cleanup cancelled"
    exit 0
fi

cd "$(dirname "$0")/terraform"

# Get bucket names before destroying
echo ""
echo "📦 Emptying S3 buckets..."

IMAGES_BUCKET=$(terraform output -raw s3_bucket_images 2>/dev/null || echo "")
STATIC_BUCKET=$(terraform output -raw s3_bucket_static_assets 2>/dev/null || echo "")
ML_MODELS_BUCKET=$(terraform output -raw s3_bucket_ml_models 2>/dev/null || echo "")

if [ -n "$IMAGES_BUCKET" ]; then
    echo "   Emptying $IMAGES_BUCKET..."
    aws s3 rm s3://$IMAGES_BUCKET --recursive || true
fi

if [ -n "$STATIC_BUCKET" ]; then
    echo "   Emptying $STATIC_BUCKET..."
    aws s3 rm s3://$STATIC_BUCKET --recursive || true
fi

if [ -n "$ML_MODELS_BUCKET" ]; then
    echo "   Emptying $ML_MODELS_BUCKET..."
    aws s3 rm s3://$ML_MODELS_BUCKET --recursive || true
fi

echo "✅ S3 buckets emptied"

# Destroy infrastructure
echo ""
echo "🔥 Destroying infrastructure..."
terraform destroy -auto-approve

# Clean up local files
echo ""
echo "🧹 Cleaning up local files..."
cd ..
rm -f lambda_layer.zip
rm -f outputs.env
rm -rf python/

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "All AWS resources have been destroyed."
echo "You will no longer be charged for these resources."
echo ""
