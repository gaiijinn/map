import logging
from functools import wraps

from django.http import Http404
from rest_framework import status

logger_warning = logging.getLogger('achievement_warning')
logger_info = logging.getLogger('achievement_info')


def handle_msg_log_404(message=''):
    def log_404(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Http404 as error:
                logger_warning.warning(f"{str(error)} | {message}")
                raise
        return wrapper
    return log_404


def handler_success_request_for_achievement_update(achievement_keyword=None, update_func=None):
    """
    This decorator is responsible to handle the request and check it to 200 status code, and then start our
    'update_func' to update achievement progress.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK and achievement_keyword is not None and update_func:
                update_func(user_id=request.user.id, achievement_keyword=achievement_keyword)
            return response
        return wrapper
    return decorator
