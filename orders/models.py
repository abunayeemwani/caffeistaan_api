from decimal import Decimal
from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from menu.models import Dish


class Order(TimeStampedModel):
    class OrderType(models.TextChoices):
        DELIVERY = 'DELIVERY', 'Home Delivery'
        TAKEAWAY = 'TAKEAWAY', 'Takeaway / Pickup'
        DINE_IN = 'DINE_IN', 'Dine-In'

    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Confirmation'
        ACCEPTED = 'ACCEPTED', 'Accepted by Kitchen'
        PREPARING = 'PREPARING', 'Preparing in Kitchen'
        READY = 'READY', 'Ready for Dispatch / Pickup'
        DISPATCHED = 'DISPATCHED', 'Out for Delivery'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        REJECTED = 'REJECTED', 'Rejected'

    order_number = models.CharField(max_length=32, unique=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    order_type = models.CharField(max_length=20, choices=OrderType.choices, default=OrderType.DELIVERY)
    order_status = models.CharField(max_length=25, choices=OrderStatus.choices, default=OrderStatus.PENDING, db_index=True)

    # Customer Contact Info
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=17, db_index=True)
    customer_email = models.EmailField(blank=True, null=True)

    # Contextual Delivery / Dine-in specifics
    delivery_street_address = models.TextField(blank=True, null=True)
    delivery_locality = models.CharField(max_length=100, blank=True, null=True)
    delivery_instructions = models.CharField(max_length=255, blank=True, null=True)
    dine_in_table_number = models.CharField(max_length=20, blank=True, null=True)
    pickup_time = models.DateTimeField(blank=True, null=True)

    # Financial breakdown
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, default="Cash on Delivery (COD)")

    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} ({self.customer_name}) - ₹{self.total_amount}"


class OrderItem(models.Model):
    """Snapshot of purchased line items."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    dish_name = models.CharField(max_length=200)
    variant_name = models.CharField(max_length=100, blank=True)
    addons_summary = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.dish_name} (₹{self.line_total})"


class OrderStatusHistory(TimeStampedModel):
    """Tracks every lifecycle status change with timestamps."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=25)
    comments = models.CharField(max_length=255, blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.order.order_number} -> {self.status}"