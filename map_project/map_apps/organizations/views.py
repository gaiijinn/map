from rest_framework import generics, viewsets

from .serializers import OrganizationsCreateSerializer

# Create your views here.

class OrganizationCreateAPIView(generics.CreateAPIView):
    serializer_class = OrganizationsCreateSerializer
