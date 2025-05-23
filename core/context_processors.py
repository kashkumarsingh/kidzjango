from .models import FAQ, PricingPackage

def faq_pricing_context(request):
    return {
        'faqs': FAQ.objects.all()[:5],
        'pricing_packages': PricingPackage.objects.all(),
    }