# 🔴 Fixing 500 Internal Server Error on Vercel

## What's Happening

You're seeing `500 Internal Server Error` which means:
- ❌ Django can't connect to the database
- ❌ Missing environment variables
- ❌ Or other configuration issue

The **200 responses** you see are from older deployments that worked.

---

## 🔍 Step 1: Check Function Logs (Find the Real Error)

1. Go to **Vercel Dashboard**
2. Click your project: **book-my-seat**
3. Click **"Deployments"** tab
4. Click the **latest deployment** (the one with errors)
5. Click **"Functions"** tab
6. Click **"index.py"** function
7. Look for the **ACTUAL error message**

Common errors you might see:
- `django.core.exceptions.ImproperlyConfigured: SECRET_KEY`
- `psycopg2.OperationalError: could not connect to server`
- `KeyError: 'DATABASE_URL'`
- `No module named 'xxx'`

---

## 🔧 Step 2: Most Likely Fix - Check Environment Variables

### Go to Vercel Settings:

1. **Vercel Dashboard** → Your project → **Settings** → **Environment Variables**

### Verify ALL these are set:

| Variable | Should Be | Check |
|----------|-----------|-------|
| `SECRET_KEY` | Long random string | [ ] |
| `DEBUG` | `False` | [ ] |
| `DATABASE_URL` | `postgresql://...?sslmode=require` | [ ] |
| `ALLOWED_HOSTS` | `.vercel.app` | [ ] |

### If DATABASE_URL is Missing or Wrong:

**You MUST have a PostgreSQL database!** SQLite won't work on Vercel.

1. **Create database on Neon:** https://neon.tech
2. **Get connection string** (looks like):
   ```
   postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
3. **Add to Vercel:**
   - Key: `DATABASE_URL`
   - Value: (paste connection string)
   - Environment: All
4. **Save and redeploy**

### If SECRET_KEY is Missing:

Generate a new one:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Add to Vercel:
- Key: `SECRET_KEY`
- Value: (paste generated key)
- Environment: All

---

## 🔧 Step 3: Run Migrations

Even if DATABASE_URL is set, you MUST run migrations!

```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"

# Replace with YOUR Neon connection string!
$env:DATABASE_URL = "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require"

# Run migrations
python manage.py migrate
```

**Expected output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying movies.0001_initial... OK
  ...
```

If you see errors, the database connection is wrong.

---

## 🔧 Step 4: Redeploy After Changes

After fixing environment variables or running migrations:

1. Go to **Deployments** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**
4. Wait for deployment to complete
5. Test your app

---

## 🎯 Quick Checklist

Go through this systematically:

### Database:
- [ ] Created Neon database account
- [ ] Got connection string with `?sslmode=require`
- [ ] Added DATABASE_URL to Vercel
- [ ] Connection string is correct (test locally)
- [ ] Ran migrations: `python manage.py migrate`

### Environment Variables in Vercel:
- [ ] `DATABASE_URL` is set
- [ ] `SECRET_KEY` is set (not the default one!)
- [ ] `DEBUG` is set to `False`
- [ ] `ALLOWED_HOSTS` is set to `.vercel.app`
- [ ] All variables applied to "Production"

### Code:
- [ ] Latest code pushed to GitHub
- [ ] `index.py` exists in repository
- [ ] `vercel.json` points to `index.py`
- [ ] Requirements.txt includes `psycopg2-binary` and `dj-database-url`

### Deployment:
- [ ] Redeployed after adding variables
- [ ] Build succeeded (green checkmark)
- [ ] Function logs checked for specific error

---

## 🔍 Common Specific Errors & Fixes

### Error: "SECRET_KEY must not be empty"

**Fix:**
```powershell
# Generate new key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Add to Vercel as SECRET_KEY
```

### Error: "FATAL: password authentication failed"

**Fix:**
1. Go to Neon dashboard
2. Copy connection string again (might have expired)
3. Update DATABASE_URL in Vercel
4. Redeploy

### Error: "relation 'movies_movie' does not exist"

**Fix:**
```powershell
# Run migrations!
$env:DATABASE_URL = "your-neon-url"
python manage.py migrate
```

### Error: "could not connect to server: Connection timed out"

**Fix:**
1. Check DATABASE_URL has `?sslmode=require` at end
2. Wake up Neon database (it auto-sleeps):
   - Go to Neon dashboard
   - Click your project
   - Wait for it to activate
3. Redeploy

### Error: "No module named 'psycopg2'"

**Fix:**
Ensure `requirements.txt` has:
```
psycopg2-binary==2.9.10
```

Commit and push:
```powershell
git add requirements.txt
git commit -m "Fix psycopg2"
git push origin main
```

### Error: "ALLOWED_HOSTS"

**Fix:**
Add to Vercel environment variables:
- Key: `ALLOWED_HOSTS`
- Value: `.vercel.app`

---

## 🚀 Step-by-Step Recovery Plan

If still broken, do this in order:

### 1. Create Database (if not done)
```
✓ Go to https://neon.tech
✓ Create project "bookmyseat"
✓ Copy connection string
```

### 2. Set Environment Variables in Vercel
```
✓ DATABASE_URL = postgresql://...?sslmode=require
✓ SECRET_KEY = (generate new)
✓ DEBUG = False
✓ ALLOWED_HOSTS = .vercel.app
```

### 3. Run Migrations Locally
```powershell
$env:DATABASE_URL = "postgresql://..."
python manage.py migrate
```

### 4. Redeploy
```
✓ Vercel → Deployments → Redeploy
✓ Wait for green checkmark
```

### 5. Test
```
✓ Visit https://book-my-seat-alpha.vercel.app
✓ Should see movie list (might be empty)
```

---

## 📊 Test Database Connection Locally

Before redeploying, test if your DATABASE_URL works:

```powershell
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"

# Set your DATABASE_URL
$env:DATABASE_URL = "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require"

# Test connection
python manage.py dbshell
```

If successful, you'll see PostgreSQL prompt:
```
psql (16.x)
Type "help" for help.

neondb=>
```

Type `\q` to quit.

If this fails, your DATABASE_URL is wrong!

---

## 🔍 View Full Error Details

To see the actual Python error:

### Method 1: Vercel Dashboard
1. Deployments → Latest → Functions → index.py
2. Scroll through logs
3. Look for Python traceback starting with "Traceback"

### Method 2: Vercel CLI
```powershell
npm install -g vercel
vercel login
vercel logs book-my-seat --prod
```

---

## ⚡ Quick Fix Commands

```powershell
# Navigate to project
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"

# Set DATABASE_URL (REPLACE WITH YOURS!)
$env:DATABASE_URL = "postgresql://user:pass@host.neon.tech/db?sslmode=require"

# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Test database connection
python manage.py check --database default

# Run migrations
python manage.py migrate

# Check if migrations worked
python manage.py showmigrations
```

---

## 🎯 Expected Working State

When everything is working:

1. **Vercel deployment:** Green checkmark ✅
2. **Homepage:** Shows movie list (might be empty)
3. **Admin:** `https://book-my-seat-alpha.vercel.app/admin/` loads
4. **Status code:** 200 (not 500)
5. **Function logs:** No errors, just successful requests

---

## 🆘 Still Getting 500 Errors?

### Share the actual error message:

Look in Vercel Function Logs for lines like:
```
Traceback (most recent call last):
  File "...", line X, in ...
    ...
[ERROR TYPE]: [ERROR MESSAGE]
```

Copy that full error and I can help fix it specifically.

---

## 💡 Alternative: Switch to Render

If Vercel is too complex, **Render is MUCH easier** for Django:
- ✅ Built-in database (no Neon needed)
- ✅ Simpler setup
- ✅ Better error messages
- ✅ One-click deploy

See: **`RENDER_URGENT_FIX.md`**

---

## ✅ Summary

**Most likely cause:** Missing or incorrect DATABASE_URL

**Quick fix:**
1. Create Neon database → Get connection string
2. Add DATABASE_URL to Vercel environment variables
3. Run migrations locally: `python manage.py migrate`
4. Redeploy in Vercel
5. Test: Visit your app URL

**Check Function Logs in Vercel for the specific error!**
