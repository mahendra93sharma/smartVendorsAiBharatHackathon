# AWS Configuration Guide

## Prerequisites

You need:
1. AWS Account (free tier available)
2. AWS CLI installed
3. AWS credentials (Access Key ID and Secret Access Key)

---

## Step 1: Create AWS Account

1. Go to https://aws.amazon.com
2. Click "Create an AWS Account"
3. Follow the signup process
4. Verify your email
5. Add payment method (free tier available)

---

## Step 2: Install AWS CLI

### macOS (you're on macOS):
```bash
# Using Homebrew
brew install awscli

# Or using pip
pip3 install awscli
```

### Verify installation:
```bash
aws --version
```

Expected output: `aws-cli/2.x.x Python/3.x.x Darwin/xx.x.x`

---

## Step 3: Get AWS Credentials

### Method A: IAM User (Recommended)

1. **Login to AWS Console:**
   - Go to https://console.aws.amazon.com
   - Login with your account

2. **Create IAM User:**
   - Go to IAM service
   - Click "Users" → "Add users"
   - Username: `smart-vendors-deploy`
   - Access type: ✅ Programmatic access
   - Click "Next: Permissions"

3. **Attach Policies:**
   - Click "Attach existing policies directly"
   - Select these policies:
     - ✅ AmazonS3FullAccess
     - ✅ AmazonDynamoDBFullAccess
     - ✅ AWSLambda_FullAccess
     - ✅ IAMFullAccess
     - ✅ CloudFrontFullAccess
     - ✅ AmazonAPIGatewayAdministrator
   - Click "Next" → "Create user"

4. **Save Credentials:**
   - You'll see:
     - Access Key ID: `AKIA...`
     - Secret Access Key: `wJalr...`
   - **IMPORTANT:** Download CSV or copy these - you can't see them again!

### Method B: Root User (Not Recommended)

1. Go to AWS Console
2. Click your name → Security Credentials
3. Create Access Key
4. Save credentials

---

## Step 4: Configure AWS CLI

Run this command:
```bash
aws configure
```

You'll be prompted:

```
AWS Access Key ID [None]: AKIA... (paste your Access Key ID)
AWS Secret Access Key [None]: wJalr... (paste your Secret Access Key)
Default region name [None]: us-east-1 (or ap-south-1 for India)
Default output format [None]: json
```

---

## Step 5: Verify Configuration

```bash
# Test AWS connection
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDA...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/smart-vendors-deploy"
}
```

If you see this, AWS is configured! ✅

---

## Step 6: Deploy to AWS

Now you can deploy the full stack:

### Option A: Deploy Frontend to S3 + CloudFront

```bash
# Build frontend
cd frontend
npm run build

# Create S3 bucket
aws s3 mb s3://smart-vendors-frontend-$(date +%s)

# Upload to S3
aws s3 sync dist/ s3://smart-vendors-frontend-$(date +%s)/ --acl public-read

# Enable website hosting
aws s3 website s3://smart-vendors-frontend-$(date +%s)/ \
  --index-document index.html \
  --error-document index.html
```

Your URL: `http://smart-vendors-frontend-xxx.s3-website-us-east-1.amazonaws.com`

### Option B: Full AWS Deployment (Lambda + DynamoDB)

Follow the comprehensive guide:
```bash
# Read the full deployment guide
cat DEPLOYMENT_CHECKLIST.md
```

This includes:
- Creating DynamoDB tables
- Deploying Lambda functions
- Setting up API Gateway
- Configuring IAM roles
- Deploying frontend to S3/CloudFront

---

## AWS Regions

Choose a region close to your users:

- **US East (N. Virginia):** `us-east-1` (most services)
- **Asia Pacific (Mumbai):** `ap-south-1` (India)
- **US West (Oregon):** `us-west-2`
- **Europe (Ireland):** `eu-west-1`

---

## Cost Estimate

### Free Tier (First 12 months):
- S3: 5 GB storage
- Lambda: 1M requests/month
- DynamoDB: 25 GB storage
- CloudFront: 50 GB data transfer

### After Free Tier:
- Frontend only: ~$1-2/month
- Full stack: ~$10-20/month

---

## Security Best Practices

1. **Never commit credentials to Git:**
   ```bash
   # Add to .gitignore
   echo ".aws/" >> .gitignore
   echo "*.pem" >> .gitignore
   ```

2. **Use IAM roles for Lambda:**
   - Don't hardcode credentials in Lambda functions
   - Use IAM roles instead

3. **Enable MFA:**
   - Go to IAM → Users → Security credentials
   - Enable Multi-Factor Authentication

4. **Rotate credentials regularly:**
   - Create new access keys every 90 days
   - Delete old keys

---

## Troubleshooting

### Problem: "aws: command not found"
```bash
# Install AWS CLI
brew install awscli
# Or
pip3 install awscli
```

### Problem: "Unable to locate credentials"
```bash
# Reconfigure AWS
aws configure
```

### Problem: "Access Denied"
```bash
# Check your credentials
aws sts get-caller-identity

# Verify IAM permissions in AWS Console
```

### Problem: "Region not found"
```bash
# Set region explicitly
aws configure set region us-east-1
```

---

## Quick Commands Reference

```bash
# Check configuration
aws configure list

# Test connection
aws sts get-caller-identity

# List S3 buckets
aws s3 ls

# List Lambda functions
aws lambda list-functions

# List DynamoDB tables
aws dynamodb list-tables

# Check region
aws configure get region
```

---

## Alternative: AWS Amplify (Easier)

If AWS CLI is too complex, use AWS Amplify:

1. **Install Amplify CLI:**
   ```bash
   npm install -g @aws-amplify/cli
   ```

2. **Configure:**
   ```bash
   amplify configure
   ```
   (Opens browser, easier setup)

3. **Deploy:**
   ```bash
   cd frontend
   amplify init
   amplify add hosting
   amplify publish
   ```

You'll get: `https://xxx.amplifyapp.com`

---

## Recommendation

**For hackathon submission, I recommend:**

1. **Use Vercel** (no AWS needed) - Get URL in 5 minutes
2. **Then optionally** deploy to AWS for bonus points

**Why?**
- Vercel: Fast, free, works perfectly for demo
- AWS: More complex, takes 30-60 minutes, costs money

**Your demo mode works perfectly on Vercel without any backend!**

---

## Summary

### To Configure AWS:
1. Create AWS account
2. Install AWS CLI: `brew install awscli`
3. Create IAM user with permissions
4. Run: `aws configure`
5. Enter credentials
6. Test: `aws sts get-caller-identity`

### To Deploy:
- **Quick (Vercel):** 5 minutes, no AWS needed
- **Full AWS:** 30-60 minutes, requires AWS account

---

## Need Help?

- AWS Documentation: https://docs.aws.amazon.com
- AWS Free Tier: https://aws.amazon.com/free
- AWS Support: https://console.aws.amazon.com/support

---

**Recommendation: Use Vercel for now, deploy to AWS later if needed!**
