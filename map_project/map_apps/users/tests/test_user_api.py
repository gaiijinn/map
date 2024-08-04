from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


def user_creating(**params):
    return get_user_model().objects.create_user(**params)


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
        
