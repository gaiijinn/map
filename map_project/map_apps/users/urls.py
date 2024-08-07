from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreatorSubscriptionsModelViewSet, UserCreationPage,
                    UserLoginPage, UserProfileRetrieveUpdateDestroyAPIView,
                    UserProfileView)

app_name = "users"

router = DefaultRouter()
router.register('subscriptions', CreatorSubscriptionsModelViewSet)

urlpatterns = [
    path("api/v1/user-profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "api/v1/user-profile-update/",
        UserProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="user-profile-update-v1",
    ),
    path("api/v1/user-registration/", UserCreationPage.as_view(), name='user-registration'),
    path("api/v1/user-login/", UserLoginPage.as_view(), name='user-login'),

    path('api/v1/', include(router.urls)),
]
