# Microphone Permission Error - Fix Guide

## Problem

Your frontend is deployed at: `http://smart-vendors-frontend-1772474994.s3-website.ap-south-1.amazonaws.com/`

The microphone permission error occurs because:
1. **HTTP vs HTTPS**: Modern browsers (Chrome, Firefox, Safari) block microphone access on HTTP sites for security reasons
2. **S3 Static Website Hosting**: Uses HTTP by default, not HTTPS

## Solution Options

### Option 1: Use CloudFront with HTTPS (Recommended)

CloudFront provides free HTTPS certificates and CDN benefits.

#### Steps:

1. **Create CloudFront Distribution**:
```bash
# Navigate to CloudFront in AWS Console
# Click "Create Distribution"
```

2. **Configure Origin**:
   - Origin Domain: `smart-vendors-frontend-1772474994.s3-website.ap-south-1.amazonaws.com`
   - Protocol: HTTP only (S3 website endpoints don't support HTTPS)
   - Origin Path: Leave empty

3. **Configure Distribution Settings**:
   - Viewer Protocol Policy: Redirect HTTP to HTTPS
   - Allowed HTTP Methods: GET, HEAD, OPTIONS
   - Cache Policy: CachingOptimized
   - Default Root Object: `index.html`

4. **Configure Error Pages** (for React Router):
   - Go to "Error Pages" tab
   - Create custom error response:
     - HTTP Error Code: 403
     - Customize Error Response: Yes
     - Response Page Path: `/index.html`
     - HTTP Response Code: 200
   - Repeat for 404 error

5. **Request SSL Certificate** (Optional - for custom domain):
   - Use AWS Certificate Manager (ACM)
   - Request certificate in `us-east-1` region (required for CloudFront)
   - Add your domain name
   - Validate via DNS or Email

6. **Deploy and Test**:
   - Wait 15-20 minutes for distribution to deploy
   - Access via CloudFront URL: `https://d1234567890.cloudfront.net`
   - Test microphone permission

#### Estimated Time: 30 minutes
#### Cost: Free (CloudFront free tier: 1TB data transfer/month)

---

### Option 2: Deploy to Netlify (Fastest)

Netlify provides automatic HTTPS and is optimized for React apps.

#### Steps:

1. **Install Netlify CLI**:
```bash
npm install -g netlify-cli
```

2. **Deploy from Frontend Directory**:
```bash
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

3. **Follow Prompts**:
   - Authorize Netlify account
   - Create new site or link existing
   - Confirm deployment

4. **Access HTTPS URL**:
   - Netlify provides: `https://your-site-name.netlify.app`
   - Custom domain available (optional)

#### Estimated Time: 5 minutes
#### Cost: Free

---

### Option 3: Deploy to Vercel (Alternative)

Similar to Netlify, optimized for frontend frameworks.

#### Steps:

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Deploy**:
```bash
cd frontend
vercel --prod
```

3. **Follow Prompts**:
   - Authorize Vercel account
   - Configure project settings
   - Confirm deployment

#### Estimated Time: 5 minutes
#### Cost: Free

---

### Option 4: Use AWS Amplify

AWS-native solution with automatic HTTPS.

#### Steps:

1. **Go to AWS Amplify Console**
2. **Create New App** → Host Web App
3. **Deploy without Git**:
   - Upload your `frontend/dist` folder as ZIP
   - Or connect GitHub repository for CI/CD

4. **Configure Build Settings**:
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: dist
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

5. **Access HTTPS URL**:
   - Amplify provides: `https://main.d1234567890.amplifyapp.com`

#### Estimated Time: 15 minutes
#### Cost: Free tier available

---

## Quick Fix for Testing (Development Only)

If you need to test immediately without redeploying:

### Use localhost with HTTPS

1. **Generate Self-Signed Certificate**:
```bash
cd frontend
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

2. **Update vite.config.ts**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'

export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync('./key.pem'),
      cert: fs.readFileSync('./cert.pem'),
    },
    host: true,
    port: 5173,
  },
})
```

3. **Run Dev Server**:
```bash
npm run dev
```

4. **Access**: `https://localhost:5173`
   - Browser will warn about self-signed certificate
   - Click "Advanced" → "Proceed to localhost"

**Note**: This only works for local testing, not for production deployment.

---

## Recommended Approach

For your hackathon submission, I recommend:

1. **Immediate**: Deploy to Netlify (5 minutes, automatic HTTPS)
2. **Production**: Set up CloudFront (better AWS integration, custom domain support)

---

## After Deploying with HTTPS

Update your frontend environment variables:

```bash
# frontend/.env
VITE_API_BASE_URL=https://your-api-gateway-url.amazonaws.com/prod
VITE_ENABLE_DEMO_MODE=true
```

Rebuild and redeploy:
```bash
npm run build
# Then deploy to your chosen platform
```

---

## Testing Microphone Access

After deploying with HTTPS:

1. Open your HTTPS URL
2. Navigate to Voice Transaction page
3. Click the microphone button
4. Browser will prompt: "Allow microphone access?"
5. Click "Allow"
6. Microphone should now work

---

## Browser Compatibility

| Browser | HTTP Microphone | HTTPS Microphone |
|---------|----------------|------------------|
| Chrome  | ❌ Blocked     | ✅ Allowed       |
| Firefox | ❌ Blocked     | ✅ Allowed       |
| Safari  | ❌ Blocked     | ✅ Allowed       |
| Edge    | ❌ Blocked     | ✅ Allowed       |

**Exception**: `localhost` is treated as secure context even on HTTP.

---

## Need Help?

If you encounter issues:
1. Check browser console for specific error messages
2. Verify HTTPS is working (look for padlock icon in address bar)
3. Try in incognito/private mode to rule out extension conflicts
4. Check browser permissions: Settings → Privacy → Microphone
