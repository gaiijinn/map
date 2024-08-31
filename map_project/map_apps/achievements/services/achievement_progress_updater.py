from django.shortcuts import get_object_or_404

from ..models import AchievementsProgressStatus
from .decorators.decorators import handle_msg_log_404


@handle_msg_log_404()
def progress_updater(achievement_id, user_id):
    achiev_obj = get_object_or_404(AchievementsProgressStatus, user__id=user_id,
                                   achievement__id=achievement_id)
    if not achiev_obj.is_achieved:
        achiev_obj.progress_rn += 1
        achiev_obj.save()
