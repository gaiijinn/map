from django.shortcuts import render
from rest_framework import viewsets

from .models import Achievements
from .serializers import AchievementSerializer

# Create your views here.


class AchievementsModelViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementSerializer
    queryset = Achievements.objects.all()
