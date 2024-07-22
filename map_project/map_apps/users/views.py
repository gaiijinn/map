from django.shortcuts import HttpResponse, render
from rest_framework import generics
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


def users(request):
    return HttpResponse("200")


class UserProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().select_related('user', 'user_level')
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.queryset.get(user=self.request.user)
