from .achievement_abc import BaseIsAchievedUpdater, BaseProgressUpdater

from map_apps.users.service.level_calculating_service import \
    UserLevelCalculating

from ..models import AchievementsProgressStatus


class ProgressUpdater(BaseProgressUpdater):
    def __init__(self, achievement_obj):
        self.obj = achievement_obj

    def get_new_progress(self):
        new_progress = min(self.obj.progress_rn, self.obj.achievement.final_value)
        return new_progress


class IsAchievedUpdater(BaseIsAchievedUpdater):
    def __init__(self, achievement_obj):
        self.obj = achievement_obj

    def get_is_achieved(self) -> bool:
        is_achieved = self.obj.progress_rn >= self.obj.achievement.final_value
        return is_achieved


class AchievementStatusUpdater:
    def __init__(self, achievement_obj, progress_updater, is_achieved_updater):
        self.obj = achievement_obj
        self.progress_updater = progress_updater
        self.is_achieved_updater = is_achieved_updater

    def update_achievement_status(self):
        new_progress = self.progress_updater.get_new_progress()
        is_achieved = self.is_achieved_updater.get_is_achieved()

        if is_achieved != self.obj.is_achieved:
            AchievementsProgressStatus.objects.filter(id=self.obj.id).update(
                is_achieved=is_achieved, progress_rn=new_progress
            )
            return True

        else:
            AchievementsProgressStatus.objects.filter(id=self.obj.id).update(
                progress_rn=new_progress
            )
            return False


class AchievementController:
    def __init__(self, achievement_obj, progress_updater=ProgressUpdater, is_achieved_updater=IsAchievedUpdater,
                 user_level_calculating=UserLevelCalculating):
        self.obj = achievement_obj
        self.progress_updater = progress_updater(self.obj)
        self.is_achieved_updater = is_achieved_updater(self.obj)
        self.user_level_calculating = user_level_calculating(self.obj.user)

    def achievement_status_processing(self):
        achievement_status_updater = AchievementStatusUpdater(
            self.obj, self.progress_updater, self.is_achieved_updater
        )

        if achievement_status_updater.update_achievement_status():
            user_level_calculating = UserLevelCalculating(self.obj.user)
            user_level_calculating.level_updater()
