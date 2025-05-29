from .models import FAQ, PricingPackage
from django.conf import settings

def stripe_keys(request):
    return {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }

def faq_pricing_context(request):
    from .models import FAQ, PricingPackage
    return {
        'faqs': FAQ.objects.all()[:5],
        'pricing_packages': PricingPackage.objects.all(),
    }

def faq_pricing_context(request):
    return {
        'faqs': FAQ.objects.all()[:5],
        'pricing_packages': PricingPackage.objects.all(),
    }