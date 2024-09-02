from django.views.generic import TemplateView
from rest_framework import generics, mixins, parsers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..achievements.services.achievement_progress_updater import \
    progress_updater
from ..achievements.services.decorators.decorators import \
    handler_success_request_for_achievement_update
from .models import User, UserProfile, UserSubscription
from .serializers import (UserProfileSerializer,
                          UserSubscriptionCreationSerializer,
                          UserSubscriptionSerializer)

# Create your views here.


class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().select_related("user", "user_level")
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)
        
    def get_object(self):
        return self.queryset.get(user=self.request.user)

    @handler_success_request_for_achievement_update(achievement_keyword='UP', update_func=progress_updater)
    def patch(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class UserSubscriptionsModelViewSet(mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.CreateModelMixin,
                                    viewsets.GenericViewSet):
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-subscribe_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSubscriptionCreationSerializer
        return self.serializer_class

    @handler_success_request_for_achievement_update(achievement_keyword='CS', update_func=progress_updater)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserProfilePage(TemplateView):
    template_name = "user-profile.html"


class UserCreationPage(TemplateView):
    template_name = "user-creating.html"


class UserLoginPage(TemplateView):
    template_name = "user-login.html"
