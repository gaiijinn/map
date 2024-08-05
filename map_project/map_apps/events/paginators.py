from rest_framework.pagination import PageNumberPagination


class CustomEventPageNumberPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = None
    max_page_size = None
