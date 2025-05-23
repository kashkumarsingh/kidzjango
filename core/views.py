from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponseServerError, HttpResponseForbidden
from .models import PricingPackage, Booking, EmailConfiguration
from django.utils import timezone
import logging
import traceback

logger = logging.getLogger('core')

def choose_package(request, package_id):
    package = get_object_or_404(PricingPackage, id=package_id)
    return render(request, 'core/choose_package.html', {'package': package})

def bookings(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        package = get_object_or_404(PricingPackage, id=package_id)

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_time = request.POST.get('date_time')
        description = request.POST.get('description', '')

        # Convert date_time to timezone-aware datetime
        if date_time:
            date_time_obj = timezone.datetime.strptime(date_time.replace('T', ' '), '%Y-%m-%d %H:%M')
            date_time_obj = timezone.make_aware(date_time_obj, timezone.get_current_timezone())

        # Create the booking
        booking = Booking.objects.create(
            package=package,
            name=name,
            email=email,
            phone=phone,
            date_time=date_time_obj,
            description=description,
            start_date=date_time_obj,
            status='completed'
        )

        try:
            # Get dynamic email configuration
            email_config = EmailConfiguration.get_active_config()

            # Send email to visitor
            visitor_subject = 'Kidz Runz Booking Confirmation'
            visitor_html_message = render_to_string('core/email_visitor_confirmation.html', {'booking': booking, 'request': request})
            visitor_text_message = render_to_string('core/email_visitor_confirmation.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
            email = EmailMultiAlternatives(
                visitor_subject,
                visitor_text_message,
                email_config['DEFAULT_FROM_EMAIL'],
                [email]
            )
            email.attach_alternative(visitor_html_message, "text/html")
            email.send()

            # Send email to admin
            admin_subject = 'New Booking Notification - Kidz Runz'
            admin_html_message = render_to_string('core/email_admin_notification.html', {'booking': booking, 'request': request})
            admin_text_message = render_to_string('core/email_admin_notification.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
            admin_email = EmailMultiAlternatives(
                admin_subject,
                admin_text_message,
                email_config['DEFAULT_FROM_EMAIL'],
                [email_config['ADMIN_EMAIL']]
            )
            admin_email.attach_alternative(admin_html_message, "text/html")
            admin_email.send()

            logger.info(f"Booking created for {name} - Reference ID: {booking.reference_id}")
        except ValueError as e:
            logger.error(f"Failed to send email for booking {booking.reference_id} due to configuration error: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to send email for booking {booking.reference_id}: {str(e)}\n{traceback.format_exc()}")
            return HttpResponseServerError(f"An error occurred while sending the email for booking {booking.reference_id}. Please contact the administrator.")

        return redirect('core:thank_you', booking_id=booking.id)

    return redirect('frontend:bookings')

def thank_you(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'core/thank_you.html', {'booking': booking})

def cancel_booking(request, reference_id):
    booking = get_object_or_404(Booking, reference_id=reference_id)
    current_time = timezone.now()

    if request.method == 'POST':
        if current_time < booking.start_date:
            booking.status = 'expired'  # Changed from 'cancelled' to 'expired'
            booking.save()
            
            # Send cancellation confirmation to visitor
            email_config = EmailConfiguration.get_active_config()
            visitor_subject = 'Kidz Runz Booking Cancellation Confirmation'
            visitor_html_message = render_to_string('core/email_visitor_cancellation.html', {'booking': booking, 'request': request})
            visitor_text_message = render_to_string('core/email_visitor_cancellation.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
            email = EmailMultiAlternatives(
                visitor_subject,
                visitor_text_message,
                email_config['DEFAULT_FROM_EMAIL'],
                [booking.email]
            )
            email.attach_alternative(visitor_html_message, "text/html")
            email.send()
            
            # Send cancellation notification to admin
            admin_subject = 'Booking Cancellation Notification - Kidz Runz'
            admin_html_message = render_to_string('core/email_admin_cancellation.html', {'booking': booking, 'request': request})
            admin_text_message = render_to_string('core/email_admin_cancellation.html', {'booking': booking, 'request': request}, request=None).replace('<[^>]+>', '')
            admin_email = EmailMultiAlternatives(
                admin_subject,
                admin_text_message,
                email_config['DEFAULT_FROM_EMAIL'],
                [email_config['ADMIN_EMAIL']]
            )
            admin_email.attach_alternative(admin_html_message, "text/html")
            admin_email.send()

            logger.info(f"Booking {booking.reference_id} cancelled by visitor.")
            return redirect('frontend:home')
        else:
            return HttpResponseForbidden("Cannot cancel booking after the start date.")

    return render(request, 'core/cancel_booking.html', {'booking': booking, 'current_time': current_time})