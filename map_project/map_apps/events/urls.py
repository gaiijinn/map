from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventReadOnlyModelViewSet

app_name = "events"

router = DefaultRouter()
router.register("events", EventReadOnlyModelViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
