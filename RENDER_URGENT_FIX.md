# 🔥 URGENT FIX - Render Dashboard Configuration

## The Problem
Render is ignoring your configuration files and using wrong commands.

## ✅ MANUAL FIX (Do this in Render Dashboard NOW)

### Step 1: Go to Your Web Service Settings

1. Go to https://dashboard.render.com
2. Click on your **bookmyseat** web service
3. Click **"Settings"** in the left sidebar

### Step 2: Update These Settings

Scroll down and update **EXACTLY** as shown:

#### Build Command
**Change from:** `./build.sh` or whatever it says  
**Change to:**
```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

#### Start Command
**Change from:** `gunicorn app:app` (WRONG!)  
**Change to:**
```bash
gunicorn bookmyseat.wsgi:application
```

#### Python Version
**Find "Python Version" setting**  
**Set to:** `3.11.9`

### Step 3: Verify Environment Variables

Still in Settings, scroll to **"Environment Variables"** section.

Make sure you have these (click "Add Environment Variable" if missing):

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Click "Generate" or paste a long random string |
| `DEBUG` | `False` |
| `DATABASE_URL` | Your PostgreSQL Internal URL (from database instance) |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `PYTHON_VERSION` | `3.11.9` |
| `RAZORPAY_KEY_ID` | Your Razorpay key |
| `RAZORPAY_KEY_SECRET` | Your Razorpay secret |

### Step 4: Save and Deploy

1. Scroll to the bottom
2. Click **"Save Changes"**
3. Render will automatically redeploy with correct settings
4. Wait 5-10 minutes for build to complete

---

## 🔍 If It Still Fails

### Check Python Version in Build Logs

1. Go to **"Logs"** tab
2. Look for: `Python version: 3.x.x`
3. If it says `3.13.x` instead of `3.11.x`:
   - Add environment variable: `PYTHON_VERSION` = `3.11.9`
   - Click "Manual Deploy" → "Clear build cache & deploy"

### Check Start Command

1. In logs, look for line starting with: `==> Running`
2. Should say: `==> Running 'gunicorn bookmyseat.wsgi:application'`
3. If it says `app:app` - you didn't update the Start Command correctly

---

## 📋 Quick Checklist

- [ ] Build Command updated to full pip install command
- [ ] Start Command = `gunicorn bookmyseat.wsgi:application`
- [ ] Python Version = `3.11.9` (in both settings and env vars)
- [ ] DATABASE_URL is set to PostgreSQL Internal URL
- [ ] SECRET_KEY is generated
- [ ] DEBUG = `False`
- [ ] ALLOWED_HOSTS = `.onrender.com`
- [ ] Saved all changes
- [ ] Deployment started

---

## 🎯 Expected Result

After fixing these settings, your build logs should show:

```
==> Using Python version: 3.11.9
==> Installing dependencies from requirements.txt
==> Collecting static files
==> Running migrations
==> Build successful!
==> Starting service with: gunicorn bookmyseat.wsgi:application
==> Your service is live!
```

---

## ⚠️ Common Mistakes

1. **NOT updating Start Command** - Most common issue!
2. **Using External Database URL instead of Internal** - Use Internal!
3. **Not setting PYTHON_VERSION environment variable**
4. **Typos in command** - Copy/paste exactly as shown

---

## 💡 Why This Happened

Render sometimes doesn't read `render.yaml` or `runtime.txt` files on first deploy. You need to manually configure it through the dashboard. Once set, future deploys will use these settings.

---

## 🆘 Still Not Working?

**Delete and recreate the web service:**

1. Delete current web service in Render
2. Create new web service
3. Connect GitHub repo
4. **BEFORE clicking "Create"**, set:
   - Build Command: (full command from above)
   - Start Command: `gunicorn bookmyseat.wsgi:application`
5. Add all environment variables
6. Then click "Create Web Service"

---

**Fix these settings NOW and your deployment will work!** 🚀
