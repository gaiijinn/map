import logging
from functools import wraps

from django.http import Http404
from rest_framework import status

logger = logging.getLogger('achievement_warning')


def handle_msg_log_404(message=''):
    def log_404(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Http404 as error:
                logger.warning(f"{str(error)} | {message}")
                raise
        return wrapper
    return log_404


def handler_success_request_for_achievement_update(achievement_id=None, update_func=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            response = func(self, request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK and achievement_id is not None and update_func:
                update_func(user_id=request.user.id, achievement_id=achievement_id)

            return response
        return wrapper
    return decorator
