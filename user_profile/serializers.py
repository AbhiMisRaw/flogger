from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .constants import Error

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "dob",
            "is_active",
            "created_at",
            "last_login",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "created_at",
            "last_login",
        ]
    

class UserRegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(required=True,write_only=True)
    confirm_password = serializers.CharField(required=True,write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "password": Error.PASSWORD_MATCHING_ERROR
            })

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({
                "email": "User with this email already exists"
            })

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["email"],
            password=data["password"]
        )

        if not user:
            raise AuthenticationFailed(detail=Error.LOGIN_ERROR)

        if not user.is_active:
            raise AuthenticationFailed(detail=Error.USER_INACTIVE)

        data["user"] = user
        data["tokens"] = self.get_tokens_for_user(user)
        return data

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
