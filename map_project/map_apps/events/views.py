from django.shortcuts import render
from rest_framework import generics
from .serializers import EventSerializer
from .models import Events

# Create your views here.


class EventListApiView(generics.ListAPIView):
    pagination_class = None
    serializer_class = EventSerializer
    queryset = Events.objects.all().select_related('creator').prefetch_related('event_types')
