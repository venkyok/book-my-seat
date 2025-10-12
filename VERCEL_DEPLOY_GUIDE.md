# 🚀 Deploy to Vercel - Step by Step Guide

## ⚠️ Important: Vercel Limitations for Django

Before deploying to Vercel, understand these limitations:

- ❌ **No SQLite persistence** - Need external PostgreSQL database
- ❌ **No media file persistence** - Need cloud storage (Cloudinary/S3)
- ❌ **10-second execution limit** - Serverless function timeout
- ❌ **No background tasks** - Need external cron service
- ❌ **Cold starts** - First request may be slow

**Alternative:** Render.com is much easier for Django (see RENDER_DEPLOYMENT_FIXED.md)

---

## ✅ Prerequisites

1. **GitHub Account** - Your code is already pushed to: https://github.com/venkyok/book-my-seat
2. **Vercel Account** - Sign up at https://vercel.com
3. **External Database** - Neon or ElephantSQL (free tier available)
4. **Cloud Storage** (optional) - Cloudinary for media files

---

## Step 1: Create External PostgreSQL Database

### Option A: Neon.tech (Recommended - Free, Modern)

1. Go to **https://neon.tech**
2. Sign up with GitHub
3. Click **"Create Project"**
4. Configure:
   - **Project Name**: `bookmyseat`
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 16
5. Click **"Create Project"**
6. **Copy the connection string** - looks like:
   ```
   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
7. **Save this** - you'll need it for environment variables!

### Option B: ElephantSQL (Alternative)

1. Go to **https://www.elephantsql.com**
2. Sign up and create new instance
3. Plan: **Tiny Turtle (Free)**
4. Copy the **URL** from instance details

---

## Step 2: Deploy to Vercel

### Using Vercel Dashboard (Easiest)

1. **Go to Vercel:** https://vercel.com
2. **Sign in** with GitHub
3. Click **"Add New..."** → **"Project"**
4. **Import** your repository: `venkyok/book-my-seat`
5. **Configure Project:**
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: Leave default or use `./build_files.sh`
   - **Output Directory**: Leave empty
6. **Don't click Deploy yet!** - Need to add environment variables first

---

## Step 3: Add Environment Variables in Vercel

**CRITICAL:** Add these before deploying!

Click **"Environment Variables"** and add:

### Required Variables:

| Variable | Value | How to Get |
|----------|-------|------------|
| `SECRET_KEY` | `your-secret-key-here` | Generate below ⬇️ |
| `DEBUG` | `False` | Type as-is |
| `DATABASE_URL` | `postgresql://...` | From Neon (Step 1) |
| `ALLOWED_HOSTS` | `.vercel.app` | Type as-is |

### Optional (Payment Gateway):

| Variable | Value |
|----------|-------|
| `RAZORPAY_KEY_ID` | Your Razorpay key |
| `RAZORPAY_KEY_SECRET` | Your Razorpay secret |
| `STRIPE_PUBLIC_KEY` | Your Stripe key (optional) |
| `STRIPE_SECRET_KEY` | Your Stripe secret (optional) |

### Generate SECRET_KEY:

Run this locally in PowerShell:
```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste as `SECRET_KEY` value.

---

## Step 4: Deploy!

1. After adding all environment variables
2. Click **"Deploy"**
3. Wait 2-5 minutes for build
4. You'll get a URL like: `https://book-my-seat-xxx.vercel.app`

---

## Step 5: Run Migrations

**IMPORTANT:** Vercel doesn't run migrations automatically!

### Method A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```powershell
   npm install -g vercel
   ```

2. **Login:**
   ```powershell
   vercel login
   ```

3. **Pull environment variables:**
   ```powershell
   cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
   vercel env pull .env.production
   ```

4. **Run migrations locally against production database:**
   ```powershell
   # Load production DATABASE_URL
   $env:DATABASE_URL = "your-neon-database-url-here"
   python manage.py migrate
   ```

### Method B: Using Database Client

1. Install **pgAdmin** or **DBeaver**
2. Connect to your Neon database
3. Run migrations using SQL client

---

## Step 6: Create Superuser

You need to create an admin user to access `/admin/`

**Using Vercel CLI:**
```powershell
# Set DATABASE_URL environment variable
$env:DATABASE_URL = "your-neon-database-url-here"

# Create superuser
python manage.py createsuperuser
```

Follow prompts to create admin account.

---

## Step 7: Configure Media Files (Important!)

Vercel **doesn't store uploaded files**. You need cloud storage.

### Setup Cloudinary (Recommended - Free Tier)

1. **Sign up:** https://cloudinary.com
2. **Get credentials** from dashboard
3. **Install package locally:**
   ```powershell
   pip install cloudinary django-cloudinary-storage
   ```

4. **Update requirements.txt:**
   ```powershell
   pip freeze > requirements.txt
   ```

5. **Add to settings.py** (at the end):
   ```python
   # Cloudinary Configuration
   import cloudinary
   import cloudinary.uploader
   import cloudinary.api
   
   CLOUDINARY_STORAGE = {
       'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
       'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
       'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET')
   }
   
   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

6. **Add to Vercel Environment Variables:**
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`

7. **Commit and push:**
   ```powershell
   git add .
   git commit -m "Add Cloudinary for media storage"
   git push origin main
   ```

Vercel will auto-deploy!

---

## Step 8: Setup Seat Cleanup (Cron Job)

Vercel has limited cron support. Use external service:

### Option A: Cron-job.org (Free)

1. Go to **https://cron-job.org**
2. Create free account
3. Add new cron job:
   - **URL**: `https://your-app.vercel.app/cleanup-reservations/`
   - **Schedule**: `*/5 * * * *` (every 5 minutes)
   - **Enable**: Yes

### Option B: Vercel Cron (Limited)

Add to `vercel.json`:
```json
{
  "crons": [{
    "path": "/api/cleanup",
    "schedule": "*/5 * * * *"
  }]
}
```

---

## 🎯 Testing Your Deployment

### 1. Check Homepage
Visit: `https://your-app.vercel.app`

### 2. Check Admin Panel
Visit: `https://your-app.vercel.app/admin/`
Login with superuser credentials

### 3. Add Sample Data
- Add Movies (with posters from URLs)
- Add Theaters
- Add Seats

### 4. Test Booking Flow
- Select movie → theater → seats
- Try payment (test mode)
- Check email confirmation

---

## 🔍 Troubleshooting

### Build Failed

**Check Vercel Build Logs:**
1. Go to Vercel Dashboard
2. Click your project
3. Go to "Deployments"
4. Click failed deployment
5. Check logs

**Common issues:**
- Missing environment variables
- Python version mismatch
- Dependency installation failed

**Solution:**
```powershell
# Update requirements.txt if needed
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Database Connection Failed

**Check:**
- DATABASE_URL is correct (from Neon dashboard)
- DATABASE_URL includes `?sslmode=require` at the end
- Neon database is active (free tier sleeps after inactivity)

**Fix:**
1. Go to Neon dashboard
2. Click your project
3. Copy connection string again
4. Update in Vercel environment variables
5. Redeploy

### Static Files Not Loading

**Check:**
1. Build logs show "Collecting static files"
2. `STATIC_ROOT` is set in settings.py
3. WhiteNoise is installed

**Fix:**
```powershell
# Ensure WhiteNoise is in requirements
pip install whitenoise
pip freeze > requirements.txt
git add .
git commit -m "Fix static files"
git push origin main
```

### 500 Internal Server Error

**Check Vercel Function Logs:**
1. Go to Vercel Dashboard
2. Click "Functions" tab
3. View error logs

**Common causes:**
- Missing SECRET_KEY
- Database not accessible
- Missing migrations

### Media Files Not Uploading

**Vercel doesn't support file uploads!**

**Solution:**
- Setup Cloudinary (see Step 7)
- Or use AWS S3
- Or for admin only: use external URLs for movie posters

---

## 📊 Vercel Free Tier Limits

| Feature | Limit |
|---------|-------|
| Bandwidth | 100 GB/month |
| Function Execution | 100 GB-hours |
| Function Duration | 10 seconds max |
| Build Minutes | 6000 min/month |
| Deployments | Unlimited |

**Note:** Free tier is sufficient for testing and small projects.

---

## 🔄 Updating Your App

To deploy updates:

```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"

# Make your changes...

git add .
git commit -m "Your update message"
git push origin main
```

Vercel automatically detects the push and redeploys! ⚡

---

## 🎯 Production Checklist

Before going live:

- [ ] DATABASE_URL configured (Neon/ElephantSQL)
- [ ] SECRET_KEY generated and set
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS includes your domain
- [ ] Migrations run on production database
- [ ] Superuser created
- [ ] Cloudinary configured for media files
- [ ] Cron job setup for seat cleanup
- [ ] Payment gateway keys (live mode) set
- [ ] Email service configured (SendGrid/Mailgun)
- [ ] Domain name connected (optional)
- [ ] SSL enabled (automatic on Vercel)

---

## 🌐 Add Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings
2. Click "Domains"
3. Add your domain (e.g., `bookmyseat.com`)
4. Update DNS records as shown
5. Update `ALLOWED_HOSTS` in environment variables:
   ```
   ALLOWED_HOSTS=.vercel.app,bookmyseat.com,www.bookmyseat.com
   ```

---

## 📚 Useful Commands

### Vercel CLI Commands:
```powershell
# Deploy from command line
vercel --prod

# View logs
vercel logs

# View environment variables
vercel env ls

# Add environment variable
vercel env add SECRET_KEY

# Pull environment to local
vercel env pull .env.local
```

### Django Management Commands:
```powershell
# With production DATABASE_URL set
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
python manage.py cleanup_reservations
```

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Neon Docs**: https://neon.tech/docs
- **Cloudinary Docs**: https://cloudinary.com/documentation
- **Django Deployment**: https://docs.djangoproject.com/en/5.1/howto/deployment/

---

## 💡 Pro Tips

1. **Use Neon's Free Tier** - 0.5GB storage, auto-sleeps after inactivity
2. **Monitor Vercel Usage** - Check dashboard regularly
3. **Setup Error Tracking** - Use Sentry.io for production
4. **Enable CDN** - Vercel has global CDN built-in
5. **Use Environment Variable Groups** - Group by environment (dev/prod)

---

## ✅ Quick Start Commands

```powershell
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
vercel --prod

# 4. Run migrations (with DATABASE_URL from Neon)
$env:DATABASE_URL = "your-neon-url"
python manage.py migrate
python manage.py createsuperuser
```

---

**Your app is ready for Vercel deployment!** 🚀

All configuration files are already in place:
- ✅ `vercel.json` - Deployment configuration
- ✅ `build_files.sh` - Build script
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Git ignore patterns
- ✅ `requirements.txt` - Dependencies

Just follow Steps 1-8 above! 🎉
