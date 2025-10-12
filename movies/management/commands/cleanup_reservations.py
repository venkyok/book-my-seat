from django.core.management.base import BaseCommand
from django.utils import timezone
from movies.models import Booking


class Command(BaseCommand):
    help = 'Release expired seat reservations and delete pending bookings older than 5 minutes'

    def handle(self, *args, **options):
        """Clean up expired reservations and bookings"""
        count = Booking.release_expired_bookings()
        
        if count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully released {count} expired bookings and reservations')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No expired bookings found')
            )
