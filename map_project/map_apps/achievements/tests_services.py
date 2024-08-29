from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..achievements.models import Achievements, AchievementsProgressStatus
from ..achievements.services.achievement_progress_updater import \
    AchievementProgressController
from ..achievements.services.achievement_status_updater import \
    AchievementController
from ..users.models import UserLevel

# Create your tests here.

PATCH_USER_PROFILE = reverse("users:user-profile-update-v1")


def creating_level(**params):
    defaults = {"level_name": "Новачок", "low_range": 0, "top_range": 10}

    defaults.update(params)

    return UserLevel.objects.create(**defaults)


def create_user(**params):
    defaults = {
        "email": "test@example.com",
        "password": "test1233",
        "first_name": "Vlad",
        "last_name": "Achievement",
    }

    defaults.update(**params)

    return get_user_model().objects.create_user(**defaults)


def creating_base_achievement(**params):
    defaults = {
        "achievement_name": "Перше досягнення",
        "descr_achievement": "йоу",
        "given_exp": 11,
        "final_value": 1,
        "for_organization": False,
        "for_def_user": True,
    }

    defaults.update(params)

    return Achievements.objects.create(**defaults)


class AchievementServiceTest(TestCase):
    def setUp(self) -> None:
        self.first_lvl = creating_level()

        payload = {"level_name": "Продвинутий", "low_range": 11, "top_range": 20}
        self.second_lvl = creating_level(**payload)

        self.first_achievement = creating_base_achievement()
        self.user = create_user()

    def test_services_to_update_userlevel_and_achievement_status(self):
        achievement_status = AchievementsProgressStatus.objects.get(
            achievement=self.first_achievement, user=self.user
        )
        self.assertFalse(achievement_status.is_achieved)

        progress_controller = AchievementProgressController(
            achievement_id=self.first_achievement.id, user_id=self.user.id
        )
        progress_controller.progress_updater()
        achievement_status.refresh_from_db()

        self.assertTrue(achievement_status.is_achieved)

        # now we're starting the another service to recalculate user level
        status_controller = AchievementController(achievement_status)
        status_controller.achievement_status_processing()

        self.user.refresh_from_db()
        self.user.user_profile.refresh_from_db()

        # checking if user is on second level after achieved achievement
        self.assertEqual(self.user.user_profile.user_level, self.second_lvl)
