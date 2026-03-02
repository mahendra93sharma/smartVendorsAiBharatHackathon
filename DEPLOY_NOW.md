# 🚀 Deploy Smart Vendors NOW - Get Your Prototype URL

## ⚡ Fastest Option: Vercel (5 minutes)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Run Deployment Script
```bash
chmod +x deploy-vercel.sh
./deploy-vercel.sh
```

### Step 3: Follow Prompts
- Login to Vercel (browser opens)
- Confirm project settings
- Wait for deployment

### Step 4: Get Your URL
You'll receive a URL like: `https://smart-vendors-xxx.vercel.app`

---

## 🎯 Alternative: Netlify (5 minutes)

### Step 1: Install Netlify CLI
```bash
npm install -g netlify-cli
```

### Step 2: Run Deployment Script
```bash
chmod +x deploy-netlify.sh
./deploy-netlify.sh
```

### Step 3: Follow Prompts
- Login to Netlify (browser opens)
- Confirm deployment
- Wait for build

### Step 4: Get Your URL
You'll receive a URL like: `https://smart-vendors-xxx.netlify.app`

---

## 📱 Manual Deployment (If scripts don't work)

### Option A: Vercel Manual

1. **Go to:** https://vercel.com
2. **Sign up/Login** with GitHub
3. **Click:** "Add New Project"
4. **Import** your GitHub repository
5. **Configure:**
   - Framework Preset: Vite
   - Root Directory: frontend
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. **Add Environment Variables:**
   ```
   VITE_API_BASE_URL=http://localhost:8000
   VITE_ENABLE_DEMO_MODE=true
   VITE_ENABLE_OFFLINE_MODE=true
   ```
7. **Click:** "Deploy"
8. **Wait** 2-3 minutes
9. **Get URL** from dashboard

### Option B: Netlify Manual

1. **Go to:** https://netlify.com
2. **Sign up/Login** with GitHub
3. **Click:** "Add new site" → "Import an existing project"
4. **Connect** to GitHub
5. **Select** your repository
6. **Configure:**
   - Base directory: frontend
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
7. **Add Environment Variables:**
   ```
   VITE_API_BASE_URL=http://localhost:8000
   VITE_ENABLE_DEMO_MODE=true
   VITE_ENABLE_OFFLINE_MODE=true
   ```
8. **Click:** "Deploy site"
9. **Wait** 2-3 minutes
10. **Get URL** from dashboard

---

## 🐙 Option C: GitHub Pages (10 minutes)

### Step 1: Update package.json
Add to `frontend/package.json`:
```json
{
  "homepage": "https://YOUR_GITHUB_USERNAME.github.io/smart-vendors",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

### Step 2: Install gh-pages
```bash
cd frontend
npm install --save-dev gh-pages
```

### Step 3: Deploy
```bash
npm run deploy
```

### Step 4: Enable GitHub Pages
1. Go to your GitHub repository
2. Settings → Pages
3. Source: gh-pages branch
4. Save

### Step 5: Get URL
`https://YOUR_GITHUB_USERNAME.github.io/smart-vendors`

---

## ✅ After Deployment Checklist

### 1. Test Your Prototype
- [ ] Open the URL in browser
- [ ] Test home page loads
- [ ] Try voice transaction (demo mode)
- [ ] Check price intelligence
- [ ] Test freshness scanner
- [ ] Try marketplace
- [ ] View trust score
- [ ] Test on mobile device

### 2. Verify Demo Mode
- [ ] Demo mode toggle works
- [ ] Pre-recorded samples play
- [ ] Mock data displays
- [ ] No API errors in console

### 3. Update Documentation
- [ ] Add URL to `SUBMISSION_CHECKLIST.md`
- [ ] Update `README.md` with live demo link
- [ ] Test URL from different networks

### 4. Share
- [ ] Share URL with team
- [ ] Test from different devices
- [ ] Get feedback

---

## 🆘 Troubleshooting

### Build Fails
```bash
cd frontend
rm -rf node_modules dist .vite
npm install
npm run build
```

### Blank Page After Deployment
1. Check browser console for errors
2. Verify environment variables are set
3. Check `_redirects` file exists in `public/`

### 404 Errors
Add `frontend/public/_redirects`:
```
/*    /index.html   200
```

### Environment Variables Not Working
- Vercel: Dashboard → Settings → Environment Variables
- Netlify: Site settings → Environment variables
- Redeploy after adding variables

---

## 📊 Deployment Comparison

| Platform | Time | Difficulty | URL Format |
|----------|------|------------|------------|
| Vercel | 5 min | ⭐ Easy | smart-vendors-xxx.vercel.app |
| Netlify | 5 min | ⭐ Easy | smart-vendors-xxx.netlify.app |
| GitHub Pages | 10 min | ⭐⭐ Medium | username.github.io/smart-vendors |

---

## 🎬 Quick Start Commands

### Vercel (Recommended)
```bash
npm install -g vercel
cd frontend
vercel --prod
```

### Netlify
```bash
npm install -g netlify-cli
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

### GitHub Pages
```bash
cd frontend
npm install --save-dev gh-pages
npm run deploy
```

---

## 💡 Pro Tips

1. **Use Demo Mode:** Your frontend works perfectly without backend
2. **Test Mobile:** Use Chrome DevTools mobile emulation
3. **Check Performance:** Use Lighthouse in Chrome DevTools
4. **Monitor:** Check deployment logs if issues occur
5. **Update:** Redeploy anytime with same command

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ Public prototype URL
- ✅ HTTPS enabled
- ✅ Global CDN
- ✅ Automatic deployments (if connected to Git)
- ✅ Free hosting

**Your prototype is ready for hackathon submission!**

---

## 📞 Need Help?

1. Check deployment logs in platform dashboard
2. Review `DEPLOYMENT_OPTIONS.md` for detailed guides
3. Test locally first: `cd frontend && npm run dev`
4. Verify build works: `cd frontend && npm run build`

---

## 🚀 Deploy Now!

Choose your platform and run the command:

```bash
# Vercel (Fastest)
./deploy-vercel.sh

# OR Netlify
./deploy-netlify.sh

# OR Manual via web dashboard
```

**Get your prototype URL in 5 minutes!** 🎯
