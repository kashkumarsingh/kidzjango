from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.utils import timezone
import logging
import uuid

logger = logging.getLogger(__name__)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_at']

class PricingPackage(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)  # e.g., "£125"
    description = models.TextField()
    features = HTMLField(
        help_text="Enter a formatted list of features with icons (e.g., <ul><li>🏃 Feature 1</li></ul>)")
    type = models.CharField(
        max_length=20,
        choices=[
            ('single', 'Single Session'),
            ('multi', 'Multi-Session')
        ],
        default='single'
    )
    duration_hours = models.PositiveIntegerField(
        default=3,
        help_text="Total hours of the package (e.g., 3 for single, 18 for Neptune)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-type']

class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(PricingPackage, on_delete=models.CASCADE)
    reference_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True,
        help_text="Unique reference ID for this booking"
    )
    name = models.CharField(max_length=255, help_text="Visitor's full name")
    email = models.EmailField(help_text="Visitor's email for confirmation")
    phone = models.CharField(max_length=20, help_text="Visitor's phone number")
    start_date = models.DateTimeField(
        null=True, blank=True, help_text="Set when booking is confirmed")
    end_date = models.DateTimeField(
        null=True, blank=True, help_text="Calculated as start_date + duration_hours")
    date_time = models.DateTimeField(
        null=True, blank=True, help_text="Initial appointment selection")
    description = models.TextField(
        blank=True, help_text="Allergies or special needs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('expired', 'Expired')],
        default='pending'
    )

    def save(self, *args, **kwargs):
        if self.start_date and not self.end_date and self.package and self.package.duration_hours:
            try:
                # Handle ISO format (e.g., '2025-05-23T12:08') or standard format
                if isinstance(self.start_date, str):
                    try:
                        self.start_date = timezone.datetime.strptime(self.start_date.replace('T', ' '), '%Y-%m-%d %H:%M').replace(second=0, microsecond=0, tzinfo=timezone.get_current_timezone())
                    except ValueError:
                        self.start_date = timezone.datetime.strptime(self.start_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.get_current_timezone())
                elif self.start_date and timezone.is_naive(self.start_date):
                    self.start_date = timezone.make_aware(self.start_date, timezone.get_current_timezone())
                self.end_date = self.start_date + timezone.timedelta(hours=self.package.duration_hours)
                logger.debug(f"Calculated end_date: {self.end_date} for booking {self.reference_id}")
            except (TypeError, ValueError) as e:
                logger.error(f"Error calculating end_date for booking {self.reference_id}: {str(e)}")
                self.end_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.reference_id} for {self.name} - {self.package.name} on {self.start_date}"

    class Meta:
        ordering = ['-created_at']

class EmailConfiguration(models.Model):
    host = models.CharField(max_length=255, help_text="Email host (e.g., sandbox.smtp.mailtrap.io)")
    port = models.PositiveIntegerField(help_text="Email port (e.g., 2525)")
    use_tls = models.BooleanField(default=True, help_text="Use TLS for email connection")
    username = models.CharField(max_length=255, help_text="Email username")
    password = models.CharField(max_length=255, help_text="Email password")
    default_from_email = models.EmailField(
        help_text="Default 'From' email address (e.g., noreply@kidzrunz.com)")
    admin_email = models.EmailField(
        help_text="Admin email address for notifications (e.g., admin@kidzrunz.com)")
    is_active = models.BooleanField(default=True, help_text="Activate this email configuration")

    @classmethod
    def get_active_config(cls):
        """Return the first active email configuration or use settings from environment variables."""
        config = cls.objects.filter(is_active=True).first()
        if config:
            return {
                'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_HOST': config.host,
                'EMAIL_PORT': config.port,
                'EMAIL_USE_TLS': config.use_tls,
                'EMAIL_HOST_USER': config.username,
                'EMAIL_HOST_PASSWORD': config.password,
                'DEFAULT_FROM_EMAIL': config.default_from_email,
                'ADMIN_EMAIL': config.admin_email,
            }
        else:
            logger.warning("No active EmailConfiguration found. Using settings from environment variables.")
            return {
                'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_HOST': config('EMAIL_HOST'),
                'EMAIL_PORT': config('EMAIL_PORT', default=587, cast=int),
                'EMAIL_USE_TLS': config('EMAIL_USE_TLS', default=True, cast=bool),
                'EMAIL_HOST_USER': config('EMAIL_HOST_USER'),
                'EMAIL_HOST_PASSWORD': config('EMAIL_HOST_PASSWORD'),
                'DEFAULT_FROM_EMAIL': config('DEFAULT_FROM_EMAIL', default='noreply@kidzrunz.com'),
                'ADMIN_EMAIL': config('ADMIN_EMAIL', default='admin@kidzrunz.com'),
            }

    def __str__(self):
        return f"Email Config - {self.host}:{self.port}"

    class Meta:
        verbose_name = "Email Configuration"
        verbose_name_plural = "Email Configurations"