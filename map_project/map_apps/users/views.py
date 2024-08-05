from django.views.generic import TemplateView
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied

from .models import UserProfile, CreatorSubscriptions
from .serializers import UserProfileSerializer, CreatorSubscriptionsSerializer

# Create your views here.


class IsVerifPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_verif:
            raise PermissionDenied("У вас не активований акаунт")
        return user.is_verif


class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().select_related("user", "user_level")
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.queryset.get(user=self.request.user)


class CreatorSubscriptionsModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsVerifPermission)
    queryset = CreatorSubscriptions.objects.all()
    serializer_class = CreatorSubscriptionsSerializer

    def get_queryset(self):
        return (self.queryset.filter(subscriber=self.request.user.user_profile).
                select_related('creator', 'creator__user_profile'))

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user.user_profile)


class UserProfileView(TemplateView):
    template_name = "user-profile.html"


class UserCreationPage(TemplateView):
    template_name = "user-creating.html"


class UserLoginPage(TemplateView):
    template_name = "user-login.html"
