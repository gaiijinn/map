from django.shortcuts import HttpResponse, render
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer

# Create your views here.


def users(request):
    return HttpResponse("200")


class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().select_related('user', 'user_level')
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.queryset.get(user=self.request.user)
