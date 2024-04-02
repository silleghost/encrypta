
from django.urls import path
from .views import CustomTokenObtainPairView, RegistrationAPIView, TotpSetupView, TotpVerifyView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users-api"

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('totp/setup/', TotpSetupView.as_view(), name='totp_setup'),
    path('totp/verify/', TotpVerifyView.as_view(), name='verify_totp'),
]