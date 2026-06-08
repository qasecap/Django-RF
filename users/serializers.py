from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import ConfirmationCode

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('User already exists!')
        return email


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ConfirmUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        code = data['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found!")

        try:
            confirmation = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Confirmation code not found!")

        if confirmation.code != code:
            raise serializers.ValidationError("Code is wrong!")

        data['user'] = user
        return data

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save()
        user.confirmation_code.delete()
        return user
