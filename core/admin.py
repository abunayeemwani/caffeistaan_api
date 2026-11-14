from django.contrib import admin
from .models import CafeConfiguration

@admin.register(CafeConfiguration)
class CafeConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Café Profile & Branding", {
            "fields": ("cafe_name", "cafe_tagline", "cafe_description", "cafe_phone", "cafe_email", "cafe_address")
        }),
        ("Taxation & Logistics", {
            "fields": ("currency_symbol", "gst_percentage", "delivery_fee", "free_delivery_threshold")
        }),
        ("Store Availability", {
            "fields": ("is_ordering_open", "closure_message")
        }),
    )

    def has_add_permission(self, request):
        # Prevent creating multiple config rows
        return not CafeConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False