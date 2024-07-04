from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..achievements.models import Achievements, AchievementsProgressStatus
from .models import User, UserProfile, UserVerification
from .tasks import level_calculating


@receiver(post_save, sender=UserVerification)
def set_expired_time(sender, instance, created, **kwargs):
    if created:
        instance.expired_at = instance.created_at + timedelta(days=2)
        instance.verif_to = instance.created_at + timedelta(days=365)
        instance.save()


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

        AchievementsProgressStatus.objects.bulk_create(achievement_progress_list)


# @receiver(post_save, sender=UserProfile)
# def set_user_level(sender, instance, created, **kwargs):
#     level_calculating(instance.user.id)
