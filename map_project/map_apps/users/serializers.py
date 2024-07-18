from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User
from ..organizations.models import Organizations
from ..organizations.serializers import OrganizationsCreateSerializer
from django.conf import settings


class CustomCreateUserSerializer(UserCreateSerializer):
    re_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    organization = OrganizationsCreateSerializer(required=False)

    class Meta(UserCreateSerializer.Meta):
        fields = (
            "email",
            "password",
            "re_password",
            "first_name",
            "last_name",
            "is_org",
            "organization",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError(_("Паролі не відповідають один одному"))
        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password")
        organization_data = validated_data.pop("organization", None)

        user = User.objects.create_user(**validated_data)

        is_org = validated_data.get("is_org")

        if is_org and organization_data:
            Organizations.objects.create(**organization_data)

        return user
