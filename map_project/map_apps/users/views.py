from django.shortcuts import HttpResponse, render
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer

from django.views.generic import TemplateView
# Create your views here.


class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().select_related('user', 'user_level')

    def get_object(self):
        return self.queryset.get(user=self.request.user)


class UserProfileView(TemplateView):
    template_name = "user-profile.html"
