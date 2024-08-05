from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserLevel, User
from ..achievements.models import Achievements, AchievementsProgressStatus
from ..achievements.serializers import AchievementProgressStatusSerializer


ACHIEVEMENT_STATUS_URL = reverse('achievements:achievement-status')


def user_creating(**params):
    return get_user_model().objects.create_user(**params)


def creating_first_level(**params):
    defaults = {
        'level_name': 'Початківець',
        'low_range': 0,
        'top_range': 10
    }

    defaults.update(params)

    return UserLevel.objects.create(**defaults)


def creating_base_achievement(**params):
    defaults = {
        'achievement_name': 'Початківець',
        'descr_achievement': 'some text',
        'given_exp': 10,
        'final_value': 10,
        'for_organization': True,
        'for_def_user': True,
    }

    defaults.update(params)

    return Achievements.objects.create(**defaults)


class PublicUserApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.create_user_url = '/api/djoser/users/'

    def test_user_access_creating(self):
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            're_password': 'test123',
            'first_name': 'vlad',
            'last_name': 'ruban'
        }

        result = self.client.post(self.create_user_url, payload)
        self.assertEquals(result.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', result.data)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_failed_user_creating(self):
        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            're_password': 'test1232',
            'first_name': 'vlad',
            'last_name': 'ruban'
        }

        result = self.client.post(self.create_user_url, payload)
        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserAPITest(TestCase):
    def setUp(self) -> None:
        self.create_user_url = '/api/djoser/users/'
        self.client = APIClient()

    def test_after_creating_manipulating(self):
        first_lvl = creating_first_level()
        first_achievement = creating_base_achievement()
        second_achievement = creating_base_achievement(for_def_user=False)

        payload = {
            'email': 'test@example.com',
            'password': 'test123',
            're_password': 'test123',
            'first_name': 'vlad',
            'last_name': 'ruban'
        }

        result = self.client.post(self.create_user_url, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=payload['email'])
        self.assertEquals(user.user_profile.user_level, first_lvl)

        user_achievement = AchievementsProgressStatus.objects.filter(user=user)
        self.assertEqual(user.achievementsprogressstatus.count(), user_achievement.count())

