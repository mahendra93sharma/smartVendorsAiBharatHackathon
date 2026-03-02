#!/bin/bash

# Smart Vendors - Local Development Setup Script
# This script sets up the local development environment using Docker

set -e

echo "🚀 Smart Vendors - Local Development Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first:${NC}"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first:${NC}"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose found${NC}"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running. Please start Docker.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker daemon is running${NC}"

echo ""
echo "🔧 Setup Options:"
echo "1. Full setup (DynamoDB Local + LocalStack + Backend + Frontend)"
echo "2. Minimal setup (DynamoDB Local only)"
echo "3. AWS deployment (deploy to real AWS infrastructure)"
echo ""
read -p "Choose option (1/2/3): " setup_option

case $setup_option in
    1)
        echo ""
        echo "🐳 Starting full local development environment..."
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}✅ All services started!${NC}"
        echo ""
        echo "📋 Service URLs:"
        echo "   Frontend:        http://localhost:3000"
        echo "   Backend API:     http://localhost:8080"
        echo "   DynamoDB Local:  http://localhost:8000"
        echo "   DynamoDB Admin:  http://localhost:8001"
        echo "   LocalStack:      http://localhost:4566"
        echo ""
        echo "🔍 View logs:"
        echo "   docker-compose logs -f"
        echo ""
        echo "🛑 Stop services:"
        echo "   docker-compose down"
        ;;
    
    2)
        echo ""
        echo "🐳 Starting DynamoDB Local only..."
        docker-compose up -d dynamodb-local dynamodb-admin
        
        echo ""
        echo -e "${GREEN}✅ DynamoDB Local started!${NC}"
        echo ""
        echo "📋 Service URLs:"
        echo "   DynamoDB Local:  http://localhost:8000"
        echo "   DynamoDB Admin:  http://localhost:8001"
        echo ""
        echo "📝 Next steps:"
        echo "1. Set up backend:"
        echo "   cd backend"
        echo "   python -m venv venv"
        echo "   source venv/bin/activate"
        echo "   pip install -r requirements.txt"
        echo ""
        echo "2. Set up frontend:"
        echo "   cd frontend"
        echo "   npm install"
        echo "   npm run dev"
        ;;
    
    3)
        echo ""
        echo "☁️  Deploying to AWS..."
        
        # Check AWS CLI
        if ! command -v aws &> /dev/null; then
            echo -e "${RED}❌ AWS CLI not found. Please install it first.${NC}"
            exit 1
        fi
        
        # Check AWS credentials
        if ! aws sts get-caller-identity &> /dev/null; then
            echo -e "${RED}❌ AWS credentials not configured. Run 'aws configure' first.${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}✅ AWS credentials configured${NC}"
        
        # Run infrastructure setup
        cd infrastructure
        chmod +x setup.sh
        ./setup.sh
        
        cd ..
        echo ""
        echo -e "${GREEN}✅ AWS infrastructure deployed!${NC}"
        echo ""
        echo "📝 Next steps:"
        echo "1. Deploy Lambda functions:"
        echo "   cd backend"
        echo "   ./deploy_lambda.sh"
        echo ""
        echo "2. Build and deploy frontend:"
        echo "   cd frontend"
        echo "   npm run build"
        echo "   aws s3 sync dist/ s3://\$S3_BUCKET_STATIC/"
        echo ""
        echo "3. Seed demo data:"
        echo "   cd backend"
        echo "   python seed_data.py"
        ;;
    
    *)
        echo -e "${RED}❌ Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📚 Documentation:"
echo "   README.md           - Project overview"
echo "   docs/API.md         - API documentation"
echo "   docs/architecture.md - Architecture details"
echo "   docs/DEPLOYMENT.md  - Deployment guide"
echo ""
echo "🤝 Contributing:"
echo "   See CONTRIBUTING.md for guidelines"
echo ""
echo "❓ Need help?"
echo "   Open an issue: https://github.com/your-username/smart-vendors/issues"
echo ""
