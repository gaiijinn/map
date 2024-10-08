from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TopUsers, UserCreationPage, UserLoginPage, UserProfilePage,
                    UserProfileRetrieveUpdateDestroyAPIView,
                    UserSubscriptionsModelViewSet)

app_name = "users"

router = DefaultRouter()
router.register("subscriptions", UserSubscriptionsModelViewSet)

urlpatterns = [
    path(
        "api/v1/user-profile-update/",
        UserProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="user-profile-update-v1",
    ),
    path("api/v1/top-users/", TopUsers.as_view(), name="top-users"),
    path("user-registration/", UserCreationPage.as_view(), name="user-registration"),
    path("user-login/", UserLoginPage.as_view(), name="user-login"),
    path("user-profile/", UserProfilePage.as_view(), name="user-profile"),
    path("api/v1/", include(router.urls)),
]
