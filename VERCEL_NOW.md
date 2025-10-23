# 🎯 Vercel Deployment - Quick Start Guide

## ✅ Code is Ready and Pushed to GitHub!

Your code has been successfully pushed to:
**https://github.com/venkyok/book-my-seat**

---

## 🚀 Deploy Now (3 Minutes)

### Step 1: Go to Vercel Dashboard
👉 **Open:** https://vercel.com/dashboard

### Step 2: Sign In with GitHub
- Click "Continue with GitHub"
- Authorize Vercel if prompted

### Step 3: Import Your Repository

1. Click **"Add New..."** (top right)
2. Select **"Project"**
3. Click **"Import Git Repository"**
4. Find and select: **`venkyok/book-my-seat`**
5. Click **"Import"**

### Step 4: Configure Project

**Framework Preset:** Select "Other"

**Root Directory:** `./` (leave as default)

**Build Command:** (leave empty - uses build_files.sh automatically)

**Install Command:** (leave empty - uses pip install automatically)

**Output Directory:** (leave empty)

### Step 5: Add Environment Variables ⚠️ IMPORTANT

Click **"Environment Variables"** section and add these:

#### Variable 1: SECRET_KEY
```
Name: SECRET_KEY
Value: django-insecure-c8aetlj(=vp90n@#yoc^&d(_6ivp(d!bv-4-f!r$lawptjzrwu
```
*For production, generate a secure one:*
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Variable 2: DEBUG
```
Name: DEBUG
Value: False
```

#### Variable 3: ALLOWED_HOSTS (Optional - already configured)
```
Name: ALLOWED_HOSTS
Value: .vercel.app,.now.sh
```

### Step 6: Deploy! 🚀

1. Click **"Deploy"** button
2. Wait 2-3 minutes for build
3. Watch the build logs
4. ✅ When complete, you'll see: **"Your project is ready!"**

### Step 7: Visit Your Live Site

Your app will be live at:
```
https://book-my-seat.vercel.app
```
or
```
https://book-my-seat-<random>.vercel.app
```

---

## 🎯 Quick Test Checklist

After deployment, test these URLs:

```
✅ Homepage:
   https://your-project.vercel.app/

✅ Movies Page:
   https://your-project.vercel.app/movies/

✅ Admin Panel:
   https://your-project.vercel.app/admin/

✅ Register:
   https://your-project.vercel.app/register/

✅ Login:
   https://your-project.vercel.app/login/
```

---

## ⚠️ Expected Behavior (SQLite Demo)

### What Will Work:
✅ All pages load correctly  
✅ Templates render with Bootstrap styling  
✅ Navigation works  
✅ Static files (CSS/JS) load  
✅ Forms display correctly  

### What Won't Work (Database Resets):
❌ Movie list will be empty (no data persists)  
❌ Admin panel has no superuser (cannot login)  
❌ User registration works but users don't persist  
❌ Bookings don't save permanently  
❌ Database resets on every deployment  

**This is normal for SQLite on Vercel!** For real data persistence, use Render.com with PostgreSQL.

---

## 🐛 Troubleshooting

### Build Failed?

**Check Build Logs:**
- Look for red error messages
- Common issues: Missing dependencies

**Solution:**
```bash
# Test locally first
python manage.py check
python manage.py collectstatic --noinput

# If errors, fix and push again
git add .
git commit -m "Fix build errors"
git push origin main
# Vercel auto-redeploys
```

### 500 Error After Deployment?

**Check Function Logs:**
1. Go to Vercel Dashboard → Your Project
2. Click "Functions" tab
3. Look at real-time logs

**Common causes:**
- Missing SECRET_KEY environment variable
- Import errors
- Static files issues

**Quick Fix:**
- Go to Settings → Environment Variables
- Make sure SECRET_KEY is set
- Click "Redeploy" button

### Static Files Not Loading?

**Solution:**
1. Check build logs for "collectstatic" success
2. Ensure WhiteNoise is in MIDDLEWARE (it is)
3. Try redeploying: Deployments → Latest → "Redeploy"

---

## 🎨 Customize Your Domain

### Default Domain:
```
https://book-my-seat-<random>.vercel.app
```

### Custom Vercel Domain (Free):
1. Go to Settings → Domains
2. Click "Edit" on default domain
3. Change to: `your-custom-name.vercel.app`
4. Save

### Your Own Domain (Advanced):
1. Buy domain (e.g., from Namecheap, GoDaddy)
2. Go to Settings → Domains
3. Add your domain: `yourdomain.com`
4. Follow DNS configuration instructions

---

## 🔄 Automatic Deployments

Every time you push to GitHub, Vercel automatically redeploys:

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Vercel automatically:
# 1. Detects the push
# 2. Builds the project
# 3. Deploys updates
# 4. Live in ~2 minutes!
```

---

## 📊 Monitor Your Deployment

### Analytics (Free)
- Go to Analytics tab
- See page views, visitors, performance

### Function Logs (Real-time)
- Go to Functions tab
- Watch Django requests in real-time
- Useful for debugging

### Deployment History
- Go to Deployments tab
- See all previous deployments
- Rollback to any previous version

---

## 💡 Pro Tips

### 1. Preview Deployments
Every branch gets its own preview URL:
```bash
git checkout -b feature-branch
git push origin feature-branch
# Get a unique preview URL for testing
```

### 2. Environment Variables per Environment
- Production: Used for main branch
- Preview: Used for other branches
- Development: Local only

### 3. Instant Rollback
If deployment breaks:
1. Go to Deployments
2. Find last working deployment
3. Click "..." → "Promote to Production"

---

## 🎯 Next Steps

### Option A: Keep SQLite Demo
- Perfect for portfolio showcase
- Add note: "Demo version - data resets"
- Consider adding screenshots of functionality

### Option B: Upgrade to PostgreSQL
For real production app with persistent data:
1. Follow `DEPLOY_TO_RENDER_NOW.md` instead
2. Get PostgreSQL database included
3. Full functionality with data persistence

---

## 📞 Need Help?

**Vercel Documentation:**
- https://vercel.com/docs

**Django on Vercel Guide:**
- https://vercel.com/guides/deploying-django-with-vercel

**Vercel Support:**
- https://vercel.com/support

**Your GitHub Repo:**
- https://github.com/venkyok/book-my-seat

---

## ✅ Deployment Checklist

- [x] Code pushed to GitHub ✅
- [ ] Vercel account created
- [ ] Project imported from GitHub
- [ ] Environment variables added (SECRET_KEY, DEBUG)
- [ ] Deployment successful
- [ ] Site is live and accessible
- [ ] All pages load correctly
- [ ] Static files working

---

**Ready? Go deploy! 🚀**

**Vercel Dashboard:** https://vercel.com/dashboard
