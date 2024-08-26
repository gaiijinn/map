from django.views.generic import TemplateView
from rest_framework import generics, parsers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CreatorSubscriptions, UserProfile
from .serializers import CreatorSubscriptionsSerializer, UserProfileSerializer
from ..achievements.services.achievement_progress_updater import AchievementProgressController

# Create your views here.


class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().select_related("user", "user_level")
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        achievement_update = AchievementProgressController(achievements_id=3, users_id=self.get_object().id)
        achievement_update.progress_updater()
        return super().update(request, *args, **kwargs)


class CreatorSubscriptionsModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = CreatorSubscriptions.objects.all()
    serializer_class = CreatorSubscriptionsSerializer

    def get_queryset(self):
        return self.queryset.filter(
            subscriber=self.request.user.user_profile
        ).select_related("creator", "creator__user_profile")

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user.user_profile)


class UserProfilePage(TemplateView):
    template_name = "user-profile.html"


class UserCreationPage(TemplateView):
    template_name = "user-creating.html"


class UserLoginPage(TemplateView):
    template_name = "user-login.html"
