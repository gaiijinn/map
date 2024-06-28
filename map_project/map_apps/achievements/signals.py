from django.db.models.signals import post_save
from django.dispatch import receiver

from ..users.models import User
from .models import Achievements, AchievementsProgressStatus


@receiver(post_save, sender=Achievements)
def set_new_achievement(sender, instance, created, **kwargs):
    if created:
        if instance.for_def_user:
            users = User.objects.filter(is_org=False)
        else:
            users = User.objects.filter(is_org=True)

        achievement_progress_list = [
            AchievementsProgressStatus(user=user, achievement=instance)
            for user in users
        ]

        AchievementsProgressStatus.objects.bulk_create(achievement_progress_list)
