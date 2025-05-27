from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('choose-package/<int:package_id>/', views.choose_package, name='choose_package'),
    path('bookings/', views.bookings, name='bookings'),
    path('thank-you/<str:reference_id>/', views.thank_you, name='thank_you'),
    path('cancel/<str:reference_id>/', views.cancel_booking, name='cancel_booking'),
]