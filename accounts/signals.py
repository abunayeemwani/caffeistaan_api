from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomerProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        phone_val = getattr(instance, 'phone', None)
        CustomerProfile.objects.create(user=instance, phone=phone_val)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()