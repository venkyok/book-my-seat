# 🚀 Vercel Deployment Quick Start Guide

## ⚠️ Important Note About Vercel + Django

**Vercel is primarily designed for frontend frameworks (Next.js, React, etc.) and serverless functions.**

For Django applications, you may encounter limitations:
- SQLite doesn't persist (requires external PostgreSQL)
- Media files don't persist (requires cloud storage like Cloudinary/S3)
- Background tasks/cron jobs require external services
- 10-second execution timeout for serverless functions

**Recommended Alternative: [Render.com](https://render.com)** - Better for Django with built-in PostgreSQL, persistent storage, and cron jobs.

---

## Option 1: Deploy to Render.com (Recommended) ✅

Render is much easier for Django applications:

### Step 1: Push to GitHub
```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
git init
git add .
git commit -m "Initial commit for deployment"
```

Create a new repository on GitHub and push:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Sign up at **https://render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `bookmyseat`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn bookmyseat.wsgi:application`

5. Add **Environment Variables**:
   ```
   SECRET_KEY=your-secret-key-here-generate-new-one
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   RAZORPAY_KEY_ID=your_razorpay_key
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   ```

6. Click **"Create Web Service"**

Render will automatically create a PostgreSQL database for you!

---

## Option 2: Deploy to Vercel (Advanced) ⚙️

If you still want to use Vercel, follow these steps:

### Prerequisites

✅ All configuration files are ready:
- `vercel.json` - Deployment configuration
- `build_files.sh` - Build script
- `.gitignore` - Git ignore patterns
- `requirements.txt` - Python dependencies
- Updated `settings.py` with environment variables

### Step 1: Create External Database

Vercel doesn't provide databases. Choose one:

#### Option A: Neon.tech (Recommended - Free Tier)
1. Go to **https://neon.tech**
2. Sign up and create a new project
3. Copy the connection string (looks like):
   ```
   postgresql://user:password@host.neon.tech/database?sslmode=require
   ```

#### Option B: ElephantSQL
1. Go to **https://www.elephantsql.com**
2. Sign up and create a new instance (Tiny Turtle - Free)
3. Copy the URL from the instance details

### Step 2: Push Code to GitHub

```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"

# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for Vercel deployment"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Vercel

1. Go to **https://vercel.com** and sign up
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `chmod +x build_files.sh && ./build_files.sh`
   - **Output Directory**: Leave empty

### Step 4: Add Environment Variables

In Vercel project settings, add these environment variables:

```
SECRET_KEY=django-insecure-GENERATE-NEW-SECRET-KEY-HERE
DEBUG=False
DATABASE_URL=postgresql://user:password@host.neon.tech/database?sslmode=require
ALLOWED_HOSTS=.vercel.app
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

**Generate a new SECRET_KEY**: Run Python locally:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Step 5: Run Migrations

After deployment, run migrations on your database:

**Method A: Use Vercel CLI**
```powershell
npm install -g vercel
vercel login
vercel env pull .env.local
python manage.py migrate
```

**Method B: Use Database Client**
Connect to your Neon/ElephantSQL database and run migrations manually.

### Step 6: Create Superuser

```powershell
python manage.py createsuperuser
```

---

## Post-Deployment Checklist

### 1. Test Your Site
- [ ] Homepage loads
- [ ] Movies list displays
- [ ] Seat selection works
- [ ] Payment page loads
- [ ] Admin panel accessible

### 2. Configure Media Files (Important!)

Vercel doesn't persist uploaded files. Set up cloud storage:

**Option A: Cloudinary (Recommended)**
```powershell
pip install cloudinary django-cloudinary-storage
```

Add to `settings.py`:
```python
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your_cloud_name',
    'API_KEY': 'your_api_key',
    'API_SECRET': 'your_api_secret'
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

**Option B: AWS S3**
```powershell
pip install django-storages boto3
```

### 3. Set Up Seat Cleanup (Important!)

Since Vercel can't run cron jobs, use:

**Option A: Vercel Cron (Limited)**
Add to `vercel.json`:
```json
{
  "crons": [{
    "path": "/api/cleanup-seats",
    "schedule": "*/5 * * * *"
  }]
}
```

**Option B: External Cron Service**
- Use **cron-job.org** (free)
- Set up to call: `https://your-app.vercel.app/cleanup-reservations/`
- Schedule: Every 5 minutes

### 4. Configure Email Service

For production emails, use a real email service:

**Recommended: SendGrid**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
```

---

## Troubleshooting

### Error: "Module not found"
- Ensure all dependencies are in `requirements.txt`
- Rebuild: `vercel --prod`

### Error: "Database connection failed"
- Check `DATABASE_URL` format
- Ensure database allows connections from any IP (0.0.0.0/0)
- For Neon: Use connection string with `?sslmode=require`

### Error: "Static files not loading"
- Check `STATIC_ROOT` in settings.py
- Verify `collectstatic` ran in build script
- Check Vercel logs: `vercel logs`

### Error: "502 Bad Gateway"
- Check application logs in Vercel dashboard
- Ensure `wsgi.py` path is correct in `vercel.json`
- Verify Python version (3.11) is supported

### Payment Not Working
- Ensure payment keys are set in environment variables
- Check Razorpay/Stripe dashboard for webhook configuration
- Test with test card numbers provided by payment gateway

---

## Useful Commands

### Check Deployment Status
```powershell
# Run the deployment checker script
powershell -ExecutionPolicy Bypass -File vercel-deploy-check.ps1
```

### View Vercel Logs
```powershell
vercel logs
```

### Redeploy
```powershell
git add .
git commit -m "Update"
git push
# Vercel auto-deploys on push
```

### Local Development
```powershell
python manage.py runserver
```

---

## Cost Estimates

### Vercel Free Tier:
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Serverless functions
- ❌ No database included
- ❌ No persistent storage

### External Services:
- **Neon.tech**: Free tier (0.5GB storage, 1 project)
- **Cloudinary**: Free tier (25GB bandwidth, 25GB storage)
- **SendGrid**: Free tier (100 emails/day)
- **Total Monthly Cost**: $0 (with free tiers)

### Render Free Tier (Alternative):
- ✅ Free PostgreSQL database
- ✅ Free web service (spins down after inactivity)
- ✅ Persistent storage
- ✅ Built-in cron jobs
- **Much easier for Django!**

---

## Final Recommendation

**For Django applications, I strongly recommend using Render.com instead of Vercel:**

| Feature | Vercel | Render |
|---------|--------|--------|
| Django Support | ⚠️ Limited | ✅ Excellent |
| Database | ❌ External only | ✅ Built-in PostgreSQL |
| Media Files | ❌ Need cloud storage | ✅ Persistent disk |
| Cron Jobs | ❌ External service | ✅ Built-in |
| Setup Difficulty | 🔴 Hard | 🟢 Easy |
| Cost (Free Tier) | $0 + external services | $0 (all included) |

**Render is specifically designed for Python/Django applications and will save you hours of configuration time.**

---

## Need Help?

- **Vercel Documentation**: https://vercel.com/docs
- **Render Documentation**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.1/howto/deployment/

For detailed Vercel-specific instructions, see `VERCEL_DEPLOYMENT.md`.

Good luck with your deployment! 🚀
