from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from core.models import TimeStampedModel


class MenuCategory(TimeStampedModel):
    """Product categories (e.g., Artisanal Coffee, Sourdough Pizzas, Desserts)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Menu Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dish(TimeStampedModel):
    """Individual food or beverage menu items."""
    class DietaryType(models.TextChoices):
        VEG = 'VEG', 'Vegetarian'
        NON_VEG = 'NON_VEG', 'Non-Vegetarian'
        VEGAN = 'VEGAN', 'Vegan'

    category = models.ForeignKey(
        MenuCategory, 
        on_delete=models.PROTECT, 
        related_name='dishes'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    detailed_description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preparation_time = models.PositiveIntegerField(default=15, help_text="Prep time in minutes")
    dietary_type = models.CharField(
        max_length=10, 
        choices=DietaryType.choices, 
        default=DietaryType.VEG
    )
    is_available = models.BooleanField(default=True, db_index=True, help_text="1-tap toggle for sold-out items")
    is_featured = models.BooleanField(default=False, db_index=True)
    display_priority = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_priority', '-created_at']
        verbose_name_plural = "Dishes"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def current_price(self) -> Decimal:
        """Returns discounted price if set, otherwise base price."""
        if self.discounted_price is not None and self.discounted_price > 0:
            return self.discounted_price
        return self.base_price

    def __str__(self):
        return f"{self.name} (₹{self.current_price})"


class DishImage(TimeStampedModel):
    """Supports multiple gallery images per dish."""
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='dishes/%Y/%m/')
    alt_text = models.CharField(max_length=150, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"Image for {self.dish.name}"


class DishVariant(models.Model):
    """Size options or brew styles (e.g., Regular, Large 12", Chemex)."""
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    price_adjustment = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Amount added to base dish price (e.g. +150.00)"
    )
    is_default = models.BooleanField(default=False)

    def __str__(self):
        sign = '+' if self.price_adjustment >= 0 else ''
        return f"{self.dish.name} - {self.name} ({sign}₹{self.price_adjustment})"


class AddOn(models.Model):
    """Optional modifiers (e.g., Extra Cheese, Oat Milk, Shot of Hazelnut)."""
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='addons')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (+₹{self.price})"
