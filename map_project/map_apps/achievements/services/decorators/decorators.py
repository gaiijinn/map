import logging
from functools import wraps

from map_apps.achievements.models import AchievementsProgressStatus
from rest_framework import status

logger_warning = logging.getLogger('achievement_warning')
logger_info = logging.getLogger('achievement_info')


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AchievementsProgressStatus.DoesNotExist:
            logger_warning.warning(
                f"Achievement progress status not found for user and keyword ")
    return wrapper


def handler_success_request_for_achievement_update(status_codes=None,
                                                   achievement_keyword=None,
                                                   update_func=None):
    """
    This decorator is responsible for handling the request and checking if its status code is in the list of
    'status_codes', and then starts our 'update_func' to update achievement progress.
    """
    if status_codes is None:
        status_codes = [status.HTTP_200_OK]

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)
            if response.status_code in status_codes and achievement_keyword is not None and update_func:
                update_func(user_id=request.user.id, achievement_keyword=achievement_keyword)
            return response
        return wrapper

    return decorator
