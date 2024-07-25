from django.urls import path, include

from .views import EventReadOnlyModelViewSet
from rest_framework.routers import DefaultRouter

app_name = 'events'

router = DefaultRouter()
router.register('api/events', EventReadOnlyModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
