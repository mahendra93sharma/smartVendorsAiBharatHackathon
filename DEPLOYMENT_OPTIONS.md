# Smart Vendors - Quick Deployment Options

## 🚀 Option 1: Vercel (Recommended - Fastest)

**Time:** 5 minutes  
**Cost:** Free  
**Best for:** Frontend prototype URL

### Steps:

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd frontend
   vercel --prod
   ```

4. **Your URL will be:** `https://smart-vendors-xxx.vercel.app`

### Configuration:
- ✅ `vercel.json` already created
- ✅ Frontend will work in demo mode
- ✅ All features functional (using mock data)

---

## 🌐 Option 2: Netlify

**Time:** 5 minutes  
**Cost:** Free  
**Best for:** Static site hosting

### Steps:

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login:**
   ```bash
   netlify login
   ```

3. **Deploy:**
   ```bash
   cd frontend
   npm run build
   netlify deploy --prod --dir=dist
   ```

4. **Your URL will be:** `https://smart-vendors-xxx.netlify.app`

---

## 📦 Option 3: GitHub Pages

**Time:** 10 minutes  
**Cost:** Free  
**Best for:** GitHub integration

### Steps:

1. **Update package.json:**
   Add to frontend/package.json:
   ```json
   "homepage": "https://YOUR_USERNAME.github.io/smart-vendors"
   ```

2. **Install gh-pages:**
   ```bash
   cd frontend
   npm install --save-dev gh-pages
   ```

3. **Add deploy script to package.json:**
   ```json
   "scripts": {
     "predeploy": "npm run build",
     "deploy": "gh-pages -d dist"
   }
   ```

4. **Deploy:**
   ```bash
   npm run deploy
   ```

5. **Your URL will be:** `https://YOUR_USERNAME.github.io/smart-vendors`

---

## ☁️ Option 4: AWS Amplify (Full AWS Integration)

**Time:** 15 minutes  
**Cost:** Free tier available  
**Best for:** AWS ecosystem

### Steps:

1. **Install AWS Amplify CLI:**
   ```bash
   npm install -g @aws-amplify/cli
   ```

2. **Configure:**
   ```bash
   amplify configure
   ```

3. **Initialize:**
   ```bash
   cd frontend
   amplify init
   ```

4. **Add hosting:**
   ```bash
   amplify add hosting
   ```

5. **Deploy:**
   ```bash
   amplify publish
   ```

6. **Your URL will be:** `https://xxx.amplifyapp.com`

---

## 🐳 Option 5: Railway

**Time:** 10 minutes  
**Cost:** Free tier available  
**Best for:** Full-stack deployment

### Steps:

1. **Go to:** https://railway.app

2. **Connect GitHub repo**

3. **Configure build:**
   - Build Command: `cd frontend && npm install && npm run build`
   - Start Command: `npx serve -s frontend/dist -l 3000`

4. **Deploy**

5. **Your URL will be:** `https://smart-vendors-xxx.railway.app`

---

## 🎯 Recommended: Vercel (Fastest)

For hackathon submission, I recommend **Vercel** because:
- ✅ Fastest deployment (5 minutes)
- ✅ Free forever
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Perfect for React/Vite apps
- ✅ No credit card required

---

## 📝 Quick Start with Vercel

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login (opens browser)
vercel login

# 3. Deploy from frontend directory
cd frontend
vercel --prod

# 4. Follow prompts:
#    - Set up and deploy? Yes
#    - Which scope? Your account
#    - Link to existing project? No
#    - Project name? smart-vendors
#    - Directory? ./
#    - Override settings? No

# 5. Done! You'll get a URL like:
# https://smart-vendors-xxx.vercel.app
```

---

## 🔧 Environment Variables

For any deployment, set these environment variables:

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_ENABLE_DEMO_MODE=true
VITE_ENABLE_OFFLINE_MODE=true
VITE_AWS_REGION=ap-south-1
```

**Note:** Demo mode works without backend, so you can deploy frontend only!

---

## ✅ After Deployment

1. **Test your URL:**
   - Open in browser
   - Test all features
   - Verify demo mode works

2. **Update submission:**
   - Add URL to SUBMISSION_CHECKLIST.md
   - Test from different devices
   - Share with team

3. **Monitor:**
   - Check deployment logs
   - Monitor performance
   - Fix any issues

---

## 🆘 Troubleshooting

### Build fails:
```bash
# Clear cache and rebuild
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

### Environment variables not working:
- Vercel: Add in dashboard under Settings > Environment Variables
- Netlify: Add in dashboard under Site settings > Environment variables

### 404 errors:
- Add `_redirects` file to `frontend/public/`:
  ```
  /*    /index.html   200
  ```

---

## 📊 Comparison

| Platform | Time | Cost | Ease | Features |
|----------|------|------|------|----------|
| Vercel | 5 min | Free | ⭐⭐⭐⭐⭐ | Best for React |
| Netlify | 5 min | Free | ⭐⭐⭐⭐⭐ | Great for static |
| GitHub Pages | 10 min | Free | ⭐⭐⭐⭐ | GitHub integration |
| AWS Amplify | 15 min | Free tier | ⭐⭐⭐ | Full AWS stack |
| Railway | 10 min | Free tier | ⭐⭐⭐⭐ | Full-stack |

---

## 🎉 Next Steps

After deployment:
1. ✅ Get your prototype URL
2. ✅ Test all features
3. ✅ Add URL to submission
4. ✅ Create demo video
5. ✅ Submit to hackathon!

---

**Need help?** Check the platform-specific documentation or ask for assistance!
