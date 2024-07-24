from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserProfileRetrieveUpdateDestroyAPIView, UserProfileView

app_name = "users"

# router = DefaultRouter()

urlpatterns = [
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/user-profile-update/', UserProfileRetrieveUpdateDestroyAPIView.as_view(), name='user-profile-update'),
]
