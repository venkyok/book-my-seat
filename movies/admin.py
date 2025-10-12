from django.contrib import admin
from .models import Movie, Theater, Seat,Booking
from django.urls import reverse
from django.utils.html import format_html

# Customize admin site
admin.site.site_header = "BookMySeat Administration"
admin.site.site_title = "BookMySeat Admin"
admin.site.index_title = "Welcome to BookMySeat Admin Panel"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'genre', 'language', 'cast', 'has_trailer']
    list_filter = ['genre', 'language', 'rating']
    search_fields = ['name', 'cast', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'image', 'rating')
        }),
        ('Movie Details', {
            'fields': ('genre', 'language', 'cast', 'description')
        }),
        ('Media', {
            'fields': ('trailer_url',),
            'description': 'Add YouTube trailer URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)'
        }),
    )
    
    def has_trailer(self, obj):
        return bool(obj.trailer_url)
    has_trailer.boolean = True
    has_trailer.short_description = 'Trailer'

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'is_booked', 'is_reserved', 'reserved_by', 'reserved_until']
    list_filter = ['is_booked', 'theater']
    search_fields = ['seat_number', 'theater__name']
    readonly_fields = ['reserved_by', 'reserved_until']
    
    def is_reserved(self, obj):
        from django.utils import timezone
        if obj.reserved_until and obj.reserved_until > timezone.now():
            return True
        return False
    is_reserved.boolean = True
    is_reserved.short_description = 'Reserved'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie', 'theater', 'payment_status', 'amount', 'booked_at']
    list_filter = ['payment_status', 'payment_method', 'booked_at']
    search_fields = ['user__username', 'payment_id', 'seat__seat_number']
    readonly_fields = ['booked_at', 'payment_date']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'movie', 'theater', 'seat', 'booked_at')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_method', 'payment_id', 'amount', 'currency', 'payment_date')
        }),
    )
