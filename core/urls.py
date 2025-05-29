from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('choose-package/<int:package_id>/', views.choose_package, name='choose_package'),
    path('bookings/', views.bookings, name='bookings'),
    path('process-payment/<uuid:reference_id>/', views.process_payment, name='process_payment'),
    path('thank-you/<uuid:reference_id>/', views.thank_you, name='thank_you'),
    path('cancel-booking/<uuid:reference_id>/', views.cancel_booking, name='cancel_booking'),
    path('clear-session/', views.clear_session, name='clear_session'),
]