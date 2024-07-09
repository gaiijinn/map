from celery import shared_task
from django.db import transaction

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

    if obj:
        with transaction.atomic():
            is_achieved = obj.progress_rn >= obj.achievement.final_value
            new_progress = min(obj.progress_rn, obj.achievement.final_value)

            AchievementsProgressStatus.objects.filter(id=obj_id).update(
                is_achieved=is_achieved, progress_rn=new_progress
            )

            # set user level
            # в будущем надо оставить условие потому что достижения нету смысла скидывать назад постоянно
            # if is_achieved:
            #     level_calculating.delay(obj.user.id)

            level_calculating.delay(obj.user.id)
