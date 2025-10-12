# 🚀 Render Deployment Guide - Fixed for Python 3.11

## ✅ Changes Made to Fix Deployment

I've fixed the deployment issues you were experiencing:

### 1. **Added `runtime.txt`**
   - Specifies Python 3.11.9 (more stable than 3.13)
   - Prevents compatibility issues with dependencies

### 2. **Updated `requirements.txt`**
   - Updated Django to 5.1.4 (more stable)
   - Updated gunicorn to 23.0.0
   - Updated all dependencies to compatible versions
   - Added WhiteNoise for static file serving

### 3. **Updated `settings.py`**
   - Added WhiteNoise middleware for better static file handling
   - Added WhiteNoise storage configuration
   - Added MEDIA_URL and MEDIA_ROOT settings

### 4. **Created `build.sh`**
   - Automated build script for Render
   - Handles pip upgrade, dependencies, collectstatic, and migrations

### 5. **Created `render.yaml`**
   - Blueprint file for easy Render deployment
   - Pre-configured with all necessary settings

---

## 🔧 Deploy on Render (Updated Instructions)

### Step 1: Create PostgreSQL Database

1. Go to your Render dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `bookmyseat-db`
   - **Database**: `bookmyseat`
   - **User**: `bookmyseat_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click **"Create Database"**
5. **Copy the Internal Database URL** (starts with `postgresql://`)

### Step 2: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `venkyok/book-my-seat`
3. Configure:
   - **Name**: `bookmyseat`
   - **Region**: Same as your database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn bookmyseat.wsgi:application`
   - **Plan**: Free

### Step 3: Add Environment Variables

In the "Environment" section, add these variables:

```
SECRET_KEY=<click "Generate" button>
DEBUG=False
DATABASE_URL=<paste-internal-database-url-from-step-1>
ALLOWED_HOSTS=.onrender.com
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret_key
```

**Important Notes:**
- Click the **"Generate"** button next to SECRET_KEY to auto-generate
- Use the **Internal Database URL** from your PostgreSQL instance
- Don't use quotes around the values

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for the build to complete (5-10 minutes)
3. Your app will be live at: `https://bookmyseat.onrender.com`

---

## 🎯 Post-Deployment Steps

### 1. Create Superuser

Once deployed, open the Render Shell:
1. Go to your web service dashboard
2. Click **"Shell"** in the left menu
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow the prompts to create admin account

### 2. Access Admin Panel

Visit: `https://your-app-name.onrender.com/admin/`

### 3. Add Movies and Theaters

Use the admin panel to add:
- Movies (with posters and trailers)
- Theaters
- Seats

---

## 🔍 Troubleshooting

### Build Still Failing?

**Check Build Command:**
- Make sure it's: `./build.sh`
- If it says "permission denied", SSH into shell and run:
  ```bash
  chmod +x build.sh
  ```

**Check Python Version:**
- Ensure `runtime.txt` contains: `python-3.11.9`

**Check Environment Variables:**
- Verify DATABASE_URL is set correctly
- Verify SECRET_KEY is generated
- Verify DEBUG is set to False

### Static Files Not Loading?

The WhiteNoise configuration should handle this automatically. If issues persist:

1. Check that `collectstatic` ran in build logs
2. Verify STATIC_ROOT is set in settings.py
3. Try manual collectstatic:
   ```bash
   python manage.py collectstatic --no-input
   ```

### Database Connection Issues?

1. Verify DATABASE_URL is the **Internal** URL (not External)
2. Check that your web service and database are in the **same region**
3. Ensure DATABASE_URL includes `?sslmode=require` at the end

### App Crashes on Start?

1. Check logs in Render dashboard (Logs tab)
2. Common issues:
   - Missing environment variable
   - Database not accessible
   - Migrations not run

---

## 📊 What's Different from Before?

| Previous Setup | Fixed Setup |
|----------------|-------------|
| Django 5.2.6 | Django 5.1.4 (more stable) |
| No runtime.txt | Python 3.11.9 specified |
| Old gunicorn | Latest gunicorn 23.0.0 |
| No WhiteNoise | WhiteNoise for static files |
| Manual build | Automated build.sh script |
| No render.yaml | Blueprint for easy deploy |

---

## ✨ Features After Deployment

Your app will have:
- ✅ Movie listing with filters
- ✅ Seat selection with 5-minute timeout
- ✅ Payment integration (Razorpay/Stripe)
- ✅ Email confirmations
- ✅ Admin dashboard with analytics
- ✅ Responsive design
- ✅ Automatic HTTPS (via Render)

---

## 💰 Cost

**Free Tier Includes:**
- PostgreSQL Database (256MB)
- Web Service (512MB RAM)
- 750 hours/month runtime
- Automatic SSL
- Custom domain support

**Note:** Free tier services spin down after 15 minutes of inactivity (spins up in ~30 seconds on first request)

---

## 🔄 Future Updates

To deploy updates:
```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically detect the push and redeploy!

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com/
- **Check Build Logs**: Render Dashboard → Your Service → Logs

Your deployment should now work perfectly! 🎉
