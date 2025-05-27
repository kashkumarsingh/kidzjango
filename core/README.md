Core App
The core app handles the core functionality of the Kidz Runz project, including booking management, email notifications, and admin configurations.
Structure

management/commands/: Management commands for tasks like sending test emails and updating booking statuses.
services/: Business logic for bookings (booking.py) and emails (email.py).
templates/core/: HTML templates for views and email notifications.
utils/: Utility functions for views (view_helpers.py).
forms.py: Django forms for user input validation.
models.py: Django models for FAQ, PricingPackage, Booking, and EmailConfiguration.
views.py: HTTP request handlers.
tests.py: Unit tests for models, services, and views.

Key Features

Create and cancel bookings with time-based restrictions.
Send email notifications to visitors and admins.
Update booking statuses via management commands.
Admin interface for managing FAQs, packages, bookings, and email configurations.

Usage

Booking a Package: Access /core/choose-package/<package_id>/ to book a package.
Cancel a Booking: Access /core/cancel/<reference_id>/ to cancel a booking.
Management Commands:
python manage.py sendtestmail <email>: Send a test email.
python manage.py update_booking_status: Update expired bookings.



Testing
Run tests with:
python manage.py test core

Security Notes

Ensure SECRET_KEY and email credentials are stored in .env.
CSRF protection is enabled for all forms.
Consider adding rate limiting to the bookings endpoint to prevent abuse.

