import logging
from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

logger = logging.getLogger('achievements')


def handle_object_not_found(warning_message="Object not found"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ObjectDoesNotExist:
                logger.warning(warning_message)
                return None

        return wrapper

    return decorator


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
