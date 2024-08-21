from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import AchievementsProgressStatus
from .serializers import AchievementProgressStatusSerializer

# Create your views here.


class AchievementsStatusApiView(generics.ListAPIView):
    serializer_class = AchievementProgressStatusSerializer
    queryset = AchievementsProgressStatus.objects.all().order_by("-id")
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("is_achieved",)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related(
            "achievement"
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        total = cache.get("total")

        if total is None:
            total = self.get_queryset().aggregate(total=Count("id"))
            cache.set("total", total, 24 * 60 * 60)

        achieved = (
            self.get_queryset()
            .filter(is_achieved=True)
            .aggregate(achieved=Count("is_achieved"))
        )

        response_data = {"result": response.data, "achieved": achieved, "all": total}

        response.data = response_data
        return response
