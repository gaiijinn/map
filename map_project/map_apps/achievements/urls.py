from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AchievementsModelViewSet

app_name = 'achievements'

router = DefaultRouter()
router.register('achievs', AchievementsModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
