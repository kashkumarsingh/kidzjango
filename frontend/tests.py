from django.test import TestCase
from django.urls import reverse
# Create your tests here.

class FrontendViewsTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('frontend:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/home.html')

    def test_about_view(self):
        response = self.client.get(reverse('frontend:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'frontend/about.html')
