# 🚀 Deploy to Netlify with HTTPS - Fix Microphone Issue

## Quick Deploy (5 minutes)

Your frontend is already built! Just run these commands:

### Step 1: Deploy to Netlify

```bash
cd frontend
netlify deploy --prod --dir=dist
```

### Step 2: Follow the Prompts

When prompted:

1. **"This folder isn't linked to a site yet"**
   - Choose: `+ Create & configure a new site`

2. **"Team:"**
   - Select your team or press Enter for default

3. **"Site name (leave blank for random name):"**
   - Type: `smart-vendors` (or leave blank for random)
   - Press Enter

4. **"Authorize with Netlify"**
   - A browser window will open
   - Click "Authorize" to connect Netlify CLI
   - Return to terminal

5. **Deployment will start automatically**
   - Wait for upload to complete (~30 seconds)

### Step 3: Get Your HTTPS URL

After deployment completes, you'll see:

```
✔ Deployed to production site URL:
  https://smart-vendors.netlify.app
```

**Copy this URL!** This is your new HTTPS frontend URL.

---

## Alternative: Manual Deployment (No CLI)

If you prefer not to use CLI:

### Option A: Drag & Drop

1. Go to [app.netlify.com](https://app.netlify.com)
2. Sign up/Login (free account)
3. Drag the `frontend/dist` folder onto the page
4. Wait for deployment
5. Get your HTTPS URL

### Option B: GitHub Integration

1. Push your code to GitHub
2. Go to [app.netlify.com](https://app.netlify.com)
3. Click "Add new site" → "Import an existing project"
4. Connect GitHub
5. Select your repository
6. Build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
7. Click "Deploy site"

---

## After Deployment

### 1. Test Microphone

1. Open your new HTTPS URL
2. Navigate to Voice Transaction
3. Click the microphone button
4. Browser will ask: "Allow microphone access?"
5. Click "Allow"
6. ✅ Microphone should now work!

### 2. Update Environment Variables (Optional)

If you have a backend API, update Netlify environment variables:

1. Go to Site settings → Environment variables
2. Add:
   - `VITE_API_BASE_URL`: Your API Gateway URL
   - `VITE_ENABLE_DEMO_MODE`: `true`
   - `VITE_AWS_REGION`: `ap-south-1`
3. Redeploy: `netlify deploy --prod --dir=dist`

### 3. Custom Domain (Optional)

To use your own domain:

1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Follow DNS configuration steps

---

## Troubleshooting

### "netlify: command not found"

Install Netlify CLI:
```bash
npm install -g netlify-cli
```

### "This folder isn't linked to a site yet"

This is normal for first deployment. Choose "Create & configure a new site".

### Build folder not found

Rebuild the frontend:
```bash
cd frontend
npm run build
```

### Still getting microphone error

1. Check URL starts with `https://` (not `http://`)
2. Clear browser cache
3. Try in incognito/private mode
4. Check browser permissions: Settings → Privacy → Microphone

---

## Why This Fixes the Issue

| Before (S3) | After (Netlify) |
|-------------|-----------------|
| ❌ HTTP only | ✅ HTTPS enabled |
| ❌ Microphone blocked | ✅ Microphone allowed |
| `http://...s3-website...` | `https://...netlify.app` |

Modern browsers require HTTPS for microphone access. Netlify provides automatic HTTPS with free SSL certificates.

---

## Cost

**FREE!** Netlify free tier includes:
- ✅ Automatic HTTPS
- ✅ 100 GB bandwidth/month
- ✅ Continuous deployment
- ✅ Custom domain support
- ✅ Instant rollbacks

---

## Next Steps

1. ✅ Deploy to Netlify (5 minutes)
2. ✅ Test microphone feature
3. ✅ Update submission with HTTPS URL
4. ✅ Share with hackathon judges

---

## Quick Command Reference

```bash
# Deploy to production
cd frontend
netlify deploy --prod --dir=dist

# Check deployment status
netlify status

# Open site in browser
netlify open:site

# View deployment logs
netlify logs

# Rollback to previous deployment
netlify rollback
```

---

## Your Current Status

- ✅ Frontend built successfully
- ✅ Netlify CLI installed
- ⏳ Ready to deploy
- ⏳ Waiting for HTTPS URL

**Run this now:**
```bash
cd frontend
netlify deploy --prod --dir=dist
```

Then test your microphone! 🎤
