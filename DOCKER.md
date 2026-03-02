# Docker Setup Guide

This guide explains how to use Docker for local development and deployment of Smart Vendors.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Compose Services](#docker-compose-services)
- [Local Development](#local-development)
- [Building Docker Images](#building-docker-images)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### One-Command Setup

```bash
chmod +x setup.sh
./setup.sh
```

Choose option 1 for full local development environment.

---

## Docker Compose Services

The `docker-compose.yml` file defines these services:

### 1. DynamoDB Local

**Purpose**: Local DynamoDB for development without AWS costs

**Port**: 8000

**Usage**:
```bash
# Access DynamoDB Local
aws dynamodb list-tables --endpoint-url http://localhost:8000

# Create table
aws dynamodb create-table \
  --table-name test-table \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --endpoint-url http://localhost:8000
```

### 2. DynamoDB Admin UI

**Purpose**: Web UI for managing DynamoDB Local

**Port**: 8001

**Access**: http://localhost:8001

**Features**:
- View tables and items
- Create/update/delete items
- Query and scan tables
- Export data

### 3. LocalStack

**Purpose**: Emulate AWS services locally

**Port**: 4566

**Services Emulated**:
- S3 (object storage)
- Lambda (serverless functions)
- SNS (notifications)
- Transcribe (speech-to-text)
- SageMaker (ML inference)

**Usage**:
```bash
# Create S3 bucket
aws s3 mb s3://test-bucket --endpoint-url http://localhost:4566

# Upload file
aws s3 cp file.txt s3://test-bucket/ --endpoint-url http://localhost:4566

# List buckets
aws s3 ls --endpoint-url http://localhost:4566
```

### 4. Backend API

**Purpose**: FastAPI backend for local testing

**Port**: 8080

**Access**: http://localhost:8080

**Endpoints**:
- GET /health - Health check
- POST /voice/transcribe - Voice transcription
- GET /prices/{item} - Market prices
- POST /freshness/classify - Freshness classification

### 5. Frontend

**Purpose**: React frontend served by Nginx

**Port**: 3000

**Access**: http://localhost:3000

**Features**:
- Hot reload (in development mode)
- Production-optimized build
- Gzip compression
- SPA routing

---

## Local Development

### Start All Services

```bash
docker-compose up -d
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services

```bash
docker-compose down
```

### Restart Service

```bash
docker-compose restart backend
```

### Rebuild Service

```bash
docker-compose up -d --build backend
```

### Access Service Shell

```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh
```

---

## Building Docker Images

### Backend Lambda Image

```bash
cd backend
docker build -t smart-vendors-backend:latest .

# Test locally
docker run -p 8080:8080 \
  -e AWS_REGION=us-east-1 \
  -e DEMO_MODE=true \
  smart-vendors-backend:latest
```

### Frontend Image

```bash
cd frontend
docker build -t smart-vendors-frontend:latest .

# Test locally
docker run -p 3000:80 smart-vendors-frontend:latest
```

### Push to ECR (AWS)

```bash
# Login to ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

# Tag image
docker tag smart-vendors-backend:latest \
  ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/smart-vendors-backend:latest

# Push image
docker push ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/smart-vendors-backend:latest
```

---

## Development Workflow

### 1. Start Services

```bash
./setup.sh
# Choose option 1
```

### 2. Create DynamoDB Tables

```bash
cd backend
python scripts/create_local_tables.py
```

### 3. Seed Demo Data

```bash
python seed_data.py --local
```

### 4. Test Backend

```bash
# Health check
curl http://localhost:8080/health

# Get market prices
curl http://localhost:8080/prices/tomatoes
```

### 5. Test Frontend

Open http://localhost:3000 in browser

### 6. Make Changes

- Backend: Edit files in `backend/`, service auto-reloads
- Frontend: Edit files in `frontend/src/`, Vite hot-reloads

### 7. View Logs

```bash
docker-compose logs -f backend frontend
```

---

## Troubleshooting

### Port Already in Use

**Issue**: `Error: port 8000 is already allocated`

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### Container Won't Start

**Issue**: Container exits immediately

**Solution**:
```bash
# Check logs
docker-compose logs backend

# Check container status
docker-compose ps

# Rebuild container
docker-compose up -d --build backend
```

### DynamoDB Connection Error

**Issue**: Backend can't connect to DynamoDB Local

**Solution**:
```bash
# Verify DynamoDB is running
docker-compose ps dynamodb-local

# Check network
docker network inspect smart-vendors-network

# Restart DynamoDB
docker-compose restart dynamodb-local
```

### LocalStack Not Working

**Issue**: AWS services not responding

**Solution**:
```bash
# Check LocalStack logs
docker-compose logs localstack

# Verify services are ready
curl http://localhost:4566/_localstack/health

# Restart LocalStack
docker-compose restart localstack
```

### Out of Disk Space

**Issue**: Docker build fails with "no space left on device"

**Solution**:
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused containers
docker container prune

# Clean everything
docker system prune -a --volumes
```

### Slow Performance

**Issue**: Docker containers are slow

**Solution**:
1. Increase Docker memory allocation (Docker Desktop → Settings → Resources)
2. Use volume mounts instead of bind mounts
3. Disable unnecessary services in docker-compose.yml
4. Use Docker BuildKit for faster builds:
   ```bash
   export DOCKER_BUILDKIT=1
   docker-compose build
   ```

---

## Environment Variables

### Backend

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
DYNAMODB_ENDPOINT=http://dynamodb-local:8000
S3_ENDPOINT=http://localstack:4566
DEMO_MODE=true
LOG_LEVEL=DEBUG
```

### Frontend

```bash
VITE_API_BASE_URL=http://localhost:8080
```

---

## Production Deployment

### Build Production Images

```bash
# Backend
docker build -t smart-vendors-backend:prod \
  --build-arg ENV=production \
  backend/

# Frontend
docker build -t smart-vendors-frontend:prod \
  --build-arg NODE_ENV=production \
  frontend/
```

### Deploy to AWS ECS

See `docs/DEPLOYMENT.md` for AWS deployment instructions.

---

## Docker Best Practices

1. **Use .dockerignore**: Exclude unnecessary files from build context
2. **Multi-stage builds**: Reduce final image size (see frontend/Dockerfile)
3. **Layer caching**: Order Dockerfile commands from least to most frequently changing
4. **Security**: Don't include secrets in images, use environment variables
5. **Health checks**: Add HEALTHCHECK instructions to Dockerfiles
6. **Logging**: Use structured logging (JSON) for better log aggregation

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [LocalStack Documentation](https://docs.localstack.cloud/)
- [DynamoDB Local Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)

---

## Support

For Docker-related issues:
- Check logs: `docker-compose logs -f`
- Verify services: `docker-compose ps`
- Restart services: `docker-compose restart`
- Open an issue: https://github.com/your-username/smart-vendors/issues
