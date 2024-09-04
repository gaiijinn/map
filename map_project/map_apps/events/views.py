from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, mixins, parsers, permissions,
                            status, viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import EventGuests, Events
from .paginators import CustomEventPageNumberPagination
from .serializers import (EventGuestSerializer, EventListSerializer,
                          EventRetrieveSerializer)

# Create your views here.


class EventReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Events.objects.all().order_by("-id")
    pagination_class = CustomEventPageNumberPagination
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )

    filterset_fields = (
        "event_types",
        "event_status",
        "event_age",
        "begin_day",
        "created_by_org",
    )

    search_fields = ("name",)
    ordering_fields = ("price",)

    def get_queryset(self):
        if self.action == "list":
            return (
                Events.objects.all()
                .filter(result_revue="approved")
                .exclude(event_status="ended")
                .select_related(
                    "creator", "creator__user_profile", "creator__organizations"
                )
                .prefetch_related("eventtypes__event_type")
                .order_by("-id")
            )
        return (
            Events.objects.all()
            .filter(result_revue="approved")
            .select_related(
                "creator", "creator__user_profile", "creator__organizations"
            )
            .prefetch_related("eventtypes__event_type", "eventguests__guest")
            .order_by("-id")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EventRetrieveSerializer
        return EventListSerializer

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization", "X-Anonymous-User"))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.event_status == "ended":
            return Response(
                {"detail": "Event has ended and is no longer available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(instance)
        response_data = serializer.data

        total_guests = instance.eventguests.count()
        response_data["total_guests"] = total_guests

        return Response(response_data)

    @method_decorator(cache_page(30))
    @method_decorator(vary_on_headers("Authorization", "X-Anonymous-User"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class EventGuestCustomViewSet(mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    queryset = EventGuests.objects.all()
    serializer_class = EventGuestSerializer
    permission_classes = (permissions.IsAuthenticated, )
    parser_classes = (parsers.JSONParser, )

    def get_queryset(self):
        return self.queryset.filter(event__event_status="not_started", guest=self.request.user)

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)
