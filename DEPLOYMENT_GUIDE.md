# 🚀 DEPLOYMENT GUIDE - BookMySeat

## ✅ Pre-Deployment Status

**All bugs fixed and tested!** Your application is ready for deployment.

---

## 📦 QUICK START: Deploy to Render (Recommended)

### Step 1: Create Render Account
1. Go to https://render.com/
2. Sign up with GitHub account

### Step 2: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `bookmyseat-db`
3. Select free plan
4. Click "Create Database"
5. **COPY** the "Internal Database URL" (starts with `postgresql://`)

### Step 3: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `bookmyseat`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn bookmyseat.wsgi:application`

### Step 4: Set Environment Variables
In Render dashboard, add these environment variables:

```bash
# Required
SECRET_KEY=your-super-secret-random-key-here-generate-new-one
DEBUG=False
DATABASE_URL=<paste-your-postgres-url-from-step-2>
ALLOWED_HOSTS=your-app-name.onrender.com

# Email (Optional - use Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=BookMySeat <noreply@bookmyseat.com>

# Payment Gateway (Add when ready)
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### Step 5: Deploy!
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Visit your URL: `https://your-app-name.onrender.com`

### Step 6: Create Superuser
Use Render Shell:
```bash
python manage.py createsuperuser
```

---

## 🔐 GENERATE SECRET KEY

**Never use the default secret key in production!**

### Method 1: Python
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Method 2: Online
Go to: https://djecrety.ir/

Copy the generated key and use it as SECRET_KEY.

---

## 📧 EMAIL SETUP (Gmail)

### Step 1: Enable 2-Factor Authentication
1. Go to Google Account settings
2. Security → 2-Step Verification → Enable

### Step 2: Generate App Password
1. Security → App passwords
2. Select "Mail" and device
3. Copy 16-character password

### Step 3: Update Environment Variables
```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<16-character-app-password>
```

---

## 💳 PAYMENT GATEWAY SETUP

### Razorpay (For India)

1. **Sign up:** https://dashboard.razorpay.com/
2. Go to Settings → API Keys
3. Generate Test Keys (for testing)
4. Generate Live Keys (for production)
5. Add to environment variables:
```bash
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxx
```

### Important Notes:
- Test mode: Use test keys during development
- Live mode: Use live keys only after testing
- KYC required for live payments
- Test cards: https://razorpay.com/docs/payments/payments/test-card-details/

---

## 🔄 SETUP CRON JOB (Seat Cleanup)

### On Render:
1. Create new "Cron Job"
2. Name: `cleanup-reservations`
3. Command: `python manage.py cleanup_reservations`
4. Schedule: `*/1 * * * *` (every minute)

### On PythonAnywhere:
1. Go to Tasks tab
2. Add new task
3. Command: `python /path/to/manage.py cleanup_reservations`
4. Schedule: Every minute

---

## 🌐 ALTERNATIVE PLATFORMS

### Option 2: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Add PostgreSQL
railway add --plugin postgresql

# Set environment variables
railway variables set SECRET_KEY="your-key"
railway variables set DEBUG="False"

# Deploy
railway up
```

### Option 3: PythonAnywhere
1. Upload code via Git or file manager
2. Create virtual environment
3. Install requirements: `pip install -r requirements.txt`
4. Configure WSGI file
5. Set up database (MySQL or PostgreSQL)
6. Run migrations
7. Configure static files

---

## 📋 POST-DEPLOYMENT CHECKLIST

### Immediately After Deployment:

- [ ] Visit site and verify it loads
- [ ] Create superuser account
- [ ] Login to admin panel: `/admin/`
- [ ] Add at least one movie
- [ ] Add theaters with seats
- [ ] Test user registration
- [ ] Test login/logout
- [ ] Test seat selection
- [ ] Test reservation timeout (wait 5 minutes)
- [ ] Test payment flow (use test mode)
- [ ] Check email delivery
- [ ] Verify admin dashboard: `/movies/admin-dashboard/`
- [ ] Test all filters (genre, language)
- [ ] Check movie detail pages with trailers

### Within First Week:

- [ ] Monitor error logs
- [ ] Test with real users
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure backup schedule
- [ ] Add Google Analytics (optional)
- [ ] Test payment with real small amounts
- [ ] Optimize database queries
- [ ] Set up CDN for static files (optional)

---

## 🐛 TROUBLESHOOTING

### Issue: 500 Internal Server Error
**Solution:**
1. Check environment variables
2. Verify DATABASE_URL is set
3. Check logs: `python manage.py check --deploy`

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```
Make sure `STATIC_ROOT` is set.

### Issue: Database connection error
**Solution:**
- Verify DATABASE_URL format
- Check database is running
- Ensure migrations are applied

### Issue: Payment not working
**Solution:**
- Verify Razorpay keys are correct
- Check if using test vs live keys
- Look at browser console for JS errors

### Issue: Emails not sending
**Solution:**
- Verify EMAIL_HOST_PASSWORD is app password (not regular password)
- Check Gmail "Less secure app access" is enabled
- Test with console backend first

### Issue: Seat reservation not expiring
**Solution:**
- Ensure cron job is running
- Manually run: `python manage.py cleanup_reservations`
- Check server timezone settings

---

## 📊 MONITORING & MAINTENANCE

### Daily Checks:
- Monitor error rate
- Check payment success rate
- Review booking patterns

### Weekly Tasks:
- Database backup
- Clear old expired bookings
- Check disk space

### Monthly Tasks:
- Security updates: `pip list --outdated`
- Review analytics
- Optimize database
- Update dependencies

---

## 🔒 SECURITY BEST PRACTICES

### Must Do:
1. ✅ Never commit SECRET_KEY to Git
2. ✅ Always use environment variables
3. ✅ Set DEBUG=False in production
4. ✅ Use HTTPS (SSL certificate)
5. ✅ Regularly update dependencies
6. ✅ Enable CSRF protection (already done)
7. ✅ Use strong passwords
8. ✅ Regular database backups

### Recommended:
- Set up Web Application Firewall (WAF)
- Enable rate limiting
- Use Django security middleware
- Implement logging
- Set up error monitoring (Sentry)

---

## 📱 MOBILE APP CONSIDERATION

Your application is API-ready! To create a mobile app:

1. Add Django REST Framework
2. Create API endpoints
3. Use React Native or Flutter
4. Consume your backend APIs

---

## 💰 COST ESTIMATES

### Free Tier (Good for testing):
- **Render:** Free tier available (limited hours)
- **Railway:** $5 credit/month
- **PythonAnywhere:** Free tier available

### Paid Plans (For production):
- **Render:** Starting at $7/month
- **Railway:** Pay as you go (~$10-20/month)
- **PythonAnywhere:** Starting at $5/month
- **Heroku:** Starting at $7/month

### Additional Services:
- **Database:** Render PostgreSQL free tier (then $7/month)
- **Email:** Gmail free (SendGrid $15/month for 40k emails)
- **Payment Gateway:** Razorpay 2% per transaction

---

## 🎯 OPTIMIZATION TIPS

### Performance:
1. Enable database indexing (see DEPLOYMENT_READY.md)
2. Use Redis for caching
3. Optimize images (compress before upload)
4. Use CDN for static files
5. Enable Gzip compression

### SEO:
1. Add meta tags to templates
2. Create sitemap.xml
3. Add robots.txt
4. Submit to Google Search Console

### Conversion:
1. A/B test payment page
2. Optimize seat selection UX
3. Add reviews and ratings
4. Implement referral program

---

## 📞 SUPPORT

### Documentation:
- Django Docs: https://docs.djangoproject.com/
- Render Docs: https://render.com/docs
- Razorpay Docs: https://razorpay.com/docs/

### Your Project Files:
- `DEPLOYMENT_READY.md` - Bug fixes and checklist
- `SEAT_RESERVATION_DOCS.md` - Reservation feature guide
- `ADMIN_DASHBOARD_DOCS.md` - Dashboard documentation

---

## ✅ FINAL CHECKLIST BEFORE GO-LIVE

- [ ] All environment variables set
- [ ] Database configured and migrated
- [ ] Static files collected
- [ ] Secret key changed
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] Email tested and working
- [ ] Payment gateway in test mode
- [ ] Admin account created
- [ ] Sample data added
- [ ] All features tested
- [ ] Backup strategy in place
- [ ] Monitoring set up
- [ ] Domain configured (if custom)
- [ ] SSL certificate active

---

## 🎉 YOU'RE READY!

Your BookMySeat application is production-ready and fully tested. Follow this guide step-by-step, and you'll have a live application within 30 minutes!

**Good luck with your deployment! 🚀**

For issues or questions, refer to the documentation files included in your project.
