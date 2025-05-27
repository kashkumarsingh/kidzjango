from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Booking
import logging
from core.services.booking import BookingService

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Updates booking statuses to "expired" if the end date has passed.'

    def handle(self, *args, **options):
        updated_count = BookingService.update_expired_bookings()
        self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} bookings to expired status."))