from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from ..achievements.models import Achievements, AchievementsProgressStatus
from ..achievements.tasks import check_achievements_status
from .models import User, UserLevel, UserProfile


@receiver(post_save, sender=User)
def set_achievement_user(sender, instance, created, **kwargs):
    """Set achievements for User after success registration and create the profile instance"""
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


# @receiver(post_save, sender=UserProfile)
# def update_achievement_progress(sender, instance, created, **kwargs):
#     if not created:
#         with transaction.atomic():
#             achievement_status_object = get_object_or_404(AchievementsProgressStatus, user__id=instance.user.id,
#                                                           achievement__keyword='UP')
#
#             if not achievement_status_object.is_achieved:
#                 achievement_status_object.is_achieved += 1
#                 achievement_status_object.save()
#
#                 check_achievements_status.delay(achievement_status_object.id)
