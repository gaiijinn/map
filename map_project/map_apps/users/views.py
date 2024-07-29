from django.shortcuts import HttpResponse, render
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import UserProfile
from .serializers import UserProfileSerializer

# Create your views here.


class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().select_related("user", "user_level")
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.queryset.get(user=self.request.user)


class UserProfileView(TemplateView):
    template_name = "user-profile.html"


class UserCreationPage(TemplateView):
    template_name = "user-creating.html"
