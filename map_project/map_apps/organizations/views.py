from rest_framework import viewsets
from rest_framework import generics
from .serializers import OrganizationsCreateSerializer


# Create your views here.

class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = OrganizationsCreateSerializer
