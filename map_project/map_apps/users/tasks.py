from celery import shared_task
from django.core.cache import cache

from ..achievements.services.top_users_calculating import TopUsersCalculator
from .serializers import TopUsersSerializer


@shared_task()
def get_top_users():
    top_users = cache.get('top_users')

    if top_users is None:
        users = TopUsersCalculator()
        top_users_query_set = users.top_user_calculator()

        serializer = TopUsersSerializer(top_users_query_set, many=True)
        top_users = serializer.data

        cache.set('top_users', top_users, 60)

    return top_users
