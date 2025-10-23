# 🚀 Deploy to Vercel (SQLite Version)

**Status:** Ready to Deploy ✅  
**Database:** SQLite (Demo/Development Only)  
**Last Updated:** October 23, 2025

---

## ⚠️ Important Warning

**SQLite on Vercel is for DEMO purposes only!**

- ❌ **Data will NOT persist** - Vercel's filesystem is ephemeral (resets on every deployment)
- ❌ **Database resets** - Every new deployment creates a fresh database
- ❌ **No file uploads persist** - Media files disappear after deployment
- ✅ **Good for:** Demonstrations, prototypes, portfolio showcases
- ❌ **Not good for:** Production, real users, data that needs to persist

**For production with persistent data, you need PostgreSQL (see DEPLOY_TO_RENDER_NOW.md)**

---

## 📋 Pre-Deployment Checklist

✅ Database code removed (PostgreSQL dependencies)  
✅ SQLite configuration in settings.py  
✅ `vercel.json` configured  
✅ `index.py` WSGI handler ready  
✅ `build_files.sh` build script ready  
✅ `requirements.txt` updated  
✅ Static files configuration set  
✅ ALLOWED_HOSTS includes `.vercel.app`  

---

## 🎯 Quick Deploy Steps

### Step 1: Push to GitHub

```bash
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"

# Stage all changes
git add .

# Commit changes
git commit -m "Remove PostgreSQL, prepare for Vercel deployment with SQLite"

# Push to GitHub
git push origin main
```

### Step 2: Deploy to Vercel

#### Option A: Vercel Dashboard (Easiest)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Choose `venkyok/book-my-seat` repository
   - Click "Import"

3. **Configure Project**
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** Leave empty (uses build_files.sh)
   - **Output Directory:** Leave empty
   - **Install Command:** `pip install -r requirements.txt`

4. **Add Environment Variables**
   Click "Environment Variables" and add:
   
   ```
   SECRET_KEY = your-super-secret-key-here-minimum-50-characters-long
   DEBUG = False
   ALLOWED_HOSTS = .vercel.app,.now.sh
   ```

   **Generate a secure SECRET_KEY:**
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build and deployment
   - Your app will be live at: `https://book-my-seat.vercel.app`

#### Option B: Vercel CLI (Advanced)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
cd "c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone"
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Select your account
# - Link to existing project? No
# - Project name? book-my-seat
# - Directory? ./
# - Override settings? No

# Production deployment
vercel --prod
```

---

## 🔧 Post-Deployment Setup

### Step 1: Create Superuser (Temporary - Resets on Redeploy!)

**⚠️ Note:** Since SQLite resets on every deployment, you'll need to recreate the superuser after each deployment.

**Method A: Using Local SQLite (Demo Data)**
```bash
# Run migrations locally
python manage.py migrate

# Create superuser locally
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (your secure password)

# Add sample movies
python manage.py shell
>>> from movies.models import Movie
>>> Movie.objects.create(name="Test Movie", genre="Action", language="English")
>>> exit()
```

**Method B: Using Vercel API (Advanced)**
Unfortunately, Vercel doesn't provide shell access for Django management commands.

### Step 2: Test Your Deployment

1. **Homepage:**
   - Visit: `https://your-project.vercel.app/movies/`
   - Should show movie list (empty initially)

2. **Admin Panel:**
   - Visit: `https://your-project.vercel.app/admin/`
   - Login won't work (no superuser in fresh database)

3. **Static Files:**
   - Check if CSS/JS loads correctly
   - Bootstrap styles should be visible

---

## 📁 File Structure (Vercel Ready)

```
djnago-bookmyshow-clone/
├── vercel.json              ✅ Vercel configuration
├── index.py                 ✅ WSGI handler for Vercel
├── build_files.sh           ✅ Build script
├── requirements.txt         ✅ Dependencies (no PostgreSQL)
├── runtime.txt              ✅ Python version
├── manage.py                ✅ Django management
├── bookmyseat/
│   ├── settings.py          ✅ SQLite + Vercel config
│   ├── urls.py              ✅ URL routing
│   └── wsgi.py              ✅ WSGI application
├── movies/                  ✅ Movies app
├── users/                   ✅ Users app
├── templates/               ✅ HTML templates
└── static/                  ✅ Static files
```

---

## 🔍 Verification Steps

After deployment, check:

### 1. Deployment Logs
- Go to Vercel Dashboard → Your Project → Deployments
- Click on latest deployment
- Check "Building" and "Deployment" logs
- Should see: "Build Completed" ✅

### 2. Function Logs
- Go to "Functions" tab
- Check for any errors in real-time logs

### 3. Environment Variables
- Go to "Settings" → "Environment Variables"
- Verify SECRET_KEY, DEBUG, ALLOWED_HOSTS are set

### 4. Test URLs
```
✅ Homepage:        https://your-project.vercel.app/
✅ Movies:          https://your-project.vercel.app/movies/
✅ Admin:           https://your-project.vercel.app/admin/
✅ Login:           https://your-project.vercel.app/login/
✅ Register:        https://your-project.vercel.app/register/
```

---

## 🐛 Troubleshooting

### Error: "500 Internal Server Error"

**Check Vercel Function Logs:**
1. Go to Vercel Dashboard → Project → Functions
2. Look for error messages

**Common Causes:**
- Missing environment variables (SECRET_KEY)
- Static files not collecting
- Import errors

**Solutions:**
```bash
# Test locally first
python manage.py check --deploy
python manage.py collectstatic --noinput

# Check logs
vercel logs your-project.vercel.app
```

### Error: "Module not found"

**Solution:** Ensure all dependencies in `requirements.txt`
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
# Redeploy on Vercel
```

### Error: "Static files not loading"

**Solution:** Check `settings.py` has:
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MIDDLEWARE = [
    # ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]
```

### Error: "Admin panel not working"

**This is EXPECTED with SQLite on Vercel:**
- Database resets on every deployment
- No superuser persists
- Cannot create superuser on Vercel

**Solution:** Use PostgreSQL (deploy to Render instead)

---

## 📊 What Works vs. What Doesn't

### ✅ What Works on Vercel (SQLite)

| Feature | Status | Notes |
|---------|--------|-------|
| Homepage | ✅ Works | Static content loads |
| Movie List Page | ✅ Works | Shows empty list (no data persists) |
| Static Files (CSS/JS) | ✅ Works | Served via WhiteNoise |
| Templates | ✅ Works | All HTML renders correctly |
| URL Routing | ✅ Works | All routes functional |
| User Registration | ⚠️ Partial | Works but user doesn't persist |
| Login System | ⚠️ Partial | Works but session limited |

### ❌ What Doesn't Work on Vercel (SQLite)

| Feature | Status | Issue |
|---------|--------|-------|
| Database Persistence | ❌ Broken | Resets on every deployment |
| Admin Panel | ❌ Broken | No superuser (database resets) |
| User Accounts | ❌ Broken | Users don't persist |
| Bookings | ❌ Broken | Bookings don't persist |
| Media Uploads | ❌ Broken | Files don't persist |
| Movie Data | ❌ Broken | Movies don't persist |

---

## 🎭 Making It Work for Demo

### Option 1: Hardcode Demo Data in Views

Edit `movies/views.py` to show fake data:

```python
def movie_list(request):
    # Instead of querying database:
    # movies = Movie.objects.all()
    
    # Use hardcoded demo data:
    demo_movies = [
        {
            'id': 1,
            'name': 'The Shawshank Redemption',
            'genre': 'Drama',
            'language': 'English',
            'poster': '/static/demo/poster1.jpg'
        },
        {
            'id': 2,
            'name': 'The Dark Knight',
            'genre': 'Action',
            'language': 'English',
            'poster': '/static/demo/poster2.jpg'
        },
    ]
    
    return render(request, 'movies/movie_list.html', {
        'movies': demo_movies
    })
```

### Option 2: Use In-Memory SQLite (Lost on Every Request)

Edit `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # In-memory database
    }
}
```

### Option 3: Deploy to Render Instead ⭐ RECOMMENDED

Render supports persistent PostgreSQL databases for free.

See: `DEPLOY_TO_RENDER_NOW.md`

---

## 🔄 Redeployment

Every time you push to GitHub, Vercel auto-deploys:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Vercel auto-deploys in ~2 minutes
```

**Remember:** Database resets with every deployment!

---

## 💡 Recommendations

### For Demo/Portfolio Showcase:
1. ✅ Deploy to Vercel with SQLite
2. ✅ Use hardcoded demo data in views
3. ✅ Add screenshots/videos showing functionality
4. ✅ Include note: "Demo version - data resets"

### For Production/Real Users:
1. ❌ Do NOT use Vercel with SQLite
2. ✅ Deploy to **Render.com** with PostgreSQL
3. ✅ Get persistent database, storage, and cron jobs
4. ✅ Follow `DEPLOY_TO_RENDER_NOW.md` guide

---

## 📞 Support & Resources

- **Vercel Docs:** https://vercel.com/docs
- **Django on Vercel:** https://vercel.com/guides/deploying-django-with-vercel
- **Vercel CLI:** https://vercel.com/docs/cli
- **GitHub Repo:** https://github.com/venkyok/book-my-seat

---

## ✅ Summary

**What We Have:**
- ✅ SQLite configuration (no PostgreSQL)
- ✅ Vercel deployment files ready
- ✅ Static files configuration
- ✅ Environment variables setup

**What You Need to Do:**
1. Push code to GitHub
2. Import project on Vercel dashboard
3. Add environment variables (SECRET_KEY, DEBUG=False)
4. Deploy and test

**Expected Outcome:**
- ✅ App deploys successfully
- ⚠️ Database is empty (resets on every deployment)
- ⚠️ Admin panel won't work (no superuser)
- ✅ Good for demonstration purposes only

**For Real Deployment:**
- Use Render.com with PostgreSQL instead
- See `DEPLOY_TO_RENDER_NOW.md` for full production setup

---

**Ready to deploy?** Let's push to GitHub and configure Vercel! 🚀
