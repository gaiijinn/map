import time

from django.http import HttpResponseServerError


class TestMiddleware:
    """Just test middleware"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        time.sleep(1)
        execution_time = time.time() - start_time

        if execution_time > 5:
            return HttpResponseServerError(f"Request is too long: {execution_time} seconds, mid 1")

        return response
