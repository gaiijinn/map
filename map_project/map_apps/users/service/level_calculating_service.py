from django.db.models import Sum
from ..models import User, UserLevel, UserProfile
from map_project.map_apps.achievements.models import AchievementsProgressStatus


class UserLevelCalculating:
    def __init__(self, user: User):
        self.user = user

    def get_total_exp(self):
        total_exp = (
            AchievementsProgressStatus.objects.select_related("achievement")
            .filter(user=self.user, is_achieved=True)
            .aggregate(total_exp=Sum("achievement__given_exp"))["total_exp"]
            or 0
        )
        return total_exp

    def get_level(self, total_exp):
        user_level = UserLevel.objects.filter(low_range__lte=total_exp, top_range__gte=total_exp).first()

        return user_level

    def level_updater(self):
        total_exp = self.get_total_exp()
        user_level = self.get_level(total_exp)

        if user_level:
            UserProfile.objects.filter(user=self.user).update(user_level=user_level)
