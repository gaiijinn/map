from celery import shared_task

from ..achievements.services.top_users_calculating import TopUsersCalculator


@shared_task
def get_top_users():
    users = TopUsersCalculator()
    top_users = users.top_user_calculator()

    return top_users
