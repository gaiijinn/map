from django.shortcuts import get_object_or_404

from ..models import AchievementsProgressStatus
from .decorators.decorators import handle_msg_log_404


@handle_msg_log_404()
def progress_updater(achievement_keyword, user_id):
    achiev_obj = get_object_or_404(AchievementsProgressStatus, user__id=user_id,
                                   achievement__keyword=achievement_keyword)
    if not achiev_obj.is_achieved:
        achiev_obj.progress_rn += 1
        achiev_obj.save()


def progress_updater_v2(achievement_obj):
    if not achievement_obj.is_achieved:
        achievement_obj.progress_rn += 1
        achievement_obj.save()
