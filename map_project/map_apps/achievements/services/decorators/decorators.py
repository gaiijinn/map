from functools import wraps

from django.core.exceptions import ObjectDoesNotExist


def handle_no_object(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist:
            return None
    return wrapper
