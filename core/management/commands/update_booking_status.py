from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Booking
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updates booking statuses to "expired" if the end date has passed.'

    def handle(self, *args, **options):
        current_time = timezone.now()
        bookings = Booking.objects.filter(status='completed', end_date__lt=current_time)

        updated_count = 0
        for booking in bookings:
            booking.status = 'expired'
            booking.save()
            updated_count += 1
            logger.info(f"Updated booking {booking.reference_id} to expired status.")

        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} bookings to expired status."))