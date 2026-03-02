# Smart Vendors Backend

Serverless backend built with AWS Lambda, DynamoDB, and AI services (Bedrock, Transcribe, SageMaker).

## Architecture

The backend consists of:

- **Lambda Functions**: Serverless API endpoints
- **DynamoDB**: NoSQL database for all data
- **AWS AI Services**: Transcribe, Bedrock, SageMaker
- **S3**: Storage for images and ML models

## Directory Structure

```
backend/
├── lambda_functions/          # Lambda function handlers
│   ├── voice_transcribe/      # Voice-to-text endpoint
│   ├── transaction_extract/   # Transaction extraction
│   ├── price_query/           # Market price queries
│   ├── freshness_classify/    # Freshness classification
│   ├── marketplace_create/    # Create marketplace listing
│   └── trust_score/           # Trust score calculation
├── shared/                    # Shared code (Lambda layer)
│   ├── models/                # Data models
│   ├── services/              # Business logic
│   └── aws/                   # AWS service clients
├── scripts/                   # Utility scripts
│   └── seed_data.py          # Demo data seeding
└── tests/                     # Test suite
    ├── unit/                  # Unit tests
    ├── integration/           # Integration tests
    └── property/              # Property-based tests
```

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Configure Environment

```bash
cp ../.env.example .env
# Edit .env with your AWS credentials
```

### Run Tests

```bash
pytest tests/ -v
```

## Lambda Functions

### Voice Transcribe

**Endpoint**: `POST /voice/transcribe`

Transcribes audio using AWS Transcribe.

**Request:**
```json
{
  "audio_base64": "...",
  "language": "hi-IN"
}
```

**Response:**
```json
{
  "text": "Do kilo tamatar pachas rupaye",
  "confidence": 0.95,
  "language": "hi-IN"
}
```

### Transaction Extract

**Endpoint**: `POST /transactions`

Extracts transaction from text using Bedrock.

**Request:**
```json
{
  "text": "Do kilo tamatar pachas rupaye",
  "vendor_id": "vendor-123"
}
```

**Response:**
```json
{
  "transaction_id": "txn-456",
  "item_name": "tamatar",
  "quantity": 2.0,
  "unit": "kg",
  "price": 50.0
}
```

### Price Query

**Endpoint**: `GET /prices/{item}`

Queries market prices from DynamoDB.

**Response:**
```json
{
  "item": "tomatoes",
  "prices": [
    {
      "mandi_name": "Azadpur",
      "price_per_kg": 30.0,
      "distance_km": 5.2
    }
  ]
}
```

### Freshness Classify

**Endpoint**: `POST /freshness/classify`

Classifies produce freshness using SageMaker.

**Request:**
```json
{
  "image_base64": "..."
}
```

**Response:**
```json
{
  "category": "Fresh",
  "confidence": 0.89,
  "shelf_life_hours": 48
}
```

### Marketplace Create

**Endpoint**: `POST /marketplace/listings`

Creates B-Grade marketplace listing.

**Request:**
```json
{
  "vendor_id": "vendor-123",
  "item_name": "tomatoes",
  "weight_kg": 10.0,
  "price": 200.0
}
```

**Response:**
```json
{
  "listing_id": "listing-789",
  "buyers_notified": 5,
  "mandi_credits_earned": 100
}
```

### Trust Score

**Endpoint**: `GET /trust-score/{vendor_id}`

Calculates vendor trust score.

**Response:**
```json
{
  "vendor_id": "vendor-123",
  "trust_score": 150,
  "tier": "Silver",
  "breakdown": {
    "transactions": 100,
    "marketplace_sales": 40,
    "consistency": 10
  }
}
```

## Deployment

### Package Lambda Functions

```bash
./deploy_lambda.sh
```

### Deploy Individual Function

```bash
cd lambda_functions/voice_transcribe
zip -r function.zip .
aws lambda update-function-code \
  --function-name smart-vendors-voice-transcribe-dev \
  --zip-file fileb://function.zip
```

## Testing

### Unit Tests

```bash
pytest tests/unit/ -v
```

### Integration Tests

```bash
pytest tests/integration/ -v
```

### Property-Based Tests

```bash
pytest tests/property/ -v --hypothesis-iterations=100
```

### Coverage Report

```bash
pytest --cov=lambda_functions --cov=shared --cov-report=html
open htmlcov/index.html
```

## Development

### Code Formatting

```bash
black .
isort .
```

### Type Checking

```bash
mypy lambda_functions/ shared/
```

### Linting

```bash
flake8 lambda_functions/ shared/
```

## Environment Variables

Required environment variables for Lambda functions:

```bash
AWS_REGION=ap-south-1
S3_BUCKET_IMAGES=smart-vendors-images-dev
DYNAMODB_TABLE_VENDORS=smart-vendors-vendors-dev
DYNAMODB_TABLE_TRANSACTIONS=smart-vendors-transactions-dev
DYNAMODB_TABLE_MARKET_PRICES=smart-vendors-market-prices-dev
DYNAMODB_TABLE_MARKETPLACE_LISTINGS=smart-vendors-marketplace-listings-dev
BEDROCK_MODEL_ID=anthropic.claude-v2
SAGEMAKER_ENDPOINT_NAME=smart-vendors-freshness-classifier
```

## Troubleshooting

### Lambda Timeout

Increase timeout in Terraform:

```hcl
timeout = 30  # seconds
```

### Memory Issues

Increase memory in Terraform:

```hcl
memory_size = 512  # MB
```

### DynamoDB Throttling

Switch to provisioned capacity or increase on-demand limits.

### Bedrock Access

Ensure your AWS account has Bedrock access enabled in the region.
