from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .serializers import EventListSerializer, EventRetrieveSerializer
from .models import Events
from rest_framework.response import Response

# Create your views here.


class EventReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = (Events.objects.all().select_related('creator', 'creator__user_profile').
                prefetch_related('eventtypes__event_type'))
    filterset_fields = ('event_types', 'event_status', 'event_age', 'begin_day', 'created_by_org')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventRetrieveSerializer
        return EventListSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
