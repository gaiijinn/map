from rest_framework import serializers

from .models import Organizations


class OrganizationsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = '__all__'
