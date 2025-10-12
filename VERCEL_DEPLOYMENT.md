# 🚀 VERCEL DEPLOYMENT GUIDE - BookMySeat

## ⚠️ IMPORTANT: Vercel Limitations for Django

**Please Read:** Vercel is primarily designed for frontend/serverless applications. Django deployment on Vercel has some limitations:

### Limitations:
1. **Database:** SQLite won't persist between deployments (use external database)
2. **Media Files:** Uploaded files won't persist (use cloud storage)
3. **Background Tasks:** Seat cleanup cron won't work automatically
4. **Cold Starts:** First request may be slow
5. **Execution Time:** 10-second timeout for serverless functions

### Recommended Alternatives:
- **Render.com** (Better for Django, has PostgreSQL, persistent storage)
- **Railway.app** (Django-friendly, easier setup)
- **PythonAnywhere** (Designed for Python apps)

**If you still want to use Vercel, continue below:**

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### ✅ Files Already Configured:
- [x] `vercel.json` - Vercel configuration
- [x] `build_files.sh` - Build script
- [x] `requirements.txt` - Dependencies
- [x] `wsgi.py` - WSGI application
- [x] `.gitignore` - Ignore unnecessary files
- [x] Settings updated for environment variables

---

## 🔧 STEP 1: Setup External Database

**You MUST use an external database (Vercel doesn't support SQLite persistence)**

### Option A: Neon (PostgreSQL - Recommended & Free)

1. Go to https://neon.tech/
2. Sign up with GitHub
3. Create new project: "bookmyseat"
4. Copy the connection string (looks like: `postgresql://user:pass@host/database`)
5. Save it - you'll need it in Step 4

### Option B: ElephantSQL (PostgreSQL - Free Tier)

1. Go to https://www.elephantsql.com/
2. Sign up
3. Create new instance (Free Tiny Turtle plan)
4. Copy the URL

### Option C: MongoDB Atlas (Alternative)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create cluster
3. Get connection string
4. Note: Would need to use djongo or similar

---

## 🚀 STEP 2: Deploy to Vercel

### Method 1: Deploy via GitHub (Recommended)

#### 2.1: Push to GitHub
```bash
# Initialize git (if not already done)
cd c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Create GitHub repository
# Go to https://github.com/new
# Name: bookmyseat
# Don't initialize with README

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/bookmyseat.git
git branch -M main
git push -u origin main
```

#### 2.2: Connect to Vercel
1. Go to https://vercel.com/
2. Sign up/Login with GitHub
3. Click "Add New..." → "Project"
4. Import your `bookmyseat` repository
5. Configure project:
   - **Framework Preset:** Other
   - **Root Directory:** ./
   - **Build Command:** (leave default)
   - **Output Directory:** (leave default)

### Method 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone
vercel

# Follow prompts:
# - Set up and deploy? Y
# - Which scope? (choose your account)
# - Link to existing project? N
# - Project name? bookmyseat
# - Directory? ./
# - Override settings? N
```

---

## 🔐 STEP 3: Configure Environment Variables

### In Vercel Dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

```bash
# Required Variables

# Generate a new secret key at https://djecrety.ir/
SECRET_KEY=your-new-secret-key-here-52-characters-long-random-string

# Set to False for production
DEBUG=False

# Database URL from Step 1 (Neon or ElephantSQL)
DATABASE_URL=postgresql://user:password@host.region.neon.tech/database

# Allowed hosts (will be your-project.vercel.app)
ALLOWED_HOSTS=your-project.vercel.app,.vercel.app

# Email Configuration (Optional but recommended)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=BookMySeat <noreply@bookmyseat.com>

# Payment Gateway (Add when ready)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### Important Notes:
- Click "Add" after each variable
- Select all environments (Production, Preview, Development)
- Don't include quotes around values

---

## 🗃️ STEP 4: Initialize Database

After first deployment, you need to run migrations:

### Option 1: Using Vercel CLI
```bash
# Install dependencies
vercel env pull

# Run migrations locally against production database
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Option 2: Using Database Client
```bash
# Connect directly to your database
# For Neon, use their SQL editor in the dashboard
# Run migration SQL manually (not recommended)
```

### Option 3: Temporary DEBUG=True (Quick but Insecure)
```bash
# In Vercel dashboard, temporarily set:
DEBUG=True

# Visit your site URL - Django will show error page
# Click the error and it may auto-create tables
# IMMEDIATELY set DEBUG=False after
# Create superuser using Vercel CLI
```

---

## 📁 STEP 5: Handle Media Files (Optional)

Since Vercel doesn't persist uploaded files, you have two options:

### Option A: Use Cloudinary (Recommended)

1. Sign up at https://cloudinary.com/
2. Install package:
```bash
pip install django-cloudinary-storage
```

3. Update settings.py:
```python
INSTALLED_APPS = [
    # ... other apps
    'cloudinary_storage',
    'cloudinary',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your_cloud_name',
    'API_KEY': 'your_api_key',
    'API_SECRET': 'your_api_secret',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### Option B: Use AWS S3

Follow Django S3 storage guide.

---

## 🔄 STEP 6: Handle Seat Cleanup (Cron Job Alternative)

Since Vercel doesn't support cron jobs, use one of these:

### Option A: External Cron Service

**Use cron-job.org:**
1. Go to https://cron-job.org/
2. Create free account
3. Add new cron job:
   - URL: `https://your-project.vercel.app/movies/cleanup-endpoint/`
   - Schedule: Every minute
   - Need to create this endpoint first!

**Create cleanup endpoint in views:**
```python
# In movies/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def cleanup_endpoint(request):
    # Add simple authentication
    if request.GET.get('key') != 'your-secret-key':
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    count = Booking.release_expired_bookings()
    return JsonResponse({'released': count})

# Add to urls.py
path('cleanup-endpoint/', views.cleanup_endpoint, name='cleanup_endpoint'),
```

### Option B: Client-Side Cleanup

Run cleanup on each page load (not ideal but works):
```python
# In movies/views.py, add to each view:
Booking.release_expired_bookings()
```

---

## 📊 STEP 7: Post-Deployment Testing

### Test Checklist:

1. **Visit your site:** `https://your-project.vercel.app/`
2. **Check admin:** `https://your-project.vercel.app/admin/`
3. **Test user registration**
4. **Test movie browsing**
5. **Test seat selection**
6. **Test payment (use test mode)**
7. **Check analytics dashboard**

### If Something Breaks:

Check Vercel logs:
```bash
vercel logs
```

Or in dashboard: Project → Deployments → Click deployment → View logs

---

## 🐛 TROUBLESHOOTING

### Issue: "Application Error" on Vercel
**Solution:**
- Check environment variables are set
- Verify DATABASE_URL is correct
- Check Vercel function logs
- Set DEBUG=True temporarily to see error

### Issue: Static files not loading
**Solution:**
```bash
# Redeploy to trigger collectstatic
vercel --prod
```

### Issue: Database connection failed
**Solution:**
- Verify DATABASE_URL format
- Check database service is running
- Ensure IP whitelist includes Vercel IPs (if required)

### Issue: "This field is required" on payment
**Solution:**
- Check RAZORPAY_KEY_ID is set in environment variables
- Verify keys are correct

### Issue: 500 Internal Server Error
**Solution:**
```bash
# View detailed logs
vercel logs --follow
```

---

## 💰 COSTS

### Free Tier:
- **Vercel:** Free (hobby plan)
- **Neon Database:** Free tier (0.5GB storage)
- **Cloudinary:** Free tier (25GB bandwidth)
- **Total:** $0/month

### Paid (if you exceed limits):
- **Vercel Pro:** $20/month
- **Neon Scale:** $19/month
- **Cloudinary Pro:** $99/month

---

## 🔒 SECURITY CHECKLIST

Before going live:

- [ ] Set DEBUG=False
- [ ] Generate new SECRET_KEY
- [ ] Use HTTPS (Vercel provides automatically)
- [ ] Set proper ALLOWED_HOSTS
- [ ] Use environment variables (not hardcoded)
- [ ] Enable CSRF protection (already enabled)
- [ ] Add rate limiting (optional)
- [ ] Set up monitoring

---

## 📱 CUSTOM DOMAIN (Optional)

### Add Custom Domain:

1. In Vercel dashboard: Settings → Domains
2. Add your domain: `bookmyseat.com`
3. Follow DNS configuration instructions
4. Update ALLOWED_HOSTS:
```bash
ALLOWED_HOSTS=bookmyseat.com,www.bookmyseat.com,.vercel.app
```

---

## 🔄 UPDATING YOUR APP

### After making changes:

```bash
# Commit changes
git add .
git commit -m "Update feature X"
git push origin main

# Vercel will automatically redeploy!
```

Or using CLI:
```bash
vercel --prod
```

---

## 📞 SUPPORT RESOURCES

### Documentation:
- **Vercel Docs:** https://vercel.com/docs
- **Django on Vercel:** https://vercel.com/guides/deploying-django-with-vercel
- **Neon Docs:** https://neon.tech/docs

### Quick Commands:
```bash
# View logs
vercel logs

# Rollback deployment
vercel rollback

# List deployments
vercel ls

# Remove project
vercel remove bookmyseat
```

---

## ⚠️ IMPORTANT REMINDERS

1. **Database:** Must use external PostgreSQL (Neon or ElephantSQL)
2. **Media Files:** Must use Cloudinary or S3
3. **Cron Jobs:** Need external service for seat cleanup
4. **Cold Starts:** First request may be slow (3-5 seconds)
5. **Timeouts:** Responses must complete within 10 seconds

---

## 🎯 ALTERNATIVE: QUICK SWITCH TO RENDER

If Vercel proves difficult, Render is easier for Django:

```bash
# Create Render account
# Connect GitHub repo
# Add PostgreSQL database (included!)
# Deploy (handles migrations automatically)
# No media file issues
# Cron jobs supported natively

# Total time: 15 minutes vs Vercel's 45+ minutes
```

**Recommendation:** Use Render for Django apps unless you specifically need Vercel's edge network.

---

## ✅ DEPLOYMENT SUCCESS CHECKLIST

- [ ] External database configured (Neon/ElephantSQL)
- [ ] GitHub repository created and pushed
- [ ] Vercel project created
- [ ] Environment variables set (minimum 3: SECRET_KEY, DEBUG, DATABASE_URL)
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Static files collected
- [ ] Site accessible at vercel.app URL
- [ ] Admin panel working
- [ ] User registration tested
- [ ] Booking flow tested
- [ ] Payment gateway tested (test mode)

---

## 🎉 YOU'RE LIVE!

Once all checks pass, your BookMySeat application is live on Vercel!

**Your URL:** `https://your-project.vercel.app/`

Share it with the world! 🚀🎬🎟️

---

**Need Help?** Check the troubleshooting section or Vercel's documentation.
