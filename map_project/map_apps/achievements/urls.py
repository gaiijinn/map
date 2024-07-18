from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AchievementsStatusApiView

app_name = "achievements"

urlpatterns = [
    path("achievement-status/", AchievementsStatusApiView.as_view(), name='achievement-status'),
]
