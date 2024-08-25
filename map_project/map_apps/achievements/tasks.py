from celery import shared_task
from .models import AchievementsProgressStatus
from .services.achievement_service import AchievementController


@shared_task
def check_achievements_status(obj_id):
    """Task to update achievement status and level calculating"""

    obj = (
        AchievementsProgressStatus.objects.select_related("user")
        .filter(id=obj_id)
        .first()
    )

    if obj:
        controller = AchievementController(obj)
        controller.achievement_status_processing()
