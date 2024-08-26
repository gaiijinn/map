from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from ..models import Achievements, AchievementsProgressStatus


class NoneReturner:
    def get_object_or_none(self, model_class, **kwargs):
        try:
            return model_class.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class AchievementGetter(NoneReturner):
    def get_achievement(self, achievement_id):
        return super().get_object_or_none(Achievements, id=achievement_id)


class UserGetter(NoneReturner):
    def get_user(self, users_id):
        return super().get_object_or_none(get_user_model(), id=users_id)


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

    def __init__(self, achievements_id, users_id):
        self.achievements_id = achievements_id
        self.users_id = users_id

    def achievement_obj_builder(self):
        return AchievementGetter().get_achievement(self.achievements_id)

    def user_obj_builder(self):
        return UserGetter().get_user(self.users_id)

    def progress_updater(self):
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
