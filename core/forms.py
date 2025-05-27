from django import forms
from django.core.exceptions import ValidationError
import re
from .models import PricingPackage

class BookingForm(forms.Form):
    package_id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=20, required=True, label="Phone Number")
    date_time = forms.DateTimeField(required=True, label="Preferred Date and Time")
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Additional Information",
        help_text="Allergies, special needs, or other notes"
    )

    def clean_package_id(self):
        package_id = self.cleaned_data['package_id']
        try:
            PricingPackage.objects.get(id=package_id)
        except PricingPackage.DoesNotExist:
            raise ValidationError("Selected package does not exist.")
        return package_id

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\+?1?\d{9,15}$', phone.replace(" ", "").replace("-", "")):
            raise ValidationError("Please enter a valid phone number.")
        return phone

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[A-Za-z\s-]+$', name):
            raise ValidationError("Name should only contain letters, spaces, or hyphens.")
        return name