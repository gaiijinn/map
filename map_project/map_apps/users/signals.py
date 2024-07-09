from datetime import timedelta

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..achievements.models import Achievements, AchievementsProgressStatus
from .models import User, UserProfile, UserVerification, UserLevel
from .tasks import level_calculating


@receiver(post_save, sender=UserVerification)
def set_expired_time(sender, instance, created, **kwargs):
    if created:
        instance.expired_at = instance.created_at + timedelta(days=2)


@receiver(post_save, sender=User)
def set_achievement_user(sender, instance, created, **kwargs):
    """Set achievements for User after success reg or level calculating"""
    if created:
        if instance.is_org:
            achievements = Achievements.objects.filter(for_organization=True)
        else:
            achievements = Achievements.objects.filter(for_def_user=True)

        achievement_progress_list = [
            AchievementsProgressStatus(user=instance, achievement=achievement)
            for achievement in achievements
        ]

        with transaction.atomic():
            AchievementsProgressStatus.objects.bulk_create(achievement_progress_list)
            UserProfile.objects.create(user=instance, user_level=UserLevel.objects.first())
