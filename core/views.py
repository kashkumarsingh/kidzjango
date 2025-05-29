from django.shortcuts import redirect, render
# from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.conf import settings
from .models import PricingPackage, Booking
from .services.booking import BookingService
from .services.email import EmailService
from .services.payment import PaymentService
from .utils.view_helpers import handle_view_error, require_post_method, fetch_object_or_error
from .forms import BookingForm
import logging
import stripe

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

    # Check if there's an existing pending_payment booking for this session
    initial_data = {'package_id': package_id}
    if 'booking_reference_id' in request.session:
        try:
            existing_booking = Booking.objects.get(
                reference_id=request.session['booking_reference_id'],
                status='pending_payment'
            )
            initial_data.update({
                'name': existing_booking.name,
                'email': existing_booking.email,
                'phone': existing_booking.phone,
                'date_time': existing_booking.date_time,
                'description': existing_booking.description,
            })
        except Booking.DoesNotExist:
            # Clear the session if the booking doesn't exist or isn't pending_payment
            if 'booking_reference_id' in request.session:
                del request.session['booking_reference_id']

    form = BookingForm(initial=initial_data)
    return render(request, 'core/choose_package.html', {'package': package, 'form': form})
# @ratelimit(key='ip', rate='10/m', method='POST', block=True)
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
        # Check if there's an existing booking in the session
        if 'booking_reference_id' in request.session:
            try:
                booking = Booking.objects.get(
                    reference_id=request.session['booking_reference_id'],
                    status='pending_payment'
                )
                # Update existing booking
                booking.name = form.cleaned_data['name']
                booking.email = form.cleaned_data['email']
                booking.phone = form.cleaned_data['phone']
                booking.date_time = timezone.datetime.strptime(
                    form.cleaned_data['date_time'].strftime('%Y-%m-%dT%H:%M').replace('T', ' '),
                    '%Y-%m-%d %H:%M'
                )
                booking.date_time = timezone.make_aware(booking.date_time, timezone.get_current_timezone())
                booking.start_date = booking.date_time
                booking.description = form.cleaned_data['description']
                booking.save()
            except Booking.DoesNotExist:
                # If the booking doesn't exist, create a new one
                booking = BookingService.create_booking(
                    package_id=form.cleaned_data['package_id'],
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    date_time=form.cleaned_data['date_time'].strftime('%Y-%m-%dT%H:%M'),
                    description=form.cleaned_data['description']
                )
        else:
            booking = BookingService.create_booking(
                package_id=form.cleaned_data['package_id'],
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                date_time=form.cleaned_data['date_time'].strftime('%Y-%m-%dT%H:%M'),
                description=form.cleaned_data['description']
            )

        # Store booking reference in session
        request.session['booking_reference_id'] = str(booking.reference_id)
        logger.info(f"Booking created/updated (pending payment) for {form.cleaned_data['name']} - Reference ID: {booking.reference_id}")
        return redirect('core:process_payment', reference_id=booking.reference_id)
    except Exception as e:
        return handle_view_error(f"Failed to process booking for {form.cleaned_data['name']}", e)
# @ratelimit(key='ip', rate='5/m', method='POST', block=True)
def process_payment(request, reference_id):
    booking = fetch_object_or_error(
        Booking,
        f"Booking with reference {reference_id} not found.",
        'frontend:home',
        reference_id=reference_id
    )
    if isinstance(booking, HttpResponse):
        return booking

    # Allow processing for both 'pending_payment' and 'failed' statuses
    if booking.status not in ['pending_payment', 'failed']:
        logger.warning(f"Booking {reference_id} is not in pending_payment or failed status. Current status: {booking.status}")
        return render(request, 'core/error.html', {
            'error': "This booking cannot be paid for at this time."
        }, status=400)

    # Calculate amount in pence (e.g., "£125" -> 12500)
    try:
        price = float(booking.package.price.replace("£", "").strip())
        amount = int(price * 100)
    except (ValueError, AttributeError) as e:
        logger.error(f"Invalid package price format for booking {reference_id}: {str(e)}")
        return render(request, 'core/error.html', {
            'error': "Invalid package price. Please contact support."
        }, status=500)

    if request.method == 'GET' or (request.method == 'POST' and request.POST.get('retry_payment') == 'true'):
        try:
            logger.debug(f"Stripe Publishable Key: {settings.STRIPE_PUBLISHABLE_KEY}")
            # If retrying, cancel the old Payment Intent if it exists
            if booking.payment_intent_id and request.POST.get('retry_payment') == 'true':
                try:
                    stripe.PaymentIntent.cancel(booking.payment_intent_id)
                    logger.info(f"Cancelled old Payment Intent {booking.payment_intent_id} for booking {reference_id}")
                except stripe.error.StripeError as e:
                    logger.warning(f"Failed to cancel old Payment Intent {booking.payment_intent_id}: {str(e)}")

            # Create a new Payment Intent
            payment_intent = PaymentService.create_payment_intent(
                amount=amount,
                metadata={'booking_reference_id': str(booking.reference_id)}
            )
            # Store payment intent ID in booking
            booking.payment_intent_id = payment_intent.id
            # Reset status to pending_payment if retrying
            if booking.status == 'failed':
                booking.status = 'pending_payment'
            booking.save()
            return render(request, 'core/payment.html', {
                'booking': booking,
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                'client_secret': payment_intent.client_secret,
                'error': None
            })
        except Exception as e:
            logger.error(f"Failed to create payment intent for booking {reference_id}: {str(e)}")
            return render(request, 'core/payment.html', {
                'booking': booking,
                'error': "Failed to initialize payment. Please try again."
            })

    elif request.method == 'POST':
        try:
            # Retrieve the Payment Intent to check its status
            payment_intent = stripe.PaymentIntent.retrieve(booking.payment_intent_id)
            if payment_intent.status == 'succeeded':
                PaymentService.validate_payment_amount(booking.package.price, payment_intent.amount)
                booking = BookingService.confirm_booking(booking, payment_intent.id)
                EmailService.send_booking_confirmation(booking, request)
                EmailService.send_admin_notification(booking, request)
                # Clear session after successful payment
                if 'booking_reference_id' in request.session:
                    del request.session['booking_reference_id']
                logger.info(f"Payment successful for booking {reference_id}. Booking confirmed.")
                return redirect('core:thank_you', reference_id=booking.reference_id)
            else:
                # Mark booking as failed
                BookingService.fail_booking(booking)
                # Clear session after payment failure
                if 'booking_reference_id' in request.session:
                    del request.session['booking_reference_id']
                logger.warning(f"Payment Intent {payment_intent.id} not succeeded for booking {reference_id}. Status: {payment_intent.status}. Booking marked as failed.")
                return render(request, 'core/payment.html', {
                    'booking': booking,
                    'error': "Payment failed. Please retry with a different payment method."
                })
        except Exception as e:
            # Mark booking as failed on exception
            BookingService.fail_booking(booking)
            # Clear session after payment failure
            if 'booking_reference_id' in request.session:
                del request.session['booking_reference_id']
            logger.error(f"Payment processing failed for booking {reference_id}: {str(e)}. Booking marked as failed.")
            return render(request, 'core/payment.html', {
                'booking': booking,
                'error': "Payment processing failed. Please retry with a different payment method."
            })

def thank_you(request, reference_id):
    booking = fetch_object_or_error(
        Booking,
        f"Booking with reference {reference_id} not found.",
        'frontend:home',
        reference_id=reference_id
    )
    if isinstance(booking, HttpResponse):
        return booking
    if booking.status != 'completed':
        logger.warning(f"Booking {reference_id} accessed thank you page but status is {booking.status}.")
        return redirect('frontend:home')
    # Clear session when viewing thank you page to prevent reuse
    if 'booking_reference_id' in request.session:
        del request.session['booking_reference_id']
    return render(request, 'core/thank_you.html', {'booking': booking})
# @ratelimit(key='ip', rate='5/m', method='POST', block=True)
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
            # Clear session if cancelling
            if 'booking_reference_id' in request.session:
                del request.session['booking_reference_id']
            logger.info(f"Booking {booking.reference_id} cancelled by visitor.")
            return redirect('frontend:home')
        except ValueError:
            return HttpResponseForbidden("Cannot cancel booking after the start date.")
        except Exception as e:
            return handle_view_error(f"Failed to cancel booking {reference_id}", e)

    return render(request, 'core/cancel_booking.html', {'booking': booking, 'current_time': current_time})

def clear_session(request):
    if request.method == 'POST':
        if 'booking_reference_id' in request.session:
            del request.session['booking_reference_id']
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)