from django.contrib import admin
from .models import FAQ, PricingPackage, Booking, EmailConfiguration

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['question', 'answer']

@admin.register(PricingPackage)
class PricingPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['reference_id', 'name', 'email', 'package', 'start_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'package__name', 'reference_id']

@admin.register(EmailConfiguration)
class EmailConfigurationAdmin(admin.ModelAdmin):
    list_display = ['host', 'port', 'use_tls', 'username', 'is_active']
    list_filter = ['is_active']
    search_fields = ['host', 'username']