# Smart Vendors - Quick Deployment Guide

## Prerequisites
- AWS Account configured (`aws configure`)
- Docker installed
- Node.js 18+ and Python 3.11+ installed

## Quick Deploy Steps

### 1. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
# Choose option 3 for AWS deployment
```

### 2. Deploy Backend
```bash
cd backend
chmod +x deploy_lambda.sh
./deploy_lambda.sh
```

### 3. Seed Demo Data
```bash
cd backend
python seed_data.py
```

### 4. Deploy Frontend
```bash
cd frontend
npm run build
aws s3 sync dist/ s3://smart-vendors-static-dev/
```

### 5. Verify Deployment
```bash
python verify_submission.py
```

## Important Files Created

1. **DEPLOYMENT_CHECKLIST.md** - Complete step-by-step AWS deployment guide
2. **verify_submission.py** - Automated verification script
3. **SUBMISSION_CHECKLIST.md** - Hackathon submission checklist
4. **QUICK_DEPLOY.md** - This file (quick reference)

## Next Steps

1. Follow **DEPLOYMENT_CHECKLIST.md** for detailed AWS setup
2. Run **verify_submission.py** to check all deliverables
3. Complete **SUBMISSION_CHECKLIST.md** before submitting
4. Create demo video (3-5 minutes)
5. Create project summary PDF (1-2 pages)

## Demo Credentials
- Username: `demo_vendor`
- Password: `hackathon2024`

## Support
See DEPLOYMENT_CHECKLIST.md for troubleshooting and detailed instructions.
