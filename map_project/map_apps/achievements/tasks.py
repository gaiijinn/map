from celery import shared_task
from django.db import transaction

from ..users.models import UserLevel
from ..users.tasks import level_calculating


@shared_task
def check_achievements_status(obj_id):
    """Tracking progress to set current is_achieved value"""
    from .models import AchievementsProgressStatus

    obj = (
        AchievementsProgressStatus.objects.select_related("user")
        .filter(id=obj_id)
        .first()
    )

    last_lvl = UserLevel.objects.last()

    if obj:
        with transaction.atomic():
            is_achieved = obj.progress_rn >= obj.achievement.final_value
            new_progress = min(obj.progress_rn, obj.achievement.final_value)

            AchievementsProgressStatus.objects.filter(id=obj_id).update(
                progress_rn=new_progress
            )

            # we are changing boolean field only when it has changed
            if obj.is_achieved != is_achieved:
                AchievementsProgressStatus.objects.filter(id=obj_id).update(
                    is_achieved=is_achieved
                )

                if obj.user.user_profile.user_level != last_lvl:
                    level_calculating.delay(obj.user.id)
