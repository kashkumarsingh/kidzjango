from django.shortcuts import render
from core.models import FAQ, PricingPackage
import logging

# Create your views here.
logger = logging.getLogger('frontend')

def home(request):
    logger.info("Rendering home page")
    faqs = FAQ.objects.all()[:3]  # Show top 3 FAQs
    pricing_packages = PricingPackage.objects.all()
    return render(request, 'frontend/home.html', {'faqs': faqs, 'pricing_packages': pricing_packages})

def about(request):
    logger.info("Rendering about page")
    return render(request, 'frontend/about.html')

def welcome(request):
    logger.info("Rendering welcome page")
    return render(request, 'frontend/welcome.html')

def mission(request):
    logger.info("Rendering mission page")
    return render(request, 'frontend/mission.html')

def story(request):
    logger.info("Rendering story page")
    return render(request, 'frontend/story.html')

def communication(request):
    logger.info("Rendering communication page")
    return render(request, 'frontend/communication.html')

def parent_tips(request):
    logger.info("Rendering parent tips page")
    return render(request, 'frontend/parent_tips.html')

def safeguarding(request):
    logger.info("Rendering safeguarding page")
    return render(request, 'frontend/safeguarding.html')

def cams(request):
    logger.info("Rendering cams page")
    return render(request, 'frontend/cams.html')

def activities(request):
    logger.info("Rendering activities page")
    return render(request, 'frontend/activities.html')

def benefits(request):
    logger.info("Rendering benefits page")
    return render(request, 'frontend/benefits.html')

def explore(request):
    logger.info("Rendering explore page")
    return render(request, 'frontend/explore.html')

def contact(request):
    logger.info("Rendering contact page")
    return render(request, 'frontend/contact.html')

def bookings(request):
    logger.info("Rendering bookings page")
    pricing_packages = PricingPackage.objects.all()
    return render(request, 'frontend/bookings.html', {'pricing_packages': pricing_packages})

def services(request):
    logger.info("Rendering services page")
    return render(request, 'frontend/services.html')

def testimonials(request):
    logger.info("Rendering testimonials page")
    return render(request, 'frontend/testimonials.html')

def faqs(request):
    logger.info("Rendering faqs page")
    faqs = FAQ.objects.all()
    return render(request, 'frontend/faqs.html', {'faqs': faqs})

def gallery(request):
    logger.info("Rendering gallery page")
    return render(request, 'frontend/gallery.html')

def pricing_packages(request):
    pricing_packages = PricingPackage.objects.all()
    return render(request, 'frontend/pricing_packages.html', {'pricing_packages': pricing_packages})

def terms(request):
    logger.info("Rendering terms page")
    return render(request, 'frontend/terms.html')