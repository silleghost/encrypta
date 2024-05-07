import base64
import hashlib

import pyotp

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.api.utils import generate_secret_key, verify_totp_code
from users.api.serializers import RegistrationSerializer
from users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.user
            if user.totp_enabled:
                # request.session['totp_login'] = True
                return Response({"message": "Пожалуйста введите TOTP код"})
            else:
                token = serializer.get_token(user)
                return Response(
                    {"access": str(token.access_token), "refresh": str(token)}, status=status.HTTP_200_OK
                )


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TotpSetupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.totp_enabled:
            secret_key = generate_secret_key()
            user.totp_enabled = True
            user.totp_secret = secret_key
            user.save()
            return Response(
                {
                    "status": "success",
                    "message": "TOTP верификация успешно установлена.",
                }
            )
        else:
            return Response(
                {"status": "error", "message": "TOTP верификация уже установлена."}
            )


class TotpVerifyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        totp_code = request.data.get("totp_code")
        username = request.data.get("username")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Некорректный логин"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.totp_enabled:
            return Response(
                {"error": "TOTP верификация не установлена"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if verify_totp_code(totp_code, user.totp_secret):
            serializer = MyTokenObtainPairSerializer()
            token = serializer.get_token(user)
            return Response(
                {"access_token": str(token.access_token), "refresh_token": str(token)}
            )
        else:
            return Response(
                {"error": "Неправильный TOTP код"}, status=status.HTTP_400_BAD_REQUEST
            )
