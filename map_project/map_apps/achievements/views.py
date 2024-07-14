from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import AchievementsProgressStatus
from .serializers import AchievementProgressStatusSerializer
from django.db.models import Count

# Create your views here.


class AchievementsModelViewSet(viewsets.ModelViewSet):
    serializer_class = AchievementProgressStatusSerializer
    queryset = AchievementsProgressStatus.objects.all().order_by('-id')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related('achievement')

    # @method_decorator(cache_page(60 * 15))  # кеширование на 15 минут
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data, 'total_amount': self.get_queryset().aggregate(total=Count('id'))}
        response.data = response_data

        return response
