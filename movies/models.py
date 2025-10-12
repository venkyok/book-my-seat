from django.db import models
from django.contrib.auth.models import User 


class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('sci-fi', 'Sci-Fi'),
        ('adventure', 'Adventure'),
        ('animation', 'Animation'),
        ('crime', 'Crime'),
    ]
    
    LANGUAGE_CHOICES = [
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('tamil', 'Tamil'),
        ('telugu', 'Telugu'),
        ('malayalam', 'Malayalam'),
        ('kannada', 'Kannada'),
        ('bengali', 'Bengali'),
        ('marathi', 'Marathi'),
    ]
    
    name= models.CharField(max_length=255)
    image= models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    cast= models.TextField()
    description= models.TextField(blank=True,null=True) # optional
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='action')
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default='english')
    trailer_url = models.URLField(max_length=500, blank=True, null=True, help_text="YouTube video URL or embed code")

    def __str__(self):
        return self.name
    
    def get_youtube_embed_url(self):
        """Convert YouTube URL to embed URL"""
        if not self.trailer_url:
            return None
        
        # Handle different YouTube URL formats
        if 'youtube.com/watch?v=' in self.trailer_url:
            video_id = self.trailer_url.split('watch?v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in self.trailer_url:
            video_id = self.trailer_url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtube.com/embed/' in self.trailer_url:
            return self.trailer_url
        else:
            return None

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theaters')
    time= models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked=models.BooleanField(default=False)
    
    # Temporary reservation fields
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reserved_seats')
    reserved_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'
    
    def is_available(self):
        """Check if seat is available (not booked and not temporarily reserved)"""
        from django.utils import timezone
        
        # If permanently booked, not available
        if self.is_booked:
            return False
        
        # If reserved and reservation hasn't expired, not available
        if self.reserved_until and self.reserved_until > timezone.now():
            return False
        
        # If reservation expired, clear it and mark as available
        if self.reserved_until and self.reserved_until <= timezone.now():
            self.release_reservation()
            return True
        
        return True
    
    def reserve(self, user, minutes=5):
        """Temporarily reserve seat for a user"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.is_available():
            self.reserved_by = user
            self.reserved_until = timezone.now() + timedelta(minutes=minutes)
            self.save()
            return True
        return False
    
    def release_reservation(self):
        """Release temporary reservation"""
        self.reserved_by = None
        self.reserved_until = None
        self.save()
    
    def is_reserved_by(self, user):
        """Check if seat is reserved by specific user"""
        from django.utils import timezone
        return (self.reserved_by == user and 
                self.reserved_until and 
                self.reserved_until > timezone.now())

class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    seat=models.OneToOneField(Seat,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE)
    booked_at=models.DateTimeField(auto_now_add=True)
    
    # Payment fields
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)  # razorpay, stripe, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=250.00)  # Ticket price
    currency = models.CharField(max_length=10, default='INR')
    payment_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name} - {self.payment_status}'
    
    def is_expired(self):
        """Check if pending booking has expired (5 minutes timeout)"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.payment_status == 'pending':
            expiry_time = self.booked_at + timedelta(minutes=5)
            return timezone.now() > expiry_time
        return False
    
    @classmethod
    def release_expired_bookings(cls):
        """Release all expired pending bookings and their seat reservations"""
        from django.utils import timezone
        from datetime import timedelta
        
        expiry_threshold = timezone.now() - timedelta(minutes=5)
        expired_bookings = cls.objects.filter(
            payment_status='pending',
            booked_at__lt=expiry_threshold
        )
        
        count = 0
        for booking in expired_bookings:
            # Release seat reservation
            if booking.seat.reserved_by == booking.user:
                booking.seat.release_reservation()
            # Delete expired booking
            booking.delete()
            count += 1
        
        return count
    
    class Meta:
        ordering = ['-booked_at']