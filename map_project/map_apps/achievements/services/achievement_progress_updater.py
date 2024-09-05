import logging

from ..models import AchievementsProgressStatus

logger_warning = logging.getLogger('achievement_warning')


def progress_updater(achievement_keyword, user_id):
    try:
        achiev_obj = AchievementsProgressStatus.objects.get(user__id=user_id, achievement__keyword=achievement_keyword)
        if not achiev_obj.is_achieved:
            achiev_obj.progress_rn += 1
            achiev_obj.save()
    except AchievementsProgressStatus.DoesNotExist:
        logger_warning.warning(
            f"Achievement progress status not found for user {user_id} and keyword {achievement_keyword}")


def progress_updater_v2(achievement_obj):
    if not achievement_obj.is_achieved:
        achievement_obj.progress_rn += 1
        achievement_obj.save()
