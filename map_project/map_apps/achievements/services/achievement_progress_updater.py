from django.db.models import F
from django.contrib.auth import get_user_model
from ..models import Achievements, AchievementsProgressStatus


class AchievementGetter:
    def get_achievement(self, achievements_id):
        return Achievements.objects.get(id=achievements_id)


class UserGetter:
    def get_user(self, users_id):
        return get_user_model().objects.get(id=users_id)


class AchievementProgressController:
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

            obj.progress_rn += 1
            obj.save()
