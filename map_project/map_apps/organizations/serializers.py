from rest_framework import serializers

from .models import Organizations, OrganizationImgs


class OrganizationsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = '__all__'


class OrganizationImgsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationImgs
        fields = ('photo', )