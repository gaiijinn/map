import logging
from functools import wraps

from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger("main")


def handle_object_not_found(warning_message="Object not found"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get("user_id", "unknown")
            try:
                return func(*args, **kwargs)
            except ObjectDoesNotExist:
                logger.warning(warning_message)
                return None

        return wrapper

    return decorator
