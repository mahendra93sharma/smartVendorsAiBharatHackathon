# Smart Vendors - Voice-First Decision Intelligence for Street Vendors

[![Deploy to AWS](https://github.com/your-username/smart-vendors/actions/workflows/deploy.yml/badge.svg)](https://github.com/your-username/smart-vendors/actions/workflows/deploy.yml)

> Empowering Delhi-NCR street vendors with AI-powered voice transactions, market intelligence, and waste reduction tools.

## 🎯 Problem Statement

Street vendors in Delhi-NCR face critical challenges:

- **40% produce waste** due to lack of freshness assessment and market timing
- **Information asymmetry** - No access to real-time market prices from mandis (Azadpur, Ghazipur, Okhla)
- **Financial exclusion** - No digital transaction records for credit access
- **Low literacy** - Traditional apps require typing and reading
- **Limited resources** - 2GB RAM devices, 3G connectivity, Hindi-first users

## 💡 Solution

Smart Vendors is a voice-first mobile application that provides:

1. **Voice Transaction Recording** - Record sales in Hindi/English without typing
2. **Market Price Intelligence** - Real-time prices from 3 nearby mandis
3. **Freshness Scanner** - AI-powered produce classification (Fresh/B-Grade/Waste)
4. **Waste Marketplace** - Monetize B-Grade produce through buyer matching
5. **Trust Score** - Build credit history through consistent usage

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Access (Mobile/Web)                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CloudFront CDN + S3 (React Frontend)                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  API Gateway (HTTP API)                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────┐    ┌──────────────────────┐
│  Lambda Functions    │    │  AWS AI Services     │
│  - Voice API         │    │  - Transcribe        │
│  - Price API         │    │  - Bedrock (NLP)     │
│  - Freshness API     │    │  - SageMaker (ML)    │
│  - Marketplace API   │    │  - SNS (Notify)      │
└──────────────────────┘    └──────────────────────┘
                │
    ┌───────────┴───────────┐
    ▼                       ▼
┌──────────┐          ┌──────────┐
│ DynamoDB │          │ S3       │
│ Tables   │          │ Buckets  │
└──────────┘          └──────────┘
```

## 🚀 AWS Services Used

| Service | Purpose |
|---------|---------|
| **Amazon Bedrock** | NLP for transaction extraction from voice transcriptions |
| **AWS Lambda** | Serverless compute for all API endpoints |
| **Amazon S3** | Storage for images, static assets, and ML models |
| **Amazon DynamoDB** | NoSQL database for vendors, transactions, prices, listings |
| **Amazon SageMaker** | ML model inference for produce freshness classification |
| **AWS Transcribe** | Speech-to-text for Hindi and English voice input |
| **Amazon CloudFront** | CDN for fast frontend delivery |
| **Amazon API Gateway** | HTTP API routing to Lambda functions |
| **Amazon SNS** | Buyer notifications for marketplace |
| **AWS IAM** | Security and access management |

## 📸 Screenshots

### Voice Transaction Recording
Record sales in Hindi or English without typing. The app transcribes your voice and extracts transaction details automatically.

![Voice Recording](docs/screenshots/voice-recording.png)

### Market Price Intelligence
Compare prices from 3 nearby mandis (Azadpur, Ghazipur, Okhla) to make informed purchasing decisions.

![Price Intelligence](docs/screenshots/price-intelligence.png)

### Freshness Scanner
AI-powered produce classification helps reduce waste by identifying Fresh, B-Grade, and Waste categories with shelf life estimates.

![Freshness Scanner](docs/screenshots/freshness-scanner.png)

### Marketplace
Monetize B-Grade produce by listing it on the marketplace and connecting with nearby buyers.

![Marketplace](docs/screenshots/marketplace.png)

### Trust Score Profile
Build credit history through consistent usage. Progress from Bronze to Silver to Gold tiers.

![Trust Score](docs/screenshots/trust-score.png)

## 🎬 Demo Video

Watch our 4-minute demo: [Smart Vendors Demo on YouTube](https://youtube.com/watch?v=YOUR_VIDEO_ID)

## 🏃 Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured (`aws configure`)
- Terraform 1.0+
- Python 3.11+
- Node.js 18+

### 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-vendors.git
cd smart-vendors
```

### 2. Deploy Infrastructure

```bash
cd infrastructure
chmod +x setup.sh
./setup.sh
```

This will:
- Create S3 buckets, DynamoDB tables, Lambda roles
- Set up CloudFront distribution and API Gateway
- Generate environment configuration

### 3. Deploy Backend (Lambda Functions)

```bash
cd backend
pip install -r requirements.txt
./deploy_lambda.sh
```

### 4. Deploy Frontend

```bash
cd frontend
npm install
npm run build
aws s3 sync dist/ s3://smart-vendors-static-dev/
```

### 5. Seed Demo Data

```bash
cd backend/scripts
python seed_data.py
```

### 6. Access Application

Frontend: `https://[CLOUDFRONT_DOMAIN]` (from Terraform outputs)

**Demo Credentials:**
- Username: `demo_vendor`
- Password: `hackathon2024`

## 🧪 Testing

### Run All Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# Property-based tests
pytest tests/property/ -v
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Property-based tests (100 iterations)
pytest tests/property/ --hypothesis-iterations=100
```

## 🔧 Troubleshooting

### Common Issues

**Issue: Lambda function timeout**
- Solution: Increase timeout in `infrastructure/terraform/lambda.tf` (default: 30s, increase to 60s)
- Check CloudWatch logs: `aws logs tail /aws/lambda/smart-vendors-voice-api --follow`

**Issue: Transcribe quota exceeded**
- Solution: Demo mode uses pre-transcribed samples. For production, request quota increase in AWS Console
- Fallback: App automatically switches to text input mode

**Issue: Frontend can't connect to API**
- Solution: Verify API Gateway URL in `frontend/.env`: `VITE_API_BASE_URL=https://[API_ID].execute-api.[REGION].amazonaws.com`
- Check CORS configuration in API Gateway

**Issue: DynamoDB table not found**
- Solution: Run infrastructure setup: `cd infrastructure && ./setup.sh`
- Verify tables exist: `aws dynamodb list-tables`

**Issue: SageMaker endpoint not available**
- Solution: Deploy endpoint using guide in `docs/SAGEMAKER_ENDPOINT_SETUP.md`
- Fallback: App uses rule-based classification for demo

**Issue: Demo credentials don't work**
- Solution: Run seed script: `cd backend && python seed_data.py`
- Verify vendor exists: `aws dynamodb get-item --table-name smart-vendors-vendors-dev --key '{"vendor_id": {"S": "demo-vendor-001"}}'`

### Getting Help

- Check [Deployment Guide](docs/DEPLOYMENT.md) for detailed setup instructions
- Review [API Documentation](docs/API.md) for endpoint details
- Open an issue on GitHub with logs and error messages

## 📚 Documentation

- [Architecture Documentation](docs/architecture.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 📊 Impact Metrics

### Projected Outcomes (Year 1)

- **30% waste reduction** through freshness assessment and B-Grade marketplace
- **20% income increase** through better pricing decisions and waste monetization
- **10,000 vendors** building digital credit history for financial inclusion
- **₹50 lakhs** in B-Grade produce monetized through marketplace

### Environmental Impact

- **500 tons** of produce waste diverted from landfills
- **1,200 tons CO₂** emissions avoided
- **Circular economy** model for urban food systems

## 🗺️ Roadmap

### Phase 1 (Current - Hackathon MVP)
- ✅ Voice transaction recording
- ✅ Market price intelligence
- ✅ Freshness scanner
- ✅ B-Grade marketplace
- ✅ Trust Score system

### Phase 2 (Q1 2025)
- WhatsApp integration for wider reach
- Demand prediction using historical data
- Weather-based recommendations
- Multi-city expansion (Mumbai, Bangalore)

### Phase 3 (Q2 2025)
- Community features (vendor networks)
- Microfinance integration
- Inventory management
- Supplier connections

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Python: Black formatter, type hints required
- TypeScript: Prettier, ESLint, strict mode
- Commits: Conventional Commits format

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👥 Team

- **[Your Name]** - Full Stack Developer - [GitHub](https://github.com/your-username)
- **[Team Member 2]** - ML Engineer
- **[Team Member 3]** - UI/UX Designer

## 📞 Contact

- **Email**: your-email@example.com
- **GitHub**: [@your-username](https://github.com/your-username)
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- AWS AI for Bharat Hackathon
- Delhi-NCR street vendor community for insights
- Open source community for tools and libraries

## 📋 Submission Checklist

- ✅ Working prototype deployed on AWS
- ✅ GitHub repository with comprehensive documentation
- ✅ Demo video (3-5 minutes)
- ✅ Project summary document
- ✅ All AWS services integrated and documented
- ✅ Demo credentials provided
- ✅ Public accessibility verified

---

**Built with ❤️ for Delhi-NCR street vendors**

**Powered by AWS AI Services**
