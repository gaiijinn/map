from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AchievementSerializer
from .models import Achievements
# Create your views here.


class AchievementsModelViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementSerializer
    queryset = Achievements.objects.all()
