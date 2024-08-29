from typing import Type

from django.contrib.auth import get_user_model

from ..models import Achievements, AchievementsProgressStatus
from .abc_modules.progress_updater_abc import (BaseAchievementGetter,
                                               BaseUserGetter)
from .decorators.decorators import handle_object_not_found


class AchievementGetter(BaseAchievementGetter):
    @handle_object_not_found(warning_message="Achievement object not found")
    def get_achievement(self, achievement_id) -> object:
        return Achievements.objects.get(id=achievement_id)


class UserGetter(BaseUserGetter):
    @handle_object_not_found(warning_message="User object not found")
    def get_user(self, users_id) -> object:
        return get_user_model().objects.get(id=users_id)


class AchievementProgressController:
    """
    Service for updating the progress of achievements for users.
    This class is responsible for updating the progress of a specific achievement for a user.
    It retrieves the achievement and user objects using the provided IDs, and then increments
    the progress of the achievement for the user.

    This class is intended to be used within controllers to handle the update logic for achievement progress. After
    successful updating, a post-save signal will be triggered on AchievementProgressStatus model, which then invoke a
    task for changing the boolean model field and level calculating.
    """

    def __init__(
        self,
        achievement_id,
        user_id,
        achievement_getter: Type[AchievementGetter] = AchievementGetter,
        user_getter: Type[UserGetter] = UserGetter,
    ):
        self.achievement_id = achievement_id
        self.user_id = user_id

        self.achievement_getter = achievement_getter()
        self.user_getter = user_getter()

        self.achievement_object = self.achievement_getter.get_achievement(
            self.achievement_id
        )
        self.user_object = self.user_getter.get_user(self.user_id)

    def progress_updater(self) -> None:
        if self.achievement_object and self.user_object:
            obj = AchievementsProgressStatus.objects.get(
                user=self.user_object, achievement=self.achievement_object
            )

            if not obj.is_achieved:
                obj.progress_rn += 1
                obj.save()

                # post_save signal is triggered (in achievements signals)
