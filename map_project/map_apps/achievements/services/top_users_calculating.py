from django.db.models import Sum
from map_apps.users.models import User, UserLevel


class LastLevelGetter:
    def get_last_level(self):
        return UserLevel.objects.last()


class TopUsersGetter:
    def get_top_users(self, last_level):
        return (User.objects.filter(user_profile__user_level=last_level).
                filter(achievementsprogressstatus__is_achieved=True))


class TopUsersCalculator:
    def __init__(self, last_level=LastLevelGetter, users=TopUsersGetter, amount_of_users=100):
        self.last_level = last_level()
        self.users = users()
        self.amount_of_users = amount_of_users

    def top_user_calculator(self):
        last_level = self.last_level.get_last_level()
        users = self.users.get_top_users(last_level)

        top_users = users.annotate(
            total_exp=Sum("achievementsprogressstatus__achievement__given_exp")).order_by('-total_exp')

        return top_users
