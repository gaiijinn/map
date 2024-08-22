from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..achievements.models import Achievements, AchievementsProgressStatus
from ..achievements.tasks import check_achievements_status
from ..users.models import UserLevel


# Create your tests here.

def creating_level(**params):
    defaults = {
        'level_name': 'Новачок',
        'low_range': 0,
        'top_range': 10
    }

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
        'achievement_name': 'Перше досягнення',
        'descr_achievement': 'йоу',
        'given_exp': 11,
        'final_value': 1,
        'for_organization': False,
        'for_def_user': True,
    }

    defaults.update(params)

    return Achievements.objects.create(**defaults)


class ModelAchievementsStatusTest(TestCase):
    def setUp(self) -> None:
        self.first_lvl = creating_level()

        payload = {
            'level_name': 'Продвинутий',
            'low_range': 11,
            'top_range': 20
        }
        self.second_lvl = creating_level(**payload)

        self.user = create_user()
        self.user_achievement = creating_base_achievement()

        payload = {
            'achievement_name': 'Для орг',
            'for_organization': True,
            'for_def_user': False,
        }
        self.org_achievement = creating_base_achievement(**payload)

    def test_manipulate_after_creating(self):
        self.assertEquals(self.user.user_profile.user_level, self.first_lvl)

    def test_success_update_user_level(self):
        """
        Verifies that the achievement status is correctly updated when progress changes,
        and the Celery task runs successfully. Also checks that the user level is updated.
        """
        achievement_progress_status = AchievementsProgressStatus.objects.get(
            user=self.user, achievement__achievement_name=self.user_achievement.achievement_name
        )
        self.assertEqual(achievement_progress_status.achievement, self.user_achievement)

        achievement_progress_status.progress_rn = 1
        achievement_progress_status.save()
        achievement_progress_status.refresh_from_db()

        result = check_achievements_status.delay(achievement_progress_status.id)

        self.assertTrue(result.successful())
        self.assertTrue(achievement_progress_status.is_achieved)

        self.user.user_profile.refresh_from_db()
        self.assertEqual(self.user.user_profile.user_level, self.second_lvl)

    def test_adding_new_achievements_to_users(self):
        new_achievement = creating_base_achievement(achievement_name='Нове досягнення')
        all_achievements = AchievementsProgressStatus.objects.filter(user=self.user)

        self.assertEqual(self.user.achievementsprogressstatus.all().count(), all_achievements.count())

    def test_deleting_achievement(self):
        achievement = Achievements.objects.first().delete()
        all_achievements = AchievementsProgressStatus.objects.filter(user=self.user)

        self.assertEqual(self.user.achievementsprogressstatus.all().count(), all_achievements.count())
