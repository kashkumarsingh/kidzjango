"""
URL configuration for the frontend app.
"""
from django.urls import path
from . import views

app_name = 'frontend'  # Namespace for URL reversing

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('welcome/', views.welcome, name='welcome'),
    path('mission/', views.mission, name='mission'),
    path('story/', views.story, name='story'),
    path('communication/', views.communication, name='communication'),
    path('parent-tips/', views.parent_tips, name='parent_tips'),
    path('safeguarding/', views.safeguarding, name='safeguarding'),
    path('gallery/', views.gallery, name='gallery'),
    path('cams/', views.cams, name='cams'),
    path('activities/', views.activities, name='activities'),
    path('benefits/', views.benefits, name='benefits'),
    path('explore/', views.explore, name='explore'),
    path('contact/', views.contact, name='contact'),
    path('bookings/', views.bookings, name='bookings'),
    path('services/', views.services, name='services'),
    path('faqs/', views.faqs, name='faqs'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('pricing_packages/', views.pricing_packages, name='pricing_packages'),
    path('terms/', views.terms, name='terms'), 
]