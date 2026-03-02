#!/bin/bash

# Smart Vendors - One-Click Deployment
# Run this script to deploy to Vercel

echo "🚀 Smart Vendors - Deployment Script"
echo "====================================="
echo ""

# Navigate to frontend
cd "$(dirname "$0")/frontend" || exit 1

echo "📍 Current directory: $(pwd)"
echo ""

# Check if Vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found"
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ Vercel CLI installed: $(vercel --version)"
echo ""

echo "🌐 Starting deployment..."
echo ""
echo "📝 You'll need to:"
echo "   1. Login to Vercel (browser will open)"
echo "   2. Answer a few setup questions"
echo "   3. Wait 2-3 minutes for deployment"
echo ""
echo "Press Enter to continue..."
read

# Deploy
vercel --prod

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Copy your prototype URL from above"
echo "   2. Test the URL in your browser"
echo "   3. Add URL to SUBMISSION_CHECKLIST.md"
echo "   4. Create demo video"
echo "   5. Submit to hackathon!"
echo ""
