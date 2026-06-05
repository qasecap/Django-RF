from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import CustomUser


class RegisterValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('User with this email already exists!')
        return email


class AuthValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ConfirmValidateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)
