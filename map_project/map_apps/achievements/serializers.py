from rest_framework import serializers

from .models import Achievements, AchievementsProgressStatus


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = "__all__"


class AchievementProgressStatusSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = AchievementsProgressStatus
        fields = "__all__"
