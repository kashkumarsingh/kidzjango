"""
Service layer for handling email-related business logic.
Follows the Single Responsibility Principle by focusing solely on email operations.
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from ..models import EmailConfiguration

class EmailService:
    @staticmethod
    def send_booking_confirmation(booking, request):
        """
        Sends a booking confirmation email to the visitor.

        Args:
            booking (Booking): The booking object.
            request: The HTTP request object for URL generation.

        Returns:
            None
        """
        email_config = EmailConfiguration.get_active_config()
        subject = 'Kidz Runz Booking Confirmation'
        html_message = render_to_string('core/email_visitor_confirmation.html', {'booking': booking, 'request': request})
        text_message = render_to_string('core/email_visitor_confirmation.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
        email = EmailMultiAlternatives(
            subject, text_message, email_config['DEFAULT_FROM_EMAIL'], [booking.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

    @staticmethod
    def send_admin_notification(booking, request):
        """
        Sends a new booking notification to the admin.

        Args:
            booking (Booking): The booking object.
            request: The HTTP request object for URL generation.

        Returns:
            None
        """
        email_config = EmailConfiguration.get_active_config()
        subject = 'New Booking Notification - Kidz Runz'
        html_message = render_to_string('core/email_admin_notification.html', {'booking': booking, 'request': request})
        text_message = render_to_string('core/email_admin_notification.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
        email = EmailMultiAlternatives(
            subject, text_message, email_config['DEFAULT_FROM_EMAIL'], [email_config['ADMIN_EMAIL']]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

    @staticmethod
    def send_cancellation_confirmation(booking, request):
        """
        Sends a cancellation confirmation email to the visitor.

        Args:
            booking (Booking): The booking object.
            request: The HTTP request object for URL generation.

        Returns:
            None
        """
        email_config = EmailConfiguration.get_active_config()
        subject = 'Kidz Runz Booking Cancellation Confirmation'
        html_message = render_to_string('core/email_visitor_cancellation.html', {'booking': booking, 'request': request})
        text_message = render_to_string('core/email_visitor_cancellation.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
        email = EmailMultiAlternatives(
            subject, text_message, email_config['DEFAULT_FROM_EMAIL'], [booking.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

    @staticmethod
    def send_cancellation_notification(booking, request):
        """
        Sends a cancellation notification to the admin.

        Args:
            booking (Booking): The booking object.
            request: The HTTP request object for URL generation.

        Returns:
            None
        """
        email_config = EmailConfiguration.get_active_config()
        subject = 'Booking Cancellation Notification - Kidz Runz'
        html_message = render_to_string('core/email_admin_cancellation.html', {'booking': booking, 'request': request})
        text_message = render_to_string('core/email_admin_cancellation.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
        email = EmailMultiAlternatives(
            subject, text_message, email_config['DEFAULT_FROM_EMAIL'], [email_config['ADMIN_EMAIL']]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

    @staticmethod
    def send_test_email(recipient):
        """
        Sends a test email using the configured SMTP settings.

        Args:
            recipient (str): Email address to send the test email to.

        Returns:
            None
        """
        email_config = EmailConfiguration.get_active_config()
        send_mail(
            'Test Email from Kidz Runz',
            'This is a test email from Kidz Runz.',
            email_config['DEFAULT_FROM_EMAIL'],
            [recipient],
            fail_silently=False,
        )