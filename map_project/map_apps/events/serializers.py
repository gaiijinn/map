from rest_framework import serializers
from .models import Events, EventType, EventTypes


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ('name', )


class EventTypesSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer()

    class Meta:
        model = EventTypes
        fields = ('event_type', )


class EventSerializer(serializers.ModelSerializer):
    event_types = EventTypesSerializer(many=True, source='eventtypes')

    class Meta:
        model = Events
        fields = ('creator', 'event_types', 'event_status', 'event_age', 'begin_day', 'begin_time', 'end_time', 'name',
                  'address', 'description', 'main_photo', 'coordinates', 'price', 'created_by_org')
