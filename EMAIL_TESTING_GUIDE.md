# Quick Test Guide - Email Confirmation Feature

## Testing in Development (Console Email Backend)

The application is currently configured to print emails to the console/terminal instead of actually sending them. This is perfect for development and testing.

### How to Test:

1. **Make sure your server is running in a terminal window** (not in the background)
   ```powershell
   cd c:\Users\vy916\Desktop\django\djnago-bookmyshow-clone
   & "C:/Program Files/Python311/python.exe" manage.py runserver
   ```

2. **Log in to the application**
   - Go to http://127.0.0.1:8000/
   - Login with your account
   - Make sure your user account has an email address (update in Profile if needed)

3. **Make a booking**
   - Browse movies
   - Select a theater and show time
   - Choose your seats
   - Confirm the booking

4. **Check the terminal/console**
   - Go back to the terminal where the server is running
   - You'll see the email content printed there
   - It will look something like this:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Booking Confirmation - Movie Name
From: noreply@bookmyseat.com
To: user@example.com
Date: Sat, 12 Oct 2025 19:30:00 -0000
Message-ID: <...>

================================
BOOKING CONFIRMATION
================================

Dear username,

Thank you for booking with BookMySeat! Your booking has been confirmed.

MOVIE DETAILS
-------------
Movie: Movie Name
Genre: Action
Language: Hindi
Rating: 8.5/10

[... rest of the email ...]
```

5. **Check for success messages**
   - After booking, you'll see a success message on the web page
   - It will say: "Booking successful! Confirmation email sent to your@email.com"

## What You'll See

### On the Website:
- ✅ Green success alert: "Booking successful! Confirmation email sent to..."
- ℹ️ Blue info alert: "Please add your email to receive booking confirmations." (if no email)

### In the Console:
- Complete email with all booking details
- Movie information
- Theater and show time
- Seat numbers
- Booking timestamp

## Troubleshooting

### If you don't see the email in console:
1. Make sure the server is running in a visible terminal (not background)
2. Check that your user has an email address in their profile
3. Look for any error messages in the terminal
4. Make sure the booking was successful

### If booking fails:
1. Check if seats are already booked
2. Ensure you're logged in
3. Look for error messages on screen or in terminal

## Testing Tips

1. **Test with different scenarios:**
   - Single seat booking
   - Multiple seats booking
   - Booking when some seats are already taken
   - Booking with a user that has no email

2. **Verify email content:**
   - Check that all movie details are correct
   - Verify seat numbers match your selection
   - Confirm theater and show time are accurate

3. **Test the UI messages:**
   - Success messages appear after booking
   - Info messages when email is missing
   - Warning messages for partial bookings

## Ready for Production?

When you're ready to deploy and send real emails:

1. Update `bookmyseat/settings.py`
2. Change EMAIL_BACKEND to SMTP
3. Add your email service credentials
4. See `EMAIL_CONFIRMATION_GUIDE.md` for detailed instructions

Happy testing! 🎬📧
