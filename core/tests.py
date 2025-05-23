from django.test import TestCase
from .models import FAQ, PricingPackage

# Create your tests here.


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
