from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserVerification


@receiver(post_save, sender=UserVerification)
def set_expired_time(sender, instance, created, **kwargs):
    if created:
        instance.expired_at = instance.created_at + timedelta(days=2)
        instance.verif_to = instance.created_at + timedelta(days=730)
        instance.save()
