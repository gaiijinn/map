from typing import Type

from django.db.models import Sum
from map_apps.achievements.models import AchievementsProgressStatus

from ..models import UserLevel, UserProfile
from .level_abc import BaseExperienceCalculator, BaseLevelFinder


class UserLevelFinder(BaseLevelFinder):
    """
    This class is responsible for finding the level depending on sum of total achieved achievements (total_exp)
    """
    def get_last_level(self) -> object:
        last_lvl = UserLevel.objects.last()
        return last_lvl

    def get_level(self, total_exp: int) -> object:
        user_level = UserLevel.objects.filter(
            low_range__lte=total_exp, top_range__gte=total_exp
        ).first()

        return user_level


class ExperienceCalculator(BaseExperienceCalculator):
    """
    This class is just a calculater, to get the (total_exp), depends on achieved user's achievements.
    """
    def get_total_exp(self, user: object) -> int:
        total_exp = (
                AchievementsProgressStatus.objects.select_related("achievement")
                .filter(user=user, is_achieved=True)
                .aggregate(total_exp=Sum("achievement__given_exp"))["total_exp"]
                or 0
        )
        return total_exp


class UserLevelCalculating:
    """
    This class is responsible for calculating and updating a user's level based on their total experience points.
    """
    def __init__(self,
                 user: object,
                 level_finder: Type[BaseLevelFinder] = UserLevelFinder,
                 experience_calculator: Type[BaseExperienceCalculator] = ExperienceCalculator):

        self.user = user
        self.level_finder = level_finder()
        self.experience_calculator = experience_calculator()

    def level_updater(self):
        last_level = self.level_finder.get_last_level()
        total_exp = self.experience_calculator.get_total_exp(self.user)
        user_level = self.level_finder.get_level(total_exp)

        if user_level and self.user.user_profile.user_level != last_level:
            """
            Updates the user's level only if a level is found and the user is not already at the last level.
            """
            UserProfile.objects.filter(user=self.user).update(user_level=user_level)
