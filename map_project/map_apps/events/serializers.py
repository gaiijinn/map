from rest_framework import serializers
from .models import Events, EventType, EventTypes, EventImgs
from ..users.models import User


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ('name', )


class EventTypesSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer()

    class Meta:
        model = EventTypes
        fields = ('event_type', )


class EventCreatorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'profile_picture')

    def get_name(self, obj):
        if obj.user_profile:
            return obj.get_full_name()
        else:
            return obj.organizations.name


class EventListSerializer(serializers.ModelSerializer):
    event_types = EventTypesSerializer(many=True, source='eventtypes', read_only=True)
    creator = EventCreatorSerializer(read_only=True)
    event_status = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Events
        fields = (
            'id', 'creator', 'event_types', 'event_status', 'event_age',
            'begin_day', 'begin_time', 'end_time', 'name', 'address', 'description',
            'main_photo', 'coordinates', 'price', 'created_by_org', 'rating'
        )

    def get_event_status(self, obj):
        return obj.get_event_status_display()

    def get_rating(self, obj):
        return obj.creator.rating


class EventImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImgs
        fields = ('img', )


class EventRetrieveSerializer(serializers.ModelSerializer):
    event_types = EventTypesSerializer(many=True, source='eventtypes', read_only=True)
    creator = EventCreatorSerializer(read_only=True)
    event_status = serializers.SerializerMethodField(read_only=True)
    eventimgs = EventImgSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Events
        fields = (
            'creator', 'event_types', 'event_status', 'event_age', 'rating',
            'begin_day', 'begin_time', 'end_time', 'name', 'address',
            'description', 'main_photo', 'coordinates', 'price', 'created_by_org', 'eventimgs',
        )

    def get_event_status(self, obj):
        return obj.get_event_status_display()

    def get_rating(self, obj):
        return obj.creator.rating
