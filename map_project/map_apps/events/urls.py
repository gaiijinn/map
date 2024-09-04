from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "events"

router = DefaultRouter()
router.register("events", views.EventReadOnlyModelViewSet)
router.register("events-guests", views.EventGuestCustomViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
