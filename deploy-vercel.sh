#!/bin/bash

# Smart Vendors - Vercel Deployment Script
# Deploys frontend to Vercel for instant prototype URL

set -e

echo "🚀 Smart Vendors - Vercel Deployment"
echo "====================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
    echo -e "${GREEN}✅ Vercel CLI installed${NC}"
fi

echo ""
echo "📋 Pre-deployment checklist:"
echo "----------------------------"

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ frontend directory not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Frontend directory found${NC}"

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Installing dependencies...${NC}"
    cd frontend
    npm install
    cd ..
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Dependencies already installed${NC}"
fi

# Test build
echo ""
echo -e "${YELLOW}🔨 Testing build...${NC}"
cd frontend
npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful${NC}"
else
    echo -e "${RED}❌ Build failed. Please fix errors first.${NC}"
    exit 1
fi
cd ..

echo ""
echo "🌐 Deploying to Vercel..."
echo "-------------------------"
echo ""
echo -e "${YELLOW}Note: You'll need to login to Vercel (browser will open)${NC}"
echo ""

# Deploy to Vercel
cd frontend
vercel --prod

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "1. Copy the deployment URL from above"
echo "2. Test your prototype at the URL"
echo "3. Add URL to SUBMISSION_CHECKLIST.md"
echo "4. Share with your team!"
echo ""
echo "🎉 Your Smart Vendors prototype is now live!"
