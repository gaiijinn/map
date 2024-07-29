from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventReadOnlyModelViewSet

app_name = "events"

router = DefaultRouter()
router.register("api/events", EventReadOnlyModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
