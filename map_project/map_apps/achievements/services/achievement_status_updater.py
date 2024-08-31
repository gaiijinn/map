from map_apps.users.service.level_calculating_service import \
    UserLevelCalculating

from ..models import AchievementsProgressStatus
from ..services.abc_modules.status_updater_abc import BaseIsAchievedUpdater


class IsAchievedUpdater(BaseIsAchievedUpdater):
    """
    This class is responsible to set the 'is_achieved' flag.
    """

    def __init__(self, achievement_obj):
        self.obj = achievement_obj

    def get_is_achieved(self) -> bool:
        is_achieved = self.obj.progress_rn >= self.obj.achievement.final_value
        return is_achieved


class AchievementStatusUpdater:
    """
    This class is responsible for tracking the new/old model field - 'is_achieved', from AchievementProgressStatus.
    """

    def __init__(self, achievement_obj, is_achieved_updater):
        self.obj = achievement_obj
        self.is_achieved_updater = is_achieved_updater

    def update_achievement_status(self) -> bool:
        """
        Checks if the 'is_achieved' status has changed. If it has, updates the field in the database.
        """
        is_achieved = self.is_achieved_updater.get_is_achieved()

        if is_achieved != self.obj.is_achieved:
            AchievementsProgressStatus.objects.filter(id=self.obj.id).update(
                is_achieved=is_achieved
            )
            return True


class AchievementController:
    """
    This class is responsible for managing the process of updating the flag - 'is_achieved' field in model
    AchievementProgressStatus, and the user level in the system. It takes an achievement object and
    initializes two services: IsAchievedUpdater for updating the achievement status and UserLevelCalculating
    for recalculating the user's level.

    The achievement_status_processing method updates the achievement status, and if the status changes,
    it triggers the user's level recalculation.
    """

    def __init__(
        self,
        achievement_obj,
        is_achieved_updater=IsAchievedUpdater,
        user_level_calculating=UserLevelCalculating,
    ):
        self.obj = achievement_obj
        self.is_achieved_updater = is_achieved_updater(self.obj)
        self.user_level_calculating = user_level_calculating(self.obj.user)

    def achievement_status_processing(self) -> None:
        achievement_status_updater = AchievementStatusUpdater(
            self.obj, self.is_achieved_updater
        )

        if achievement_status_updater.update_achievement_status():
            """
            If achievement field 'is_achieved' was changed we must recalculate the user level, so there we
            start level calculating by using the users.service.level_calculating_service
            """

            user_level_calculating = UserLevelCalculating(self.obj.user)
            user_level_calculating.level_updater()
