from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_booking_confirmation_email(user, bookings, theater):
    """
    Send booking confirmation email to user with ticket details.
    
    Args:
        user: User object who made the booking
        bookings: List of Booking objects
        theater: Theater object for the show
    """
    if not user.email:
        return False
    
    # Get booking details
    seats = [booking.seat.seat_number for booking in bookings]
    movie = bookings[0].movie if bookings else None
    
    # Email subject
    subject = f'Booking Confirmation - {movie.name}' if movie else 'Booking Confirmation'
    
    # Prepare context for email template
    context = {
        'user': user,
        'movie': movie,
        'theater': theater,
        'seats': seats,
        'seat_count': len(seats),
        'booking_time': bookings[0].booked_at if bookings else None,
        'bookings': bookings,
    }
    
    # Render HTML email
    html_content = render_to_string('emails/booking_confirmation.html', context)
    text_content = strip_tags(html_content)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bookmyseat.com',
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
