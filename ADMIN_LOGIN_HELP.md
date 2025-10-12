# Django Admin Login Help

## ✅ You Already Have an Admin Account!

**Username:** `girish`
**Email:** `girishmaharana42@gmail.com`

## 🔑 If You Forgot the Password:

### Option 1: Reset Password for Existing User

Run this command in a NEW terminal (don't close the server):

```powershell
cd c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone
& "C:/Program Files/Python311/python.exe" manage.py changepassword girish
```

Then follow the prompts to set a new password.

### Option 2: Create a New Superuser

Run this command in a NEW terminal:

```powershell
cd c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone
& "C:/Program Files/Python311/python.exe" manage.py createsuperuser
```

Follow the prompts:
- Username: (choose a new username, e.g., "admin")
- Email: (your email)
- Password: (choose a password)
- Password (again): (confirm password)

## 📋 Quick Steps to Access Admin:

1. **Keep the server running** (don't close the current terminal)
2. **Open a NEW PowerShell window**
3. **Run one of the commands above** to reset/create password
4. **Go to**: http://127.0.0.1:8000/admin/
5. **Login** with your credentials

## ⚠️ Important Notes:

- **Password must be at least 8 characters**
- **Cannot be too similar to username**
- **Cannot be entirely numeric**
- **Username and password are case-sensitive**

## 🎯 After Logging In:

1. Click **"Movies"** in the sidebar
2. Click on any movie (e.g., "avengers")
3. Scroll to **"Media"** section
4. Add YouTube URL in **"Trailer url"** field:
   ```
   https://www.youtube.com/watch?v=TcMBFSGVi1c
   ```
5. Click **"Save"**
6. Visit http://127.0.0.1:8000/movies/1/ to see the trailer!

---

**Need to reset password? Open a new terminal and run the changepassword command!**
