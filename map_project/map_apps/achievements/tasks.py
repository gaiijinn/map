from celery import shared_task
from django.db import transaction


@shared_task
def check_achievements_status(obj_id):
    from .models import AchievementsProgressStatus

    obj = AchievementsProgressStatus.objects.filter(id=obj_id).first()
    if obj:
        with transaction.atomic():
            is_achieved = obj.progress_rn >= obj.achievement.final_value
            new_progress = min(obj.progress_rn, obj.achievement.final_value)

            AchievementsProgressStatus.objects.filter(id=obj_id).update(
                is_achieved=is_achieved,
                progress_rn=new_progress
            )
