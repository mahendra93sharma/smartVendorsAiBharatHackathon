#!/bin/bash

# One-Command HTTPS Deployment
# Fixes microphone permission issue

echo "🚀 Deploying Smart Vendors with HTTPS..."
echo ""
echo "This will fix the microphone permission error by deploying to Netlify with HTTPS."
echo ""

cd frontend

# Check if dist exists
if [ ! -d "dist" ]; then
    echo "📦 Building frontend..."
    npm run build
fi

echo ""
echo "🌐 Deploying to Netlify..."
echo ""
echo "Follow the prompts:"
echo "  1. Choose: Create & configure a new site"
echo "  2. Site name: smart-vendors (or leave blank)"
echo "  3. Authorize in browser when prompted"
echo ""

netlify deploy --prod --dir=dist

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🎤 Test your microphone at the HTTPS URL above!"
