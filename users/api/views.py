import base64
import hashlib
from django.contrib import messages
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import qrcode
from urllib import response
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from users.api.permissions import TotpPermission
from users.api.utils import verify_totp_code
from users.models import User

from .serializers import RegistrationSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
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
                return Response({"message" :"Пожалуйста введите TOTP код"})
            else:
                token = serializer.get_token(user)
                return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)


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
    

class TotpSetupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user

        if not user.totp_enabled:
            secret_key = base64.b32encode(hashlib.sha1(user.username.encode()).digest()[:10]).decode().rstrip('=')
            user.totp_enabled = True
            user.totp_secret = secret_key
            user.save()
            return Response({"status":"success", "message": "TOTP верификация успешно установлена."})
        else:
            return Response({"status":"error", "message": "TOTP верификация уже установлена."})
        

    

class TotpVerifyView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        totp_code = request.data.get('totp_code')
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Некорректный логин'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.totp_enabled:
            return Response({'error': 'TOTP верификация не установлена'}, status=status.HTTP_400_BAD_REQUEST)
        
        if verify_totp_code(totp_code, user.totp_secret):
            serializer = MyTokenObtainPairSerializer()
            token = serializer.get_token(user)
            # del request.session['totp_login']
            return Response({'access_token': str(token.access_token), 'refresh_token': str(token)})
        else:
            return Response({'error': 'Неправильный TOTP код'}, status=status.HTTP_400_BAD_REQUEST)
        