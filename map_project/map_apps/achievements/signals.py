from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..users.models import User
from .models import Achievements, AchievementsProgressStatus
from .tasks import check_achievements_status


@receiver(post_save, sender=Achievements)
def set_new_achievement(sender, instance, created, **kwargs):
    """Just add new achievement for created users"""
    if created:
        with transaction.atomic():
            if instance.for_def_user:
                users = User.objects.filter(is_org=False)
            else:
                users = User.objects.filter(is_org=True)

            achievement_progress_list = [
                AchievementsProgressStatus(user=user, achievement=instance)
                for user in users
            ]

            AchievementsProgressStatus.objects.bulk_create(achievement_progress_list)


@receiver(post_save, sender=AchievementsProgressStatus)
def check_status(sender, instance, created, **kwargs):
    """From here we check the achievement status and set the actual user level"""
    if not created:
        check_achievements_status.delay(instance.id)
