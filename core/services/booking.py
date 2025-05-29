"""
Service layer for handling booking-related business logic.
Follows the Single Responsibility Principle by focusing solely on booking operations.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ..models import Booking, PricingPackage

class BookingService:
    @staticmethod
    def create_booking(package_id, name, email, phone, date_time, description=""):
        """
        Creates a new booking with the provided details, initially in 'pending_payment' status.

        Args:
            package_id (int): ID of the selected package.
            name (str): Visitor's full name.
            email (str): Visitor's email.
            phone (str): Visitor's phone number.
            date_time (str): Preferred date and time (ISO format).
            description (str): Additional information (optional).

        Returns:
            Booking: The created booking object.

        Raises:
            ObjectDoesNotExist: If the package with the given ID does not exist.
        """
        package = PricingPackage.objects.get(id=package_id)
        date_time_obj = timezone.datetime.strptime(date_time.replace('T', ' '), '%Y-%m-%d %H:%M')
        date_time_obj = timezone.make_aware(date_time_obj, timezone.get_current_timezone())
        booking = Booking.objects.create(
            package=package,
            name=name,
            email=email,
            phone=phone,
            date_time=date_time_obj,
            start_date=date_time_obj,
            description=description,
            status='pending_payment'
        )
        return booking

    @staticmethod
    def confirm_booking(booking, payment_intent_id):
        """
        Confirms a booking by updating its status and associating the payment intent.

        Args:
            booking (Booking): The booking object to confirm.
            payment_intent_id (str): Stripe Payment Intent ID.

        Returns:
            Booking: The confirmed booking object.
        """
        booking.status = 'completed'
        booking.payment_intent_id = payment_intent_id
        booking.save()
        return booking

    @staticmethod
    def fail_booking(booking):
        """
        Marks a booking as failed due to payment issues.

        Args:
            booking (Booking): The booking object to mark as failed.

        Returns:
            Booking: The updated booking object.
        """
        booking.status = 'failed'
        booking.save()
        return booking

    @staticmethod
    def cancel_booking(reference_id, current_time):
        """
        Cancels a booking if before the start date.

        Args:
            reference_id (uuid): Unique reference ID of the booking.
            current_time (datetime): Current time for comparison.

        Returns:
            Booking: The cancelled booking object.

        Raises:
            ObjectDoesNotExist: If the booking with the given reference_id does not exist.
            ValueError: If cancellation is not allowed (after start date).
        """
        booking = Booking.objects.get(reference_id=reference_id)
        if current_time >= booking.start_date:
            raise ValueError("Cannot cancel booking after the start date.")
        booking.status = 'cancelled'
        booking.save()
        return booking

    @staticmethod
    def update_expired_bookings():
        """
        Updates bookings to 'expired' if their end date has passed.

        Returns:
            int: Number of bookings updated.
        """
        current_time = timezone.now()
        bookings = Booking.objects.filter(status='completed', end_date__lt=current_time)
        updated_count = 0
        for booking in bookings:
            booking.status = 'expired'
            booking.save()
            updated_count += 1
        return updated_count