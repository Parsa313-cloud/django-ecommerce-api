# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from cart.models import ShoppingCart

@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        ShoppingCart.objects.create(user=instance)
