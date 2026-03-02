# Enable AWS AI Services - Step-by-Step Guide

## 🎯 Overview

This guide will help you enable AWS Bedrock and Transcribe services for your Smart Vendors backend.

**Current Status**:
- ✅ IAM Permissions: Added to Lambda role and user
- ⏳ Bedrock: Needs model access request
- ⏳ Transcribe: Permissions added, may need time to propagate
- ✅ SageMaker: Using demo mode (no action needed)

---

## 1️⃣ Enable AWS Bedrock (Required for Transaction Extraction)

### Step 1: Open AWS Bedrock Console

Click this link or copy to your browser:
```
https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/modelaccess
```

### Step 2: Request Model Access

1. You'll see a page titled "Model access"
2. Click the **"Manage model access"** or **"Edit"** button (orange button on the right)
3. You'll see a list of available models

### Step 3: Enable Claude Models

Scroll down and check the boxes for these models:

- ✅ **Anthropic**
  - ✅ Claude 3.5 Sonnet
  - ✅ Claude 3 Sonnet
  - ✅ Claude 3 Haiku
  - ✅ Claude 2.1
  - ✅ Claude 2
  - ✅ Claude Instant 1.2

### Step 4: Save Changes

1. Scroll to the bottom
2. Click **"Save changes"** button
3. Wait for approval (usually instant - status will change to "Access granted")

### Step 5: Verify Access

After approval, run this command to verify:

```bash
cd backend
python deployment/validate_prerequisites.py
```

You should see:
```
✓ PASS   | AWS Bedrock          | Bedrock available in ap-south-1 with Claude models ✓
```

---

## 2️⃣ Enable AWS Transcribe (Required for Voice Transcription)

### Option A: Wait for Permissions to Propagate (Recommended)

IAM permissions can take 5-15 minutes to fully propagate. Wait 10 minutes and test again:

```bash
cd backend
python deployment/validate_prerequisites.py
```

### Option B: Add Permissions via AWS Console

If waiting doesn't work, add permissions manually:

1. **Open IAM Console**:
   ```
   https://console.aws.amazon.com/iam/home?region=ap-south-1#/users/smart-vendors-deploy
   ```

2. **Add Inline Policy**:
   - Click "Add permissions" → "Create inline policy"
   - Click "JSON" tab
   - Paste this policy:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "transcribe:*"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

3. **Review and Create**:
   - Click "Review policy"
   - Name it: `TranscribeFullAccess`
   - Click "Create policy"

4. **Verify**:
   ```bash
   cd backend
   python deployment/validate_prerequisites.py
   ```

### Option C: Attach Managed Policy

1. Open IAM Console (link above)
2. Click "Add permissions" → "Attach policies directly"
3. Search for: `AmazonTranscribeFullAccess`
4. Check the box and click "Add permissions"

---

## 3️⃣ SageMaker (Optional - Already Using Demo Mode)

SageMaker is currently using demo mode, which returns mock freshness classifications. This is sufficient for development and testing.

### To Enable Real SageMaker (Optional):

If you want real ML-based freshness classification:

1. **Train and Deploy Model**:
   - This requires training a custom model
   - Deploying to a SageMaker endpoint
   - Costs ~$50-100/month for endpoint hosting

2. **Update Configuration**:
   ```bash
   # In backend/.env or Lambda environment variables
   DEMO_MODE=false
   SAGEMAKER_ENDPOINT_NAME=your-endpoint-name
   ```

**Recommendation**: Keep using demo mode for now. It's free and works for testing.

---

## 🧪 Verification Commands

### Check All Prerequisites
```bash
cd backend
python deployment/validate_prerequisites.py
```

### Test Specific Services

**Test Bedrock**:
```bash
aws bedrock list-foundation-models --region ap-south-1 | grep -i claude
```

**Test Transcribe**:
```bash
aws transcribe list-transcription-jobs --region ap-south-1 --max-results 1
```

**Test Lambda Functions**:
```bash
cd backend
python deployment/test_deployment.py
```

---

## 🎯 Quick Fix Script

Run this automated script to add all permissions:

```bash
cd backend

# Fix Lambda role permissions
python deployment/fix_aws_permissions.py

# Fix user permissions
python deployment/fix_user_permissions.py

# Verify everything
python deployment/validate_prerequisites.py
```

---

## 📊 Expected Results

After completing all steps, you should see:

```
======================================================================
VALIDATION RESULTS
======================================================================

✓ PASS   | Python Version       | Python 3.12.7 ✓
✓ PASS   | AWS CLI              | aws-cli/2.34.0 ✓
✓ PASS   | AWS Credentials      | Authenticated ✓
✓ PASS   | Python Packages      | All required packages installed ✓
✓ PASS   | AWS Bedrock          | Bedrock available with Claude models ✓
✓ PASS   | AWS Transcribe       | Transcribe available in ap-south-1 ✓
✓ PASS   | AWS SageMaker        | SageMaker available (demo mode) ⚠️
======================================================================
✓ All checks passed! Ready to deploy.
======================================================================
```

---

## 🐛 Troubleshooting

### Issue: "Access Denied" for Bedrock

**Cause**: Model access not requested

**Solution**: Follow Step 1 above to request model access in AWS Console

### Issue: "Access Denied" for Transcribe

**Cause**: Permissions not propagated or not attached

**Solutions**:
1. Wait 10-15 minutes for IAM propagation
2. Follow Option B or C in Step 2 above
3. Check if there are permission boundaries on your IAM user

### Issue: Can't Access AWS Console

**Cause**: Don't have console access

**Solution**: Ask your AWS administrator to:
1. Enable console access for your IAM user
2. Or add the required permissions directly

### Issue: Permissions Added But Still Denied

**Cause**: Permission boundaries or SCPs (Service Control Policies)

**Solution**: Check with AWS administrator if there are:
- Permission boundaries on your IAM user
- Service Control Policies (SCPs) restricting Bedrock/Transcribe
- Resource-based policies blocking access

---

## 📞 Need Help?

### Check Current Permissions

```bash
# Check user policies
aws iam list-user-policies --user-name smart-vendors-deploy

# Check attached policies
aws iam list-attached-user-policies --user-name smart-vendors-deploy

# Check Lambda role policies
aws iam list-role-policies --role-name smart-vendors-lambda-execution-dev
```

### Get IAM Policy Simulator

Test permissions without making actual API calls:
```
https://policysim.aws.amazon.com/
```

### AWS Support

If you're still having issues:
1. Check AWS Service Health Dashboard
2. Contact AWS Support
3. Check CloudTrail logs for detailed error messages

---

## ✅ Success Checklist

- [ ] Bedrock model access requested and approved
- [ ] Transcribe permissions added and working
- [ ] SageMaker in demo mode (or endpoint deployed)
- [ ] All prerequisite checks passing
- [ ] Lambda functions can invoke AI services
- [ ] API endpoints returning successful responses

---

## 🚀 Next Steps After Enabling Services

Once all services are enabled:

1. **Test Voice Transcription**:
   ```bash
   curl -X POST https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com/voice/transcribe \
     -H "Content-Type: application/json" \
     -d '{"audio": "base64_audio", "vendor_id": "test-123"}'
   ```

2. **Test Transaction Extraction**:
   ```bash
   curl -X POST https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com/transactions \
     -H "Content-Type: application/json" \
     -d '{"text": "2 kg tomatoes 50 rupees", "vendor_id": "test-123"}'
   ```

3. **Test Freshness Classification**:
   ```bash
   curl -X POST https://ji5ymmu4g7.execute-api.ap-south-1.amazonaws.com/freshness/classify \
     -H "Content-Type: application/json" \
     -d '{"image": "base64_image", "vendor_id": "test-123"}'
   ```

---

**Last Updated**: March 3, 2026  
**Region**: ap-south-1 (Mumbai)  
**Account**: 410431701036
