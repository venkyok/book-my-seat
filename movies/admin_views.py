from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q, F, Avg
from django.utils import timezone
from datetime import timedelta
from .models import Booking, Movie, Theater, Seat
from django.contrib.auth.models import User
import json


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with comprehensive analytics"""
    
    # Get date range filter (default: last 30 days)
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # ========== REVENUE METRICS ==========
    # Total revenue (paid bookings only)
    total_revenue = Booking.objects.filter(
        payment_status='paid'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Revenue in selected period
    period_revenue = Booking.objects.filter(
        payment_status='paid',
        payment_date__gte=start_date
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Revenue by payment method
    revenue_by_method = Booking.objects.filter(
        payment_status='paid'
    ).values('payment_method').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')
    
    # Average ticket price
    avg_ticket_price = Booking.objects.filter(
        payment_status='paid'
    ).aggregate(avg=Avg('amount'))['avg'] or 0
    
    
    # ========== BOOKING METRICS ==========
    # Total bookings
    total_bookings = Booking.objects.filter(payment_status='paid').count()
    
    # Bookings in selected period
    period_bookings = Booking.objects.filter(
        payment_status='paid',
        payment_date__gte=start_date
    ).count()
    
    # Pending bookings (potential revenue)
    pending_bookings = Booking.objects.filter(payment_status='pending').count()
    pending_revenue = Booking.objects.filter(
        payment_status='pending'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Failed bookings
    failed_bookings = Booking.objects.filter(payment_status='failed').count()
    
    # Booking status breakdown
    booking_status = Booking.objects.values('payment_status').annotate(
        count=Count('id'),
        revenue=Sum('amount')
    ).order_by('-count')
    
    
    # ========== POPULAR MOVIES ==========
    # Most popular movies by bookings
    popular_movies = Booking.objects.filter(
        payment_status='paid'
    ).values(
        'movie__name',
        'movie__id',
        'movie__genre',
        'movie__language'
    ).annotate(
        total_bookings=Count('id'),
        revenue=Sum('amount')
    ).order_by('-total_bookings')[:10]
    
    # Movies with highest revenue
    top_revenue_movies = Booking.objects.filter(
        payment_status='paid'
    ).values(
        'movie__name',
        'movie__id'
    ).annotate(
        revenue=Sum('amount'),
        bookings=Count('id')
    ).order_by('-revenue')[:10]
    
    
    # ========== THEATER METRICS ==========
    # Busiest theaters
    busiest_theaters = Booking.objects.filter(
        payment_status='paid'
    ).values(
        'theater__name',
        'theater__id',
        'theater__movie__name'
    ).annotate(
        total_bookings=Count('id'),
        revenue=Sum('amount'),
        occupancy_rate=Count('seat') * 100.0 / Count('theater__seats', distinct=True)
    ).order_by('-total_bookings')[:10]
    
    # Theater revenue ranking
    theater_revenue = Booking.objects.filter(
        payment_status='paid'
    ).values(
        'theater__name',
        'theater__id'
    ).annotate(
        revenue=Sum('amount'),
        bookings=Count('id')
    ).order_by('-revenue')[:10]
    
    
    # ========== USER METRICS ==========
    # Total registered users
    total_users = User.objects.count()
    
    # Active users (made at least one booking)
    active_users = User.objects.filter(
        booking__payment_status='paid'
    ).distinct().count()
    
    # Top customers
    top_customers = User.objects.filter(
        booking__payment_status='paid'
    ).annotate(
        total_bookings=Count('booking'),
        total_spent=Sum('booking__amount')
    ).order_by('-total_spent')[:10]
    
    
    # ========== SEAT METRICS ==========
    # Total seats
    total_seats = Seat.objects.count()
    
    # Booked seats
    booked_seats = Seat.objects.filter(is_booked=True).count()
    
    # Reserved seats (temporary)
    reserved_seats = Seat.objects.filter(
        reserved_until__gt=timezone.now()
    ).count()
    
    # Available seats
    available_seats = total_seats - booked_seats - reserved_seats
    
    # Overall occupancy rate
    occupancy_rate = (booked_seats / total_seats * 100) if total_seats > 0 else 0
    
    
    # ========== GENRE & LANGUAGE ANALYTICS ==========
    # Popular genres
    genre_stats = Booking.objects.filter(
        payment_status='paid'
    ).values('movie__genre').annotate(
        bookings=Count('id'),
        revenue=Sum('amount')
    ).order_by('-bookings')
    
    # Popular languages
    language_stats = Booking.objects.filter(
        payment_status='paid'
    ).values('movie__language').annotate(
        bookings=Count('id'),
        revenue=Sum('amount')
    ).order_by('-bookings')
    
    
    # ========== TIME-BASED ANALYTICS ==========
    # Revenue trend (last 7 days)
    revenue_trend = []
    for i in range(6, -1, -1):
        day = timezone.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_revenue = Booking.objects.filter(
            payment_status='paid',
            payment_date__gte=day_start,
            payment_date__lt=day_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        day_bookings = Booking.objects.filter(
            payment_status='paid',
            payment_date__gte=day_start,
            payment_date__lt=day_end
        ).count()
        
        revenue_trend.append({
            'date': day_start.strftime('%b %d'),
            'revenue': float(day_revenue),
            'bookings': day_bookings
        })
    
    
    # ========== CONVERSION METRICS ==========
    # Conversion rate (paid / total bookings)
    total_all_bookings = Booking.objects.count()
    conversion_rate = (total_bookings / total_all_bookings * 100) if total_all_bookings > 0 else 0
    
    # Average time to payment (for paid bookings)
    paid_bookings_with_time = Booking.objects.filter(
        payment_status='paid',
        payment_date__isnull=False
    )
    
    
    context = {
        # Revenue
        'total_revenue': total_revenue,
        'period_revenue': period_revenue,
        'revenue_by_method': revenue_by_method,
        'avg_ticket_price': avg_ticket_price,
        
        # Bookings
        'total_bookings': total_bookings,
        'period_bookings': period_bookings,
        'pending_bookings': pending_bookings,
        'pending_revenue': pending_revenue,
        'failed_bookings': failed_bookings,
        'booking_status': booking_status,
        
        # Movies
        'popular_movies': popular_movies,
        'top_revenue_movies': top_revenue_movies,
        
        # Theaters
        'busiest_theaters': busiest_theaters,
        'theater_revenue': theater_revenue,
        
        # Users
        'total_users': total_users,
        'active_users': active_users,
        'top_customers': top_customers,
        
        # Seats
        'total_seats': total_seats,
        'booked_seats': booked_seats,
        'reserved_seats': reserved_seats,
        'available_seats': available_seats,
        'occupancy_rate': round(occupancy_rate, 2),
        
        # Genre & Language
        'genre_stats': genre_stats,
        'language_stats': language_stats,
        
        # Trends
        'revenue_trend': json.dumps(revenue_trend),
        
        # Conversion
        'conversion_rate': round(conversion_rate, 2),
        
        # Filter
        'selected_days': days,
    }
    
    return render(request, 'admin/dashboard.html', context)
