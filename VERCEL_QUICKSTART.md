# 🚀 Vercel Quick Deploy - 5 Steps

## Before You Start

**⚠️ Important:** Vercel requires an external PostgreSQL database. Django with Vercel has limitations.

**Easier Alternative:** Use Render.com (see RENDER_URGENT_FIX.md) - it includes database, storage, and is designed for Django!

---

## Step 1: Create Database (5 minutes)

### Go to Neon.tech (Free PostgreSQL)

1. Visit: **https://neon.tech**
2. Sign up with GitHub
3. Create project: "bookmyseat"
4. **Copy the connection string** (looks like):
   ```
   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
5. **Save this!** You'll need it in Step 3

---

## Step 2: Deploy to Vercel (2 minutes)

1. Visit: **https://vercel.com**
2. Sign in with GitHub
3. Click **"Add New..."** → **"Project"**
4. Import: **`venkyok/book-my-seat`**
5. **STOP! Don't deploy yet** - Add environment variables first ⬇️

---

## Step 3: Add Environment Variables (3 minutes)

**In Vercel project settings, add these:**

### Generate SECRET_KEY First:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Required Variables:

| Name | Value |
|------|-------|
| `SECRET_KEY` | Output from command above |
| `DEBUG` | `False` |
| `DATABASE_URL` | Your Neon connection string from Step 1 |
| `ALLOWED_HOSTS` | `.vercel.app` |

### Optional (Payment):

| Name | Value |
|------|-------|
| `RAZORPAY_KEY_ID` | Your test key |
| `RAZORPAY_KEY_SECRET` | Your test secret |

---

## Step 4: Deploy! (5 minutes)

1. Click **"Deploy"** in Vercel
2. Wait for build to complete
3. You'll get URL: `https://book-my-seat-xxx.vercel.app`

---

## Step 5: Setup Database (5 minutes)

### Install Vercel CLI:
```powershell
npm install -g vercel
```

### Login:
```powershell
vercel login
```

### Run Migrations:
```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"

# Set your Neon database URL
$env:DATABASE_URL = "postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## ✅ Done! Test Your App

1. **Visit your app:** `https://your-app.vercel.app`
2. **Login to admin:** `https://your-app.vercel.app/admin`
3. **Add movies, theaters, seats** through admin panel

---

## 🎯 Important Next Steps

### Media Files Don't Persist on Vercel!

You need Cloudinary for movie posters:

1. Sign up: https://cloudinary.com (free tier)
2. Get credentials from dashboard
3. Add to Vercel environment variables:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`

**OR** use external URLs for movie posters (easier for testing)

### Setup Seat Cleanup Cron Job

1. Go to: https://cron-job.org
2. Create free account
3. Add cron job:
   - URL: `https://your-app.vercel.app/cleanup-reservations/`
   - Schedule: Every 5 minutes (`*/5 * * * *`)

---

## 🔍 Troubleshooting

### Build Failed?
- Check build logs in Vercel dashboard
- Verify all environment variables are set
- Check Python version is 3.11

### Database Connection Error?
- Ensure DATABASE_URL includes `?sslmode=require`
- Check Neon database is active (wake it up if sleeping)
- Verify DATABASE_URL is correct

### 500 Error?
- Check Vercel function logs
- Ensure migrations were run
- Verify SECRET_KEY is set

### Static Files Not Loading?
- Check build logs show "Collecting static files"
- Wait for build to complete fully

---

## 📚 Full Documentation

For detailed instructions, see:
- **`VERCEL_DEPLOY_GUIDE.md`** - Complete step-by-step guide
- **`VERCEL_QUICK_START.md`** - Quick start with Render comparison

---

## 🆘 Vercel Not Working?

**Switch to Render** (much easier for Django):

See **`RENDER_URGENT_FIX.md`** for:
- Built-in PostgreSQL (no external database needed)
- Persistent file storage
- Native cron jobs
- Simpler deployment

---

## 💡 Quick Commands

```powershell
# Deploy updates
git add .
git commit -m "Update"
git push origin main
# Vercel auto-deploys!

# View logs
vercel logs

# Run migrations on production DB
$env:DATABASE_URL = "your-neon-url"
python manage.py migrate
```

---

**Ready to deploy to Vercel!** 🚀

All files are configured and pushed to GitHub.

**Your GitHub Repo:** https://github.com/venkyok/book-my-seat
