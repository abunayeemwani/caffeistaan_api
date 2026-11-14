from decimal import Decimal
from django.db import models
from django.core.cache import cache

class TimeStampedModel(models.Model):
    """Abstract base model providing created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CafeConfiguration(TimeStampedModel):
    """
    Singleton model for global café profile, taxes, fees, and operational switches.
    Cached in memory to eliminate redundant DB queries on every price calculation.
    """
    # Branding & Information
    cafe_name = models.CharField(max_length=150, default="Caffeistaan")
    cafe_tagline = models.CharField(max_length=255, default="Artisanal Roastery & Kitchen")
    cafe_description = models.TextField(
        default="Precision single-origin pour-overs, handcrafted pizzas, and artisan kitchen fare."
    )
    cafe_phone = models.CharField(max_length=20, default="6005833574")
    cafe_email = models.EmailField(default="caffeistaan@gmail.com")
    cafe_address = models.TextField(default="Upper Market, Keller, Shopian")
    
    # Financial & Delivery Rules
    currency_symbol = models.CharField(max_length=5, default="₹")
    gst_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("18.00"),
        help_text="Standard restaurant GST rate percentage (e.g., 18.00 for 18%)"
    )
    delivery_fee = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal("20.00"),
        help_text="Fixed delivery charge applied to HOME_DELIVERY orders"
    )
    free_delivery_threshold = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("1000.00"),
        help_text="Subtotal amount above which delivery fee becomes ₹0.00"
    )
    
    # Operational Toggles
    is_ordering_open = models.BooleanField(
        default=True,
        help_text="Emergency kill-switch to pause new orders"
    )
    closure_message = models.CharField(
        max_length=255, 
        default="We are currently closed for kitchen maintenance.",
        blank=True
    )

    class Meta:
        verbose_name = "Café Business Configuration"
        verbose_name_plural = "Café Business Configuration"

    def save(self, *args, **kwargs):
        self.pk = 1  # Enforce singleton
        super().save(*args, **kwargs)
        cache.set("CAFE_CONFIG_CACHE_KEY", self, timeout=86400)

    def delete(self, *args, **kwargs):
        pass  # Prevent accidental deletion

    @classmethod
    def get_solo(cls):
        """Fetches from cache or database, auto-creating default if none exists."""
        config = cache.get("CAFE_CONFIG_CACHE_KEY")
        if not config:
            config, _ = cls.objects.get_or_create(pk=1)
            cache.set("CAFE_CONFIG_CACHE_KEY", config, timeout=86400)
        return config

    def __str__(self):
        return f"{self.cafe_name} Settings (GST: {self.gst_percentage}%, Delivery: {self.currency_symbol}{self.delivery_fee})"
