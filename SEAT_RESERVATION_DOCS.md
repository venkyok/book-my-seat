# Seat Reservation Timeout Feature

## Overview
This feature implements a temporary seat reservation system that holds selected seats for **5 minutes** during the payment process. If payment is not completed within this time, seats are automatically released back to the pool.

## How It Works

### 1. Seat Reservation Flow
```
User selects seats → Seats reserved for 5 minutes → Payment page with countdown
                                                    ↓
                          ← Payment completed → Seats permanently booked
                          ← Payment failed/timeout → Seats released
```

### 2. Model Changes

#### Seat Model
New fields added:
- `reserved_by` - ForeignKey to User (who reserved the seat)
- `reserved_until` - DateTime (when reservation expires)

New methods:
- `is_available()` - Checks if seat can be selected
- `reserve(user, minutes=5)` - Temporarily reserves seat for user
- `release_reservation()` - Clears temporary reservation
- `is_reserved_by(user)` - Checks if specific user has reservation

#### Booking Model
New methods:
- `is_expired()` - Checks if pending booking has expired
- `release_expired_bookings()` - Class method to clean up expired bookings

### 3. Reservation States

**Available Seat:**
- `is_booked = False`
- `reserved_by = None`
- `reserved_until = None`

**Reserved Seat (Temporary):**
- `is_booked = False`
- `reserved_by = User object`
- `reserved_until = Datetime (5 minutes from now)`

**Booked Seat (Permanent):**
- `is_booked = True`
- `reserved_by = None`
- `reserved_until = None`

### 4. Automatic Cleanup

**During User Actions:**
- When seat selection page loads - expired reservations are released
- When payment page loads - expired bookings are checked and released
- When payment is processed - validation ensures booking hasn't expired

**Manual Cleanup:**
Run the management command:
```bash
python manage.py cleanup_reservations
```

**Scheduled Cleanup (Production):**
Set up a cron job or task scheduler:
```bash
# Run every minute
* * * * * cd /path/to/project && python manage.py cleanup_reservations
```

Or use Django-cron, Celery, or APScheduler for periodic tasks.

## User Experience Features

### 1. Visual Indicators
**Seat Selection Page:**
- Green = Available
- Yellow/Orange = Reserved by another user
- Gray = Permanently booked

**Payment Page:**
- Countdown timer showing remaining time
- Warning alert (yellow) when > 1 minute remaining
- Danger alert (red) when < 1 minute remaining
- Auto-redirect when time expires

### 2. Messages
- Success: "Seats reserved for 5 minutes! Please complete payment."
- Error: "Booking session has expired. Please select seats again."
- Error: "The following seats are not available: A1 (reserved), A2 (booked)"

### 3. Protection Mechanisms
- Double-booking prevention via database integrity
- Race condition handling in seat selection
- Session management for pending bookings
- Automatic cleanup of expired data

## Admin Features

### Seat Admin
Enhanced list view shows:
- Seat number
- Theater
- Booking status (is_booked)
- Reservation status (is_reserved) - shows as boolean indicator
- Reserved by (username)
- Reserved until (expiry time)

### Booking Admin
Shows payment status and tracks:
- Pending bookings (awaiting payment)
- Paid bookings (completed)
- Failed bookings
- Refunded bookings

## Configuration

### Timeout Duration
Default: **5 minutes**

To change, update in these locations:

1. **Seat.reserve() method** (models.py):
```python
def reserve(self, user, minutes=5):  # Change the default here
```

2. **Booking expiry check** (models.py):
```python
expiry_threshold = timezone.now() - timedelta(minutes=5)  # Change here
```

3. **View timeout calculation** (views.py):
```python
expiry_time = first_booking.booked_at + timezone.timedelta(minutes=5)  # And here
```

4. **User message** (views.py):
```python
messages.success(request, f'Seats reserved for 5 minutes!')  # Update message
```

## Testing

### Test Scenarios

1. **Normal Flow:**
   - Select seats → See 5-minute countdown → Complete payment → Seats confirmed

2. **Timeout Scenario:**
   - Select seats → Wait 5+ minutes → See expiry message → Redirected to movie list

3. **Multiple Users:**
   - User A selects seat A1
   - User B tries to select A1 → Should show as reserved/unavailable
   - User A doesn't pay, timeout occurs
   - User B refreshes → A1 now available

4. **Payment Failure:**
   - Select seats → Start payment → Cancel → Seats released immediately

5. **Concurrent Requests:**
   - Two users try to book same seat simultaneously
   - Only one succeeds, other gets error

### Manual Testing Commands

```bash
# Check current reservations
python manage.py shell
>>> from movies.models import Seat
>>> Seat.objects.filter(reserved_by__isnull=False)

# Clean up expired reservations
python manage.py cleanup_reservations

# Check pending bookings
>>> from movies.models import Booking
>>> Booking.objects.filter(payment_status='pending')
```

## Production Deployment Checklist

- [ ] Set up periodic cleanup task (cron/celery)
- [ ] Configure proper timezone settings
- [ ] Test timeout duration with real users
- [ ] Monitor database for orphaned reservations
- [ ] Add logging for reservation operations
- [ ] Consider adding email notification before timeout
- [ ] Implement seat reservation analytics
- [ ] Add admin action to bulk release reservations

## Future Enhancements

1. **Configurable Timeout:** Allow different timeout durations per movie/theater
2. **Grace Period:** Add 30-second grace period before hard expiry
3. **Email Notifications:** Warn users at 1-minute remaining
4. **Reservation Extension:** Allow users to extend reservation once
5. **Priority Queue:** VIP users get longer reservation time
6. **Analytics:** Track conversion rate from reservation to booking
7. **Real-time Updates:** WebSocket notifications for seat availability changes

## Troubleshooting

**Problem:** Seats stay reserved forever
**Solution:** Run `python manage.py cleanup_reservations` or check `reserved_until` values

**Problem:** Timer not showing on payment page
**Solution:** Check if `reservation_expiry_timestamp` is passed in context

**Problem:** Users getting timeout errors immediately
**Solution:** Verify server timezone matches `timezone.now()` calculations

**Problem:** Multiple users booking same seat
**Solution:** Check database constraints on Booking.seat (OneToOneField)

## Technical Notes

- Uses Django's `timezone.now()` for timezone-aware datetime
- Reservation time stored as ISO format in session
- JavaScript countdown syncs with server time
- No external dependencies required (pure Django)
- Compatible with SQLite, PostgreSQL, MySQL
