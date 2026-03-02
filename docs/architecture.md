# Smart Vendors - Architecture Documentation

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [AWS Services Integration](#aws-services-integration)
- [Serverless Architecture Benefits](#serverless-architecture-benefits)
- [Security Architecture](#security-architecture)
- [Scalability & Performance](#scalability--performance)

---

## System Overview

Smart Vendors is built on a serverless architecture using AWS managed services. The system follows a three-tier architecture:

1. **Presentation Layer**: React frontend hosted on S3 + CloudFront
2. **Application Layer**: AWS Lambda functions orchestrated by API Gateway
3. **Data Layer**: DynamoDB for NoSQL storage, S3 for object storage

This architecture enables:
- Zero server management
- Automatic scaling
- Pay-per-use pricing
- High availability
- Low operational overhead

---

## Architecture Diagram

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Access Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ Mobile Web   │  │ Desktop Web  │  │ Progressive  │              │
│  │ Browser      │  │ Browser      │  │ Web App      │              │
│  └──────────────┘  └──────────────┘  └──────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Content Delivery Layer                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Amazon CloudFront (CDN)                                    │    │
│  │  - Global edge locations                                    │    │
│  │  - HTTPS/SSL termination                                    │    │
│  │  - Caching static assets                                    │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│                              ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Amazon S3 (Static Hosting)                                 │    │
│  │  - React build artifacts                                    │    │
│  │  - HTML, CSS, JavaScript                                    │    │
│  │  - Images, fonts, assets                                    │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       API Gateway Layer                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Amazon API Gateway (HTTP API)                              │    │
│  │  - RESTful API routing                                      │    │
│  │  - Request validation                                       │    │
│  │  - CORS configuration                                       │    │
│  │  - API key management                                       │    │
│  │  - CloudWatch logging                                       │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Voice API    │    │ Price API    │    │ Freshness    │
│ Lambda       │    │ Lambda       │    │ API Lambda   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Transaction  │    │ Marketplace  │    │ Trust Score  │
│ API Lambda   │    │ API Lambda   │    │ API Lambda   │
└──────────────┘    └──────────────┘    └──────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AWS AI/ML Services Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ AWS          │  │ Amazon       │  │ Amazon       │             │
│  │ Transcribe   │  │ Bedrock      │  │ SageMaker    │             │
│  │              │  │              │  │              │             │
│  │ Speech-to-   │  │ NLP for      │  │ ML inference │             │
│  │ text         │  │ transaction  │  │ for produce  │             │
│  │ (Hi/En)      │  │ extraction   │  │ freshness    │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────┐                                                   │
│  │ Amazon SNS   │                                                   │
│  │              │                                                   │
│  │ Buyer        │                                                   │
│  │ notifications│                                                   │
│  └──────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Data Layer                                   │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Amazon DynamoDB (NoSQL Database)                           │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │    │
│  │  │ Vendors      │  │ Transactions │  │ Market       │     │    │
│  │  │ Table        │  │ Table        │  │ Prices Table │     │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │    │
│  │  ┌──────────────┐                                          │    │
│  │  │ Marketplace  │                                          │    │
│  │  │ Listings     │                                          │    │
│  │  └──────────────┘                                          │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Amazon S3 (Object Storage)                                 │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │    │
│  │  │ Audio Files  │  │ Produce      │  │ ML Model     │     │    │
│  │  │ Bucket       │  │ Images       │  │ Artifacts    │     │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Frontend Application (React + Vite)

**Technology Stack**:
- React 18 with TypeScript
- Vite for fast builds
- TailwindCSS for styling
- React Router for navigation
- Web Speech API for voice input

**Key Features**:
- Voice-first UI with large touch targets
- Offline-first with localStorage
- Progressive Web App (PWA) capabilities
- Mobile-responsive design (320px-768px)
- Demo mode with pre-recorded samples

**Deployment**:
- Built artifacts stored in S3
- Served via CloudFront CDN
- HTTPS enabled with AWS Certificate Manager
- Gzip compression for assets

### 2. API Gateway

**Configuration**:
- HTTP API (lower latency than REST API)
- CORS enabled for frontend domain
- API key authentication for production
- CloudWatch logging enabled
- Request/response validation

**Routes**:
```
POST   /voice/transcribe
POST   /transactions
GET    /transactions/{vendor_id}
GET    /prices/{item}
POST   /freshness/classify
POST   /marketplace/listings
GET    /marketplace/buyers
POST   /marketplace/notify
GET    /trust-score/{vendor_id}
```

### 3. Lambda Functions

**Runtime**: Python 3.11

**Architecture**:
```
lambda_functions/
├── voice_transcribe.py          # Voice-to-text + extraction
├── create_transaction.py        # Transaction creation
├── get_transactions.py          # Transaction history
├── get_market_prices.py         # Price queries
├── classify_freshness.py        # Produce classification
├── create_marketplace_listing.py # Listing creation
├── get_marketplace_buyers.py    # Buyer matching
├── notify_marketplace_buyers.py # Buyer notifications
└── get_trust_score.py           # Trust Score calculation
```

**Shared Layer** (Lambda Layer):
```
shared/
├── models/                      # Data models
├── services/                    # Business logic
│   ├── voice_service.py
│   ├── price_service.py
│   ├── freshness_service.py
│   └── marketplace_service.py
├── aws/                         # AWS SDK clients
│   ├── transcribe_client.py
│   ├── bedrock_client.py
│   ├── sagemaker_client.py
│   └── s3_client.py
└── config.py                    # Configuration
```

**Configuration**:
- Memory: 512 MB (voice/freshness), 256 MB (others)
- Timeout: 30 seconds (voice/freshness), 10 seconds (others)
- Environment variables for AWS service endpoints
- IAM role with least-privilege permissions

### 4. AWS AI/ML Services

#### AWS Transcribe
- **Purpose**: Speech-to-text for Hindi and English
- **Configuration**: 
  - Language codes: `hi-IN`, `en-IN`
  - Media formats: MP3, WAV, OGG
  - Vocabulary filtering for produce terms
- **Integration**: Async job submission with polling

#### Amazon Bedrock
- **Purpose**: NLP for transaction extraction
- **Model**: Claude 3 Haiku (fast, cost-effective)
- **Prompt Engineering**:
  - Extract item name, quantity, unit, price
  - Handle Hindi and English text
  - Return structured JSON
- **Fallback**: Rule-based extraction for demo

#### Amazon SageMaker
- **Purpose**: Produce freshness classification
- **Model**: Custom CNN trained on produce images
- **Endpoint**: Real-time inference endpoint
- **Categories**: Fresh, B-Grade, Waste
- **Fallback**: Rule-based color analysis

#### Amazon SNS
- **Purpose**: Buyer notifications
- **Topics**: Marketplace listings by produce type
- **Subscribers**: Buyer phone numbers (SMS)
- **Demo Mode**: Simulated notifications

### 5. Data Layer

#### DynamoDB Tables

**Vendors Table**:
```
Partition Key: vendor_id (String)
Attributes:
  - phone_number (String)
  - name (String)
  - preferred_language (String)
  - district (String)
  - trust_score (Number)
  - tier (String)
  - created_at (String)
```

**Transactions Table**:
```
Partition Key: transaction_id (String)
GSI: vendor_id-timestamp-index
Attributes:
  - vendor_id (String)
  - item_name (String)
  - quantity (Number)
  - unit (String)
  - price_per_unit (Number)
  - total_amount (Number)
  - timestamp (String)
  - recorded_via (String)
```

**Market Prices Table**:
```
Partition Key: item_name (String)
Sort Key: timestamp (String)
TTL: 24 hours
Attributes:
  - mandi_name (String)
  - price_per_kg (Number)
  - distance_km (Number)
```

**Marketplace Listings Table**:
```
Partition Key: listing_id (String)
GSI: vendor_id-created_at-index
Attributes:
  - vendor_id (String)
  - item_name (String)
  - weight_kg (Number)
  - condition (String)
  - price (Number)
  - status (String)
  - created_at (String)
```

#### S3 Buckets

**Audio Files Bucket**:
- Lifecycle: Delete after 7 days
- Encryption: AES-256
- Access: Lambda execution role only

**Produce Images Bucket**:
- Lifecycle: Transition to Glacier after 30 days
- Encryption: AES-256
- Access: Lambda + CloudFront

**ML Models Bucket**:
- Versioning enabled
- Encryption: AES-256
- Access: SageMaker execution role

---

## Data Flow

### Voice Transaction Flow

```
1. User records voice → Frontend captures audio
2. Frontend encodes audio as base64 → POST /voice/transcribe
3. Lambda receives request → Uploads audio to S3
4. Lambda calls AWS Transcribe → Starts transcription job
5. Lambda polls for completion → Gets transcribed text
6. Lambda calls Bedrock → Extracts transaction details
7. Lambda stores transaction → DynamoDB Transactions table
8. Lambda returns response → Frontend displays confirmation
```

**Sequence Diagram**:
```
User → Frontend: Record voice
Frontend → API Gateway: POST /voice/transcribe (audio)
API Gateway → Lambda: Invoke voice_transcribe
Lambda → S3: Upload audio file
Lambda → Transcribe: Start transcription job
Transcribe → Lambda: Transcription result
Lambda → Bedrock: Extract transaction (text)
Bedrock → Lambda: Structured transaction data
Lambda → DynamoDB: Store transaction
DynamoDB → Lambda: Confirmation
Lambda → API Gateway: Response
API Gateway → Frontend: Transaction details
Frontend → User: Display confirmation
```

### Market Price Query Flow

```
1. User searches item → Frontend sends query
2. GET /prices/{item} → Lambda receives request
3. Lambda queries DynamoDB → Market Prices table
4. Lambda filters by item → Sorts by distance
5. Lambda returns top 3 → Frontend displays comparison
```

### Freshness Classification Flow

```
1. User captures image → Frontend encodes as base64
2. POST /freshness/classify → Lambda receives request
3. Lambda uploads to S3 → Produce Images bucket
4. Lambda invokes SageMaker → Endpoint inference
5. SageMaker returns prediction → Category + confidence
6. Lambda applies business logic → Shelf life, suggestions
7. Lambda stores result → DynamoDB (analytics)
8. Lambda returns response → Frontend displays result
```

### Marketplace Listing Flow

```
1. User creates listing → Frontend sends data
2. POST /marketplace/listings → Lambda receives request
3. Lambda stores listing → DynamoDB Listings table
4. Lambda queries buyers → DynamoDB Buyers table (mock)
5. Lambda publishes to SNS → Buyer notification topic
6. SNS sends SMS → Buyer phones
7. Lambda calculates credits → Updates vendor Trust Score
8. Lambda returns response → Frontend displays status
```

---

## AWS Services Integration

### Service Roles and Permissions

**Lambda Execution Role**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:*:*:model/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sagemaker:InvokeEndpoint"
      ],
      "Resource": "arn:aws:sagemaker:*:*:endpoint/smart-vendors-freshness"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/smart-vendors-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::smart-vendors-*/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:*:*:smart-vendors-*"
    }
  ]
}
```

### Cost Optimization

**Strategies**:
1. **Lambda**: Use ARM64 architecture (20% cost savings)
2. **DynamoDB**: On-demand pricing for variable workload
3. **S3**: Lifecycle policies to transition to cheaper storage
4. **CloudFront**: Cache static assets (reduce S3 requests)
5. **Transcribe**: Batch processing for non-real-time use cases
6. **SageMaker**: Use serverless inference for low traffic

**Estimated Monthly Cost** (1000 vendors, 10 transactions/day):
- Lambda: $5
- DynamoDB: $10
- S3: $2
- CloudFront: $3
- Transcribe: $15
- Bedrock: $20
- SageMaker: $30
- **Total**: ~$85/month

---

## Serverless Architecture Benefits

### 1. Zero Server Management
- No EC2 instances to provision or maintain
- No OS patching or security updates
- No capacity planning

### 2. Automatic Scaling
- Lambda scales from 0 to 1000s of concurrent executions
- DynamoDB auto-scales read/write capacity
- CloudFront handles traffic spikes globally

### 3. High Availability
- Multi-AZ deployment by default
- 99.99% SLA for Lambda and DynamoDB
- Automatic failover

### 4. Pay-Per-Use Pricing
- No idle server costs
- Pay only for actual requests
- Free tier covers development/testing

### 5. Fast Development
- Focus on business logic, not infrastructure
- Quick iteration and deployment
- Built-in monitoring with CloudWatch

### 6. Security
- IAM-based access control
- Encryption at rest and in transit
- VPC isolation for sensitive workloads

---

## Security Architecture

### Authentication & Authorization
- API Gateway API keys for production
- IAM authentication for internal services
- JWT tokens for user sessions (future)

### Data Encryption
- **At Rest**: AES-256 for S3 and DynamoDB
- **In Transit**: TLS 1.2+ for all API calls
- **Secrets**: AWS Secrets Manager for API keys

### Network Security
- CloudFront with AWS WAF (Web Application Firewall)
- API Gateway throttling (100 req/min per key)
- Lambda in VPC for database access (optional)

### Compliance
- GDPR: Data deletion on request
- PCI DSS: No credit card data stored
- Data residency: All data in ap-south-1 (Mumbai)

---

## Scalability & Performance

### Current Capacity
- **Concurrent Users**: 1000+
- **Transactions/Second**: 100+
- **API Latency**: <500ms (p95)
- **Frontend Load Time**: <2s (3G network)

### Scaling Strategy

**Horizontal Scaling**:
- Lambda: Automatic (up to account limits)
- DynamoDB: On-demand auto-scaling
- CloudFront: Global edge network

**Vertical Scaling**:
- Lambda memory: 256 MB → 1024 MB (if needed)
- DynamoDB: Provisioned capacity for predictable load

**Caching**:
- CloudFront: 24-hour cache for static assets
- API Gateway: Response caching (5 minutes)
- Application: In-memory caching in Lambda

### Performance Optimization

**Frontend**:
- Code splitting for faster initial load
- Image lazy loading
- Service worker for offline support
- Gzip compression

**Backend**:
- Lambda warm-up (scheduled invocations)
- DynamoDB query optimization (GSI)
- Batch operations for bulk writes
- Async processing for non-critical tasks

**Database**:
- DynamoDB single-table design
- Efficient query patterns (avoid scans)
- TTL for automatic data cleanup
- Composite keys for complex queries

---

## Monitoring & Observability

### CloudWatch Metrics
- Lambda invocations, errors, duration
- API Gateway requests, latency, errors
- DynamoDB read/write capacity, throttles
- Custom metrics: Transaction count, Trust Score distribution

### CloudWatch Logs
- Lambda function logs (structured JSON)
- API Gateway access logs
- Error tracking and alerting

### X-Ray Tracing
- End-to-end request tracing
- Service map visualization
- Performance bottleneck identification

### Alarms
- Lambda error rate > 5%
- API Gateway 5xx errors > 10/min
- DynamoDB throttling events
- SageMaker endpoint failures

---

## Disaster Recovery

### Backup Strategy
- **DynamoDB**: Point-in-time recovery (35 days)
- **S3**: Versioning enabled for critical buckets
- **Lambda**: Code stored in Git + S3

### Recovery Objectives
- **RTO** (Recovery Time Objective): 1 hour
- **RPO** (Recovery Point Objective): 5 minutes

### Multi-Region Strategy (Future)
- Active-passive setup in us-east-1
- DynamoDB Global Tables for replication
- Route 53 health checks for failover

---

## Future Enhancements

### Phase 2
- WebSocket API for real-time updates
- ElastiCache for Redis caching
- Step Functions for complex workflows
- EventBridge for event-driven architecture

### Phase 3
- Multi-region deployment
- GraphQL API with AppSync
- Machine learning pipeline with SageMaker Pipelines
- Data lake with S3 + Athena for analytics

---

## References

- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [API Gateway Performance](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
- [Serverless Architecture Patterns](https://aws.amazon.com/serverless/patterns/)
