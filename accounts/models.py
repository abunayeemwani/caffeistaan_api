from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

from core.models import TimeStampedModel


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with phone number as the unique identifier."""
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be provided.')
        phone = phone.strip()
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    """Custom User model for Caffiestaan supporting Customers and Staff."""
    username = None  # Remove username field
    phone = models.CharField(max_length=17, unique=True, db_index=True)
    full_name = models.CharField(max_length=150, blank=True)
    is_cafe_staff = models.BooleanField(
        default=False, 
        help_text="Designates whether this user has access to the Live Kitchen Desk."
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name or 'Customer'} ({self.phone})"


class FCMDevice(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fcm_devices',
        null=True,
        blank=True
    )
    registration_id = models.TextField(unique=True)
    device_type = models.CharField(max_length=10, choices=[('ANDROID', 'Android'), ('IOS', 'iOS'), ('WEB', 'Web')], default='ANDROID')
    is_staff_device = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} ({self.device_type}) - Staff: {self.is_staff_device}"


class CustomerProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=17, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} ({self.phone or 'No phone'})"


class Address(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_addresses'
    )
    address_label = models.CharField(
        max_length=50,
        default='Home',
        help_text="e.g. Home, Office, Work"
    )
    recipient_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=17)
    street_address = models.TextField(help_text="House/Flat No., Building, Street")
    locality = models.CharField(max_length=100, help_text="Area, Sector, Colony")
    postal_code = models.CharField(max_length=10, blank=True, default='')
    landmark = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-created_at']

    def save(self, *args, **kwargs):
        # If this address is set as default, unset existing defaults for this user
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.address_label}: {self.recipient_name}, {self.locality}"
