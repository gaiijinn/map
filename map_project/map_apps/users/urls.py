from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserProfileRetrieveUpdateDestroyAPIView, UserProfileView, UserCreationPage, UserLoginPage,
                    CreatorSubscriptionsModelViewSet)

app_name = "users"

router = DefaultRouter()
router.register('subscriptions', CreatorSubscriptionsModelViewSet)

urlpatterns = [
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "api/user-profile-update/",
        UserProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="user-profile-update",
    ),
    path("user-registration/", UserCreationPage.as_view(), name='user-registration'),
    path("user-login/", UserLoginPage.as_view(), name='user-login'),
]

urlpatterns += router.urls
