#!/bin/bash

# Deploy Frontend to Netlify with HTTPS
# This fixes the microphone permission issue

set -e

echo "🚀 Deploying Smart Vendors Frontend to Netlify with HTTPS..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to frontend directory
cd frontend

# Check if dist folder exists
if [ ! -d "dist" ]; then
    echo -e "${YELLOW}⚠️  Build folder not found. Building frontend...${NC}"
    npm run build
fi

echo ""
echo -e "${BLUE}📦 Deploying to Netlify...${NC}"
echo ""
echo "This will:"
echo "  ✅ Deploy your frontend with HTTPS"
echo "  ✅ Fix microphone permission issues"
echo "  ✅ Provide a custom domain (*.netlify.app)"
echo ""

# Deploy to Netlify
netlify deploy --prod --dir=dist

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo "Your frontend is now live with HTTPS! 🎉"
echo ""
echo "Next steps:"
echo "  1. Copy the HTTPS URL from above"
echo "  2. Test the microphone feature"
echo "  3. Update your submission with the new URL"
echo ""
echo "The microphone permission issue should now be fixed!"
