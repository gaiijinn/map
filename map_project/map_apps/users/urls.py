from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import users, UserProfileRetrieveUpdateDestroyAPIView

app_name = "users"

# router = DefaultRouter()

urlpatterns = [
    #path('', include(router.urls)),
    path("", users, name="users"),
    path("user-profile-update/", UserProfileRetrieveUpdateDestroyAPIView.as_view(), name="user-profile-update"),
]
