import random

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import ConfirmationCode, CustomUser
from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmValidateSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegisterValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            is_active=False,
        )

        code = str(random.randint(100000, 999999))
        ConfirmationCode.objects.create(user=user, code=code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 'code': code}
        )


class AuthorizationView(APIView):
    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

        if user is not None:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ConfirmView(APIView):
    def post(self, request):
        serializer = ConfirmValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'User not found!'}
            )

        try:
            confirmation = ConfirmationCode.objects.get(user=user, code=code)
        except ConfirmationCode.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': 'Code is wrong!'}
            )

        user.is_active = True
        user.save()
        confirmation.delete()
        return Response(data={'message': 'User confirmed successfully!'})
