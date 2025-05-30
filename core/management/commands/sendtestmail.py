from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import EmailConfiguration
import logging
from core.services.email import EmailService

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends a test email using the configured SMTP settings.'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='?', default='admin@kidzrunz.com',
                            help='Email address to send the test email to (default: admin@kidzrunz.com)')

    def handle(self, *args, **options):
        email = options['email']
        try:
            EmailService.send_test_email(email)  # Placeholder; extend EmailService if needed
            logger.info(f"Test email sent successfully to {email}.")
            self.stdout.write(self.style.SUCCESS(f"Test email sent successfully to {email}."))
        except Exception as e:
            logger.error(f"Failed to send test email to {email}: {str(e)}")
            raise