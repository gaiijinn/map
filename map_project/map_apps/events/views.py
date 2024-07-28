from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .serializers import EventListSerializer, EventRetrieveSerializer
from .models import Events
from django.db.models import Count
from rest_framework.response import Response


# Create your views here.


class EventReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Events.objects.all()
    filterset_fields = ('event_types', 'event_status', 'event_age', 'begin_day', 'created_by_org')

    def get_queryset(self):
        if self.action == 'list':
            return (Events.objects.all().select_related('creator', 'creator__user_profile', 'creator__organizations').
                    prefetch_related('eventtypes__event_type')).exclude(event_status='ended')
        return (Events.objects.all().select_related('creator', 'creator__user_profile', 'creator__organizations').
                prefetch_related('eventtypes__event_type', 'eventguests__guest'))

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventRetrieveSerializer
        return EventListSerializer

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_headers("Authorization", "X-Anonymous-User"))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = serializer.data
        total_guests = instance.eventguests.count()
        response_data['total_guests'] = total_guests

        return Response(response_data)

    @method_decorator(cache_page(30))
    @method_decorator(vary_on_headers("Authorization", "X-Anonymous-User"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
