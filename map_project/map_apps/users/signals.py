from datetime import timedelta

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..achievements.models import Achievements, AchievementsProgressStatus
from .models import User, UserLevel, UserProfile


@receiver(post_save, sender=User)
def set_achievement_user(sender, instance, created, **kwargs):
    """Set achievements for User after success reg or level calculating"""
    if created:
        with transaction.atomic():
            if instance.is_org:
                achievements = Achievements.objects.filter(for_organization=True)
            else:
                achievements = Achievements.objects.filter(for_def_user=True)

            achievement_progress_list = [
                AchievementsProgressStatus(user=instance, achievement=achievement)
                for achievement in achievements
            ]

            AchievementsProgressStatus.objects.bulk_create(achievement_progress_list)
            UserProfile.objects.create(
                user=instance, user_level=UserLevel.objects.first()
            )
