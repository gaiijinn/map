from ..models import AchievementsProgressStatus


class AchievementStatusUpdater:
    def __init__(self, obj):
        self.obj = obj

    def update_status(self):
        is_achieved = self.obj.progress_rn >= self.obj.achievement.final_value
        new_progress = min(self.obj.progress_rn, self.obj.achievement.final_value)

        if is_achieved != self.obj.is_achieved:
            AchievementsProgressStatus.objects.filter(id=self.obj.id).update(
                is_achieved=is_achieved, progress_rn=new_progress)
            return True

        else:
            AchievementsProgressStatus.objects.filter(id=self.obj.id).update(
                progress_rn=new_progress
            )
            return False
