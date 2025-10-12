from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from .email_utils import send_booking_confirmation_email
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.utils import timezone

def movie_list(request):
    movies = Movie.objects.all()
    
    # Get filter parameters
    search_query = request.GET.get('search')
    genre_filter = request.GET.get('genre')
    language_filter = request.GET.get('language')
    
    # Apply search filter
    if search_query:
        movies = movies.filter(name__icontains=search_query)
    
    # Apply genre filter
    if genre_filter:
        movies = movies.filter(genre=genre_filter)
    
    # Apply language filter
    if language_filter:
        movies = movies.filter(language=language_filter)
    
    # Get all unique genres and languages for filter dropdowns
    genres = Movie.GENRE_CHOICES
    languages = Movie.LANGUAGE_CHOICES
    
    context = {
        'movies': movies,
        'genres': genres,
        'languages': languages,
        'selected_genre': genre_filter,
        'selected_language': language_filter,
    }
    
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    
    context = {
        'movie': movie,
        'theaters': theaters,
    }
    
    return render(request, 'movies/movie_detail.html', context)

def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theater=Theater.objects.filter(movie=movie)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})



@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theaters = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theaters)
    
    # Clean up expired reservations and bookings before showing seats
    Booking.release_expired_bookings()
    
    if request.method == 'POST':
        selected_Seats = request.POST.getlist('seats')
        error_seats = []
        pending_bookings = []
        reserved_seats = []
        
        if not selected_Seats:
            return render(request, "movies/seat_selection.html", {'theater': theaters, "seats": seats, 'error': "No seat selected"})
        
        # First, check availability and reserve seats
        for seat_id in selected_Seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
            
            # Check if seat is available
            if not seat.is_available():
                if seat.is_booked:
                    error_seats.append(f"{seat.seat_number} (booked)")
                else:
                    error_seats.append(f"{seat.seat_number} (reserved)")
                continue
            
            # Try to reserve the seat
            if seat.reserve(request.user, minutes=5):
                reserved_seats.append(seat)
            else:
                error_seats.append(f"{seat.seat_number} (unavailable)")
        
        if error_seats:
            error_message = f"The following seats are not available: {', '.join(error_seats)}"
            # Release any seats we reserved
            for seat in reserved_seats:
                seat.release_reservation()
            return render(request, 'movies/seat_selection.html', {'theater': theaters, "seats": seats, 'error': error_message})
        
        # Create pending bookings for reserved seats
        for seat in reserved_seats:
            try:
                booking = Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters,
                    payment_status='pending',
                    amount=250.00  # Default ticket price
                )
                pending_bookings.append(booking)
            except IntegrityError:
                error_seats.append(seat.seat_number)
                # Release the reservation
                seat.release_reservation()
        
        if error_seats:
            error_message = f"Error booking seats: {', '.join(error_seats)}"
            # Delete pending bookings and release reservations
            for booking in pending_bookings:
                booking.seat.release_reservation()
                booking.delete()
            return render(request, 'movies/seat_selection.html', {'theater': theaters, "seats": seats, 'error': error_message})
        
        if pending_bookings:
            # Store booking IDs in session for payment processing
            request.session['pending_booking_ids'] = [b.id for b in pending_bookings]
            request.session['theater_id'] = theater_id
            
            # Calculate total amount
            total_amount = sum([b.amount for b in pending_bookings])
            
            # Store reservation expiry time
            first_booking = pending_bookings[0]
            expiry_time = first_booking.booked_at + timezone.timedelta(minutes=5)
            request.session['reservation_expiry'] = expiry_time.isoformat()
            
            messages.success(request, f'Seats reserved for 5 minutes! Please complete payment.')
            
            # Redirect to payment page
            return redirect('payment_page')
        
    return render(request, 'movies/seat_selection.html', {'theaters': theaters, "seats": seats})


@login_required(login_url='/login/')
def payment_page(request):
    """Display payment options page"""
    booking_ids = request.session.get('pending_booking_ids', [])
    
    if not booking_ids:
        messages.error(request, 'No pending bookings found.')
        return redirect('movie_list')
    
    # Clean up expired bookings
    Booking.release_expired_bookings()
    
    bookings = Booking.objects.filter(id__in=booking_ids, user=request.user, payment_status='pending')
    
    if not bookings:
        messages.error(request, 'Booking session has expired. Please select seats again.')
        # Clear session
        request.session.pop('pending_booking_ids', None)
        request.session.pop('reservation_expiry', None)
        return redirect('movie_list')
    
    # Check if any booking has expired
    expired = False
    for booking in bookings:
        if booking.is_expired():
            expired = True
            break
    
    if expired:
        messages.error(request, 'Your seat reservation has expired. Please select seats again.')
        # Release all reservations and delete bookings
        for booking in bookings:
            booking.seat.release_reservation()
            booking.delete()
        # Clear session
        request.session.pop('pending_booking_ids', None)
        request.session.pop('reservation_expiry', None)
        return redirect('movie_list')
    
    total_amount = sum([b.amount for b in bookings])
    
    # Get reservation expiry time
    reservation_expiry = request.session.get('reservation_expiry')
    expiry_datetime = None
    if reservation_expiry:
        try:
            from dateutil import parser
            expiry_datetime = parser.isoparse(reservation_expiry)
        except (ImportError, ValueError):
            # Fallback: calculate from first booking if dateutil not available
            expiry_datetime = bookings[0].booked_at + timezone.timedelta(minutes=5)
    else:
        expiry_datetime = bookings[0].booked_at + timezone.timedelta(minutes=5)
    
    context = {
        'bookings': bookings,
        'total_amount': total_amount,
        'razorpay_key': getattr(settings, 'RAZORPAY_KEY_ID', 'your_razorpay_key'),
        'currency': 'INR',
        'reservation_expiry': expiry_datetime.isoformat(),
        'reservation_expiry_timestamp': int(expiry_datetime.timestamp() * 1000),  # For JavaScript
    }
    
    return render(request, 'movies/payment.html', context)


@csrf_exempt
@login_required(login_url='/login/')
def process_payment(request):
    """Process Razorpay payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_id = data.get('payment_id')
            payment_method = data.get('payment_method', 'razorpay')
            
            booking_ids = request.session.get('pending_booking_ids', [])
            
            if not booking_ids:
                return JsonResponse({'success': False, 'message': 'No pending bookings'})
            
            bookings = Booking.objects.filter(id__in=booking_ids, user=request.user, payment_status='pending')
            
            if not bookings:
                return JsonResponse({'success': False, 'message': 'No valid bookings found'})
            
            # Check if bookings have expired
            for booking in bookings:
                if booking.is_expired():
                    return JsonResponse({'success': False, 'message': 'Booking has expired'})
            
            # Update bookings as paid
            for booking in bookings:
                booking.payment_status = 'paid'
                booking.payment_id = payment_id
                booking.payment_method = payment_method
                booking.payment_date = timezone.now()
                booking.save()
                
                # Mark seat as permanently booked and clear reservation
                booking.seat.is_booked = True
                booking.seat.reserved_by = None
                booking.seat.reserved_until = None
                booking.seat.save()
            
            # Send confirmation email
            if bookings:
                theater = bookings[0].theater
                send_booking_confirmation_email(request.user, list(bookings), theater)
            
            # Clear session
            del request.session['pending_booking_ids']
            if 'theater_id' in request.session:
                del request.session['theater_id']
            if 'reservation_expiry' in request.session:
                del request.session['reservation_expiry']
            
            return JsonResponse({
                'success': True,
                'message': 'Payment successful!',
                'redirect_url': '/profile/'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required(login_url='/login/')
def payment_success(request):
    """Payment success page"""
    messages.success(request, 'Payment successful! Your tickets have been booked.')
    return redirect('profile')


@login_required(login_url='/login/')
def payment_failed(request):
    """Payment failed page - cancel pending bookings and release reservations"""
    booking_ids = request.session.get('pending_booking_ids', [])
    
    if booking_ids:
        bookings = Booking.objects.filter(id__in=booking_ids, user=request.user, payment_status='pending')
        
        # Release seat reservations and delete bookings
        for booking in bookings:
            booking.seat.release_reservation()
            booking.delete()
        
        # Clear session
        del request.session['pending_booking_ids']
        if 'theater_id' in request.session:
            del request.session['theater_id']
        if 'reservation_expiry' in request.session:
            del request.session['reservation_expiry']
    
    messages.error(request, 'Payment failed or was cancelled. Please try again.')
    return redirect('movie_list')




