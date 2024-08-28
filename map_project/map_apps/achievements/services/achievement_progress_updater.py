from django.contrib.auth import get_user_model

from ..models import Achievements, AchievementsProgressStatus
from .abc_modules.progress_updater_abc import (BaseAchievementGetter,
                                               BaseUserGetter)
from .decorators.decorators import handle_no_object


class AchievementGetter(BaseAchievementGetter):
    @handle_no_object
    def get_achievement(self, achievement_id, model_class=Achievements) -> object:
        return model_class.objects.get(id=achievement_id)


class UserGetter(BaseUserGetter):
    @handle_no_object
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

    def __init__(self, achievements_id, users_id, achievement_getter=AchievementGetter, user_getter=UserGetter):
        self.achievements_id = achievements_id
        self.users_id = users_id

        self.achievement_getter = achievement_getter()
        self.user_getter = user_getter()

    def achievement_obj_builder(self) -> object:
        return self.achievement_getter.get_achievement(self.achievements_id)

    def user_obj_builder(self) -> object:
        return self.user_getter.get_user(self.users_id)

    def progress_updater(self) -> None:
        achievement = self.achievement_obj_builder()
        user = self.user_obj_builder()

        if user and achievement:
            obj = AchievementsProgressStatus.objects.get(
                user=user,
                achievement=achievement
            )

            if not obj.is_achieved:
                obj.progress_rn += 1
                obj.save()

                # post_save signal is triggered (in achievements signals)
