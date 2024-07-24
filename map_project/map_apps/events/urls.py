from django.urls import path

from .views import EventListApiView

app_name = 'events'

urlpatterns = [
    path('api/event-list/', EventListApiView.as_view(), name='event-list'),
]
