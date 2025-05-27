from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from .models import PricingPackage, Booking
from .services.booking import BookingService
from .services.email import EmailService
from .utils.view_helpers import handle_view_error, require_post_method, fetch_object_or_error
from .forms import BookingForm
import logging

logger = logging.getLogger('core')

def choose_package(request, package_id):
    package = fetch_object_or_error(
        PricingPackage,
        f"Package {package_id} not found.",
        'frontend:bookings',
        id=package_id
    )
    if isinstance(package, HttpResponse):
        return package
    form = BookingForm(initial={'package_id': package_id})
    return render(request, 'core/choose_package.html', {'package': package, 'form': form})

def bookings(request):
    redirect_response = require_post_method(request, 'frontend:bookings')
    if redirect_response:
        return redirect_response

    form = BookingForm(request.POST)
    if not form.is_valid():
        package_id = request.POST.get('package_id')
        if not package_id:
            logger.error("No package_id provided in form submission.")
            return render(request, 'core/error.html', {
                'error': "No package selected. Please choose a package to book."
            }, status=400)
        try:
            package = PricingPackage.objects.get(id=package_id)
        except (PricingPackage.DoesNotExist, ValueError):
            logger.error(f"Package {package_id} not found during form validation.")
            return render(request, 'core/error.html', {
                'error': f"Package with ID {package_id} not found. Please select a valid package."
            }, status=404)
        return render(request, 'core/choose_package.html', {'package': package, 'form': form})

    try:
        booking = BookingService.create_booking(
            package_id=form.cleaned_data['package_id'],
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data['phone'],
            date_time=form.cleaned_data['date_time'].strftime('%Y-%m-%dT%H:%M'),
            description=form.cleaned_data['description']
        )
        EmailService.send_booking_confirmation(booking, request)
        EmailService.send_admin_notification(booking, request)
        logger.info(f"Booking created for {form.cleaned_data['name']} - Reference ID: {booking.reference_id}")
        return redirect('core:thank_you', reference_id=booking.reference_id)
    except Exception as e:
        return handle_view_error(f"Failed to process booking for {form.cleaned_data['name']}", e)

def thank_you(request, reference_id):
    booking = fetch_object_or_error(
        Booking,
        f"Booking with reference {reference_id} not found.",
        'frontend:home',
        reference_id=reference_id
    )
    if isinstance(booking, HttpResponse):
        return booking
    return render(request, 'core/thank_you.html', {'booking': booking})

def cancel_booking(request, reference_id):
    booking = fetch_object_or_error(
        Booking,
        f"Booking {reference_id} not found.",
        'frontend:home',
        reference_id=reference_id
    )
    if isinstance(booking, HttpResponse):
        return booking

    current_time = timezone.now()

    if request.method == 'POST':
        try:
            BookingService.cancel_booking(reference_id, current_time)
            EmailService.send_cancellation_confirmation(booking, request)
            EmailService.send_cancellation_notification(booking, request)
            logger.info(f"Booking {booking.reference_id} cancelled by visitor.")
            return redirect('frontend:home')
        except ValueError:
            return HttpResponseForbidden("Cannot cancel booking after the start date.")
        except Exception as e:
            return handle_view_error(f"Failed to cancel booking {reference_id}", e)

    return render(request, 'core/cancel_booking.html', {'booking': booking, 'current_time': current_time})