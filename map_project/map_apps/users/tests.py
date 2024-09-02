from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..achievements.models import Achievements, AchievementsProgressStatus
from .models import User, UserLevel, UserProfile, UserSubscription
from .serializers import UserProfileSerializer

USER_UPDATE = reverse("users:user-profile-update-v1")
SUBSCRIPTION_URL = reverse("users:usersubscription-list")


def subscription_detail(subs_id):
    return reverse("users:subscriptions-detail", args=[subs_id])


def user_creating(**params):
    return get_user_model().objects.create_user(**params)


def creating_first_level(**params):
    defaults = {"level_name": "Новачок", "low_range": 0, "top_range": 10}

    defaults.update(params)

    return UserLevel.objects.create(**defaults)


def creating_base_achievement(**params):
    defaults = {
        "achievement_name": "Початківець",
        "descr_achievement": "some text",
        "given_exp": 11,
        "final_value": 1,
        "for_organization": False,
        "for_def_user": True,
    }

    defaults.update(params)

    return Achievements.objects.create(**defaults)


class PublicUserApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.create_user_url = "/api/djoser/users/"

    def test_user_access_creating(self):
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "re_password": "test123",
            "first_name": "vlad",
            "last_name": "ruban",
        }

        result = self.client.post(self.create_user_url, payload)
        self.assertEquals(result.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", result.data)

        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_failed_user_creating(self):
        payload = {
            "email": "test@example.com",
            "password": "test123",
            "re_password": "test1232",
            "first_name": "vlad",
            "last_name": "ruban",
        }

        result = self.client.post(self.create_user_url, payload)
        self.assertEquals(result.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserAPITest(TestCase):
    def setUp(self) -> None:
        self.create_user_url = "/api/djoser/users/"
        self.client = APIClient()

        self.first_lvl = creating_first_level()
        self.first_achievement = creating_base_achievement()
        self.second_achievement = creating_base_achievement(for_def_user=False)

        self.payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Vlad",
            "last_name": "Ruban",
        }
        self.user = user_creating(**self.payload)

        self.client.force_authenticate(user=self.user)

    def test_get_user(self):
        response = self.client.get(USER_UPDATE)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()

        user_profile = UserProfile.objects.get(user=self.user)
        serializer = UserProfileSerializer(user_profile)

        self.assertEqual(response_data, serializer.data)

    @mock.patch(
        'map_apps.achievements.services.decorators.decorators.handler_success_request_for_achievement_update').start()
    def test_user_retrieve_success(self):
        payload = {
            "about_me": "123g45",
            "user": {
                "last_name": "Don",
            },
        }

        response = self.client.patch(USER_UPDATE, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.user_profile.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(self.user.user_profile.about_me, payload["about_me"])
        self.assertEqual(self.user.last_name, payload["user"]["last_name"])
        self.assertEqual(self.user.first_name, self.payload["first_name"])

    @mock.patch(
        'map_apps.achievements.services.decorators.decorators.handler_success_request_for_achievement_update').start()
    def test_user_retrieve_failed(self):
        payload = {
            "user": {
                "email": "somenew@example.com",
                "password": "newpas11111",
                "rating": "8",
            }
        }

        request = self.client.patch(USER_UPDATE, payload, format="json")
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        self.assertNotEqual(self.user.email, payload["user"]["email"])
        self.assertNotEqual(self.user.rating, payload["user"]["rating"])
        self.assertFalse(self.user.check_password(payload["user"]["password"]))

    def test_user_deleting(self):
        request = self.client.delete(USER_UPDATE)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    @mock.patch(
        'map_apps.achievements.services.decorators.decorators.handler_success_request_for_achievement_update').start()
    def test_subscription_to_user(self):
        new_user = user_creating(email='test2@example.com')

        payload = {
            'subscribe_to': new_user.id
        }

        request = self.client.post(SUBSCRIPTION_URL, payload)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.user.subscriptions_made.count(), 1)


    # def test_subscription_depends_on_user(self):
    #     new_user = user_creating(email='test2@example.com')
    #     new_user2 = user_creating(email='test3@example.com')
    #
    #     new_user.subscriptions.add(new_user2)
    #
    #     payload = {
    #         'subscribe_to': new_user.id
    #     }
    #
    #     request = self.client.post(SUBSCRIPTION_URL, payload)
    #     self.assertEqual(request.status_code, status.HTTP_201_CREATED)