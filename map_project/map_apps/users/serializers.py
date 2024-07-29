from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import User, UserLevel, UserProfile


class CustomCreateUserSerializer(UserCreateSerializer):
    re_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        fields = (
            "email",
            "password",
            "re_password",
            "first_name",
            "last_name",
            "is_org",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError(_("Паролі не відповідають один одному"))
        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password")
        return super().create(validated_data)


class UserLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLevel
        fields = ("level_name", "low_range", "top_range")


class BaseUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "is_verif",
            "rating",
            "profile_picture",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    user = BaseUserProfileSerializer()
    user_level = UserLevelSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("user_level", "about_me", "inst_link", "want_newsletters", "user")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        if user_data:
            user_serializer = BaseUserProfileSerializer(
                instance.user, data=user_data, partial=True
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        return super().update(instance, validated_data)
