# 🗄️ Database Setup for Vercel - Step by Step

## Why You Need an External Database

Vercel is **serverless** and doesn't support SQLite in production because:
- ❌ SQLite files don't persist (serverless functions are stateless)
- ❌ No shared filesystem between function invocations
- ✅ You MUST use an external PostgreSQL database

---

## 📊 Best Free PostgreSQL Options

| Provider | Free Tier | Setup Time | Recommended |
|----------|-----------|------------|-------------|
| **Neon** | 0.5GB, Auto-sleep | 2 min | ⭐ YES |
| **ElephantSQL** | 20MB | 3 min | ⭐ YES |
| **Supabase** | 500MB | 5 min | Good |
| **Railway** | 1GB (trial) | 5 min | Good |

**Recommendation: Use Neon.tech** - Modern, fast, generous free tier!

---

## 🚀 Option 1: Neon.tech (RECOMMENDED)

### Step 1: Sign Up

1. Go to **https://neon.tech**
2. Click **"Sign Up"**
3. Sign up with **GitHub** (fastest)
4. You'll be redirected to dashboard

### Step 2: Create Database Project

1. Click **"Create a project"** or **"New Project"**
2. Fill in details:
   - **Project name**: `bookmyseat` (or any name)
   - **PostgreSQL version**: 16 (latest)
   - **Region**: Choose closest to you:
     - US East (Ohio) - `us-east-2`
     - US West (Oregon) - `us-west-2`
     - Europe (Frankfurt) - `eu-central-1`
     - Asia Pacific (Singapore) - `ap-southeast-1`
3. Click **"Create project"**

### Step 3: Get Connection String

After project creation, you'll see a connection string:

**Copy the connection string** - it looks like:
```
postgresql://neondb_owner:AbCdEfGh123456@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**Components explained:**
- `neondb_owner` - Username
- `AbCdEfGh123456` - Password
- `ep-cool-name-123456.us-east-2.aws.neon.tech` - Host
- `neondb` - Database name
- `?sslmode=require` - SSL mode (required!)

**⚠️ SAVE THIS!** You'll need it for Vercel environment variables.

### Step 4: Keep the Tab Open

Don't close the Neon tab - you might need to reference it.

**Important Note:** Neon free tier auto-sleeps after 5 minutes of inactivity. It wakes up automatically on first request (takes ~1 second).

---

## 🚀 Option 2: ElephantSQL (Alternative)

### Step 1: Sign Up

1. Go to **https://www.elephantsql.com**
2. Click **"Get a managed database today"**
3. Sign up with email or GitHub

### Step 2: Create Instance

1. Click **"Create New Instance"**
2. Fill in:
   - **Name**: `bookmyseat`
   - **Plan**: **Tiny Turtle** (Free)
   - **Tags**: (leave empty)
3. Click **"Select Region"**
4. Choose closest datacenter
5. Click **"Review"**
6. Click **"Create instance"**

### Step 3: Get Connection URL

1. Click on your new instance
2. Copy the **URL** (looks like):
```
postgresql://username:password@host.db.elephantsql.com/username
```

**⚠️ SAVE THIS!** You'll need it for Vercel.

---

## 🔧 Add Database to Vercel

### Step 1: Go to Vercel Dashboard

1. Go to **https://vercel.com**
2. Click your project: **book-my-seat**
3. Click **"Settings"** tab
4. Click **"Environment Variables"** in left menu

### Step 2: Add DATABASE_URL

1. Click **"Add New"** or **"Add Variable"**
2. Fill in:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste your Neon/ElephantSQL connection string
   - **Environment**: Select all (Production, Preview, Development)
3. Click **"Save"**

**Example:**
```
Key: DATABASE_URL
Value: postgresql://user:pass@ep-cool-name.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Step 3: Verify Other Environment Variables

While you're here, ensure these are also set:

| Key | Value | Example |
|-----|-------|---------|
| `SECRET_KEY` | (generate new) | `django-insecure-abc123...` |
| `DEBUG` | `False` | `False` |
| `ALLOWED_HOSTS` | `.vercel.app` | `.vercel.app` |
| `RAZORPAY_KEY_ID` | (optional) | `rzp_test_...` |
| `RAZORPAY_KEY_SECRET` | (optional) | `your_secret` |

### Step 4: Redeploy

After adding DATABASE_URL:
1. Go to **"Deployments"** tab
2. Click **"..."** on latest deployment
3. Click **"Redeploy"**
4. Wait for deployment to complete

---

## 🎯 Run Migrations on Your Database

**IMPORTANT:** After setting up the database, you MUST run migrations!

### Method 1: Using Local Computer (Easiest)

1. **Open PowerShell**
2. **Navigate to your project:**
   ```powershell
   cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
   ```

3. **Set the DATABASE_URL environment variable:**
   ```powershell
   $env:DATABASE_URL = "postgresql://user:pass@ep-cool-name.neon.tech/neondb?sslmode=require"
   ```
   ⚠️ Replace with YOUR actual connection string from Neon/ElephantSQL!

4. **Run migrations:**
   ```powershell
   python manage.py migrate
   ```

5. **Create superuser:**
   ```powershell
   python manage.py createsuperuser
   ```
   Enter:
   - Username: `admin` (or your choice)
   - Email: your email
   - Password: choose a strong password
   - Confirm password

6. **Test database connection:**
   ```powershell
   python manage.py dbshell
   ```
   If successful, you'll see PostgreSQL prompt. Type `\q` to quit.

### Method 2: Using Vercel CLI

1. **Install Vercel CLI:**
   ```powershell
   npm install -g vercel
   ```

2. **Login:**
   ```powershell
   vercel login
   ```

3. **Link project:**
   ```powershell
   cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
   vercel link
   ```
   Follow prompts to link to your Vercel project.

4. **Pull environment variables:**
   ```powershell
   vercel env pull .env.production
   ```
   This downloads your Vercel environment variables locally.

5. **Run migrations:**
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Method 3: Using Database Client (GUI)

1. **Download pgAdmin:** https://www.pgadmin.org/download/
2. **Connect to database:**
   - Host: (from your connection string)
   - Port: 5432
   - Database: (from your connection string)
   - Username: (from your connection string)
   - Password: (from your connection string)
3. **Run SQL manually** (not recommended, use method 1 or 2)

---

## ✅ Verify Database Setup

### Test 1: Check Migrations

```powershell
$env:DATABASE_URL = "your-connection-string"
python manage.py showmigrations
```

You should see all migrations with [X] marks:
```
movies
 [X] 0001_initial
users
 [X] 0001_initial
...
```

### Test 2: Check Tables

```powershell
python manage.py dbshell
```

In PostgreSQL shell, run:
```sql
\dt
```

You should see tables like:
- `movies_movie`
- `movies_theater`
- `movies_seat`
- `movies_booking`
- `auth_user`
- etc.

Type `\q` to quit.

### Test 3: Access Admin Panel

After deployment:
1. Go to: `https://your-app.vercel.app/admin/`
2. Login with superuser credentials
3. You should see Django admin dashboard

---

## 🎬 Add Sample Data

After migrations, add some data:

### Option 1: Through Admin Panel

1. Go to: `https://your-app.vercel.app/admin/`
2. Add Movies:
   - Click "Movies" → "Add Movie"
   - Fill in details (name, genre, language, etc.)
   - For poster: Use external URL (Vercel doesn't persist files)
3. Add Theaters
4. Add Seats

### Option 2: Using Django Shell

```powershell
$env:DATABASE_URL = "your-connection-string"
python manage.py shell
```

```python
from movies.models import Movie, Theater, Seat

# Create a movie
movie = Movie.objects.create(
    name="Inception",
    genre="Action",
    language="English",
    duration=148,
    description="A mind-bending thriller",
    trailer_url="https://www.youtube.com/watch?v=YoHD9XEInc0"
)

# Create a theater
theater = Theater.objects.create(
    name="PVR Cinemas",
    location="Downtown",
    movie=movie,
    show_time="2025-10-15 19:00:00"
)

# Create seats
for row in ['A', 'B', 'C']:
    for num in range(1, 11):
        Seat.objects.create(
            theater=theater,
            seat_number=f"{row}{num}",
            is_available=True
        )

print("Sample data created!")
```

---

## 🔍 Troubleshooting

### Error: "Could not connect to database"

**Check:**
1. DATABASE_URL is correctly set in Vercel
2. Connection string includes `?sslmode=require`
3. Database is active (Neon wakes up on first request)

**Fix:**
```powershell
# Test connection locally
$env:DATABASE_URL = "your-connection-string"
python manage.py dbshell
```

### Error: "relation does not exist"

**Cause:** Migrations not run

**Fix:**
```powershell
$env:DATABASE_URL = "your-connection-string"
python manage.py migrate --run-syncdb
```

### Error: "FATAL: password authentication failed"

**Cause:** Wrong credentials in DATABASE_URL

**Fix:**
1. Go back to Neon/ElephantSQL dashboard
2. Copy connection string again
3. Update DATABASE_URL in Vercel
4. Redeploy

### Error: "database is locked" (SQLite error)

**Cause:** Still using SQLite instead of PostgreSQL

**Fix:**
1. Verify DATABASE_URL is set in Vercel
2. Check settings.py properly reads DATABASE_URL
3. Redeploy

---

## 📊 Database Management

### View Database Size

```powershell
$env:DATABASE_URL = "your-connection-string"
python manage.py dbshell
```

```sql
SELECT pg_size_pretty(pg_database_size('neondb'));
\q
```

### Backup Database

```powershell
# Export to SQL file
$env:DATABASE_URL = "your-connection-string"
python manage.py dumpdata > backup.json
```

### Reset Database (Careful!)

```powershell
$env:DATABASE_URL = "your-connection-string"
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

---

## 💰 Free Tier Limits

### Neon Free Tier:
- ✅ 0.5 GB storage
- ✅ Unlimited queries
- ✅ Auto-sleep after 5 min inactivity
- ✅ Automatic backups
- ⚠️ One project

### ElephantSQL Free Tier:
- ✅ 20 MB storage (smaller)
- ✅ 5 concurrent connections
- ✅ Always active
- ⚠️ Smaller storage

**Both are free forever!**

---

## 🎯 Quick Reference

### Your Connection String Format:
```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE?sslmode=require
```

### Essential Commands:
```powershell
# Set database URL
$env:DATABASE_URL = "your-connection-string"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access database shell
python manage.py dbshell

# Check migrations status
python manage.py showmigrations
```

---

## ✅ Checklist

Setup completed when you can check all these:

- [ ] Neon/ElephantSQL account created
- [ ] Database project/instance created
- [ ] Connection string copied
- [ ] DATABASE_URL added to Vercel environment variables
- [ ] Vercel redeployed
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Can login to admin panel
- [ ] Sample data added
- [ ] App loads without database errors

---

## 🆘 Still Having Issues?

### Option 1: Use Render Instead

Render includes PostgreSQL database - much easier!

See: **`RENDER_URGENT_FIX.md`**

### Option 2: Check Logs

In Vercel dashboard:
1. Go to "Deployments"
2. Click latest deployment
3. Check "Function Logs"
4. Look for database-related errors

---

**You're ready to set up the database!** 🚀

**Quick Start:**
1. Go to https://neon.tech
2. Create project
3. Copy connection string
4. Add to Vercel as DATABASE_URL
5. Run migrations locally
6. Done! ✅
