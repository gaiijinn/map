from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Achievements
from .serializers import AchievementSerializer

# Create your views here.


class AchievementsModelViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementSerializer
    queryset = Achievements.objects.all()
    permission_classes = (IsAuthenticated, )

    @method_decorator(cache_page(60 * 15))  # кеширование на 15 минут
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
