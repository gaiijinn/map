from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "events"

router = DefaultRouter()
router.register("events", views.EventReadOnlyModelViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/set-guest-to-event/", views.EventGuestCreateAPIView.as_view(), name='set-guest-to-event')
]
