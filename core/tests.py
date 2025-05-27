from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import FAQ, PricingPackage, Booking
from .services.booking import BookingService
from .services.email import EmailService

class FAQModelTest(TestCase):
    def setUp(self):
        FAQ.objects.create(
            question="What are your hours?",
            answer="We are open from 9 AM to 5 PM."
        )

    def test_faq_str(self):
        faq = FAQ.objects.get(question="What are your hours?")
        self.assertEqual(str(faq), "What are your hours?")

class PricingPackageModelTest(TestCase):
    def setUp(self):
        PricingPackage.objects.create(
            name="Basic Package",
            price="£125",
            description="Basic mentoring package",
            features="<ul><li>🏃 Feature 1</li><li>🌟 Feature 2</li></ul>",
            type="single"
        )

    def test_pricing_package_str(self):
        package = PricingPackage.objects.get(name="Basic Package")
        self.assertEqual(str(package), "Basic Package")

class BookingServiceTests(TestCase):
    def setUp(self):
        self.package = PricingPackage.objects.create(
            name="Basic Package",
            price="£125",
            description="Basic mentoring package",
            features="<ul><li>🏃 Feature 1</li></ul>",
            type="single",
            duration_hours=3
        )

    def test_create_booking(self):
        date_time = timezone.now().strftime('%Y-%m-%dT%H:%M')
        booking = BookingService.create_booking(
            package_id=self.package.id,
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            date_time=date_time
        )
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.name, "John Doe")
        self.assertEqual(booking.package, self.package)
        self.assertEqual(booking.status, 'completed')

    def test_cancel_booking(self):
        date_time = (timezone.now() - timezone.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
        booking = BookingService.create_booking(
            package_id=self.package.id,
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            date_time=date_time
        )
        current_time = timezone.now() - timezone.timedelta(hours=2)
        cancelled_booking = BookingService.cancel_booking(booking.reference_id, current_time)
        self.assertEqual(cancelled_booking.status, 'expired')

    def test_update_expired_bookings(self):
        past_date = timezone.now() - timezone.timedelta(days=1)
        booking = BookingService.create_booking(
            package_id=self.package.id,
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            date_time=past_date.strftime('%Y-%m-%dT%H:%M')
        )
        booking.end_date = past_date
        booking.save()
        count = BookingService.update_expired_bookings()
        self.assertEqual(count, 1)
        self.assertEqual(Booking.objects.get(id=booking.id).status, 'expired')

class EmailServiceTests(TestCase):
    def setUp(self):
        self.package = PricingPackage.objects.create(
            name="Basic Package",
            price="£125",
            description="Basic mentoring package",
            features="<ul><li>🏃 Feature 1</li></ul>",
            type="single",
            duration_hours=3
        )
        self.booking = BookingService.create_booking(
            package_id=self.package.id,
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            date_time=timezone.now().strftime('%Y-%m-%dT%H:%M')
        )

    def test_send_booking_confirmation(self):
        EmailService.send_booking_confirmation(self.booking, None)  # Pass None for request in test
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Kidz Runz Booking Confirmation')

    def test_send_admin_notification(self):
        EmailService.send_admin_notification(self.booking, None)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'New Booking Notification - Kidz Runz')

class CoreViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.package = PricingPackage.objects.create(
            name="Basic Package",
            price="£125",
            description="Basic mentoring package",
            features="<ul><li>🏃 Feature 1</li></ul>",
            type="single",
            duration_hours=3
        )
        self.booking = BookingService.create_booking(
            package_id=self.package.id,
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            date_time=timezone.now().strftime('%Y-%m-%dT%H:%M')
        )

    def test_choose_package_view(self):
        response = self.client.get(reverse('core:choose_package', args=[self.package.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/choose_package.html')
        self.assertContains(response, self.package.name)

    def test_bookings_view_post(self):
        date_time = timezone.now().strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(reverse('core:bookings'), {
            'package_id': self.package.id,
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '1234567890',
            'date_time': date_time,
            'description': 'No allergies'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to thank_you
        self.assertTrue(Booking.objects.filter(name='Jane Doe').exists())

    def test_thank_you_view(self):
        response = self.client.get(reverse('core:thank_you', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/thank_you.html')
        self.assertContains(response, self.booking.reference_id)

    def test_cancel_booking_view_get(self):
        response = self.client.get(reverse('core:cancel_booking', args=[self.booking.reference_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/cancel_booking.html')

    def test_cancel_booking_view_post(self):
        # Set start_date in the future to allow cancellation
        self.booking.start_date = timezone.now() + timezone.timedelta(hours=1)
        self.booking.save()
        response = self.client.post(reverse('core:cancel_booking', args=[self.booking.reference_id]))
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'expired')