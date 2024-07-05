from rest_framework import serializers

from .models import Achievements


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = "__all__"
