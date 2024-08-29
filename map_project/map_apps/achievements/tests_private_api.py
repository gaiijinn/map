from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..achievements.models import Achievements, AchievementsProgressStatus
from ..users.models import UserLevel

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


class PrivateAPITest(TestCase):
    def setUp(self) -> None:
        self.first_level = creating_level()
        self.achievement = creating_base_achievement()

        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

