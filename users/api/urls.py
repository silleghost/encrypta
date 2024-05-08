from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.api.views import (
    CustomTokenObtainPairView,
    RegistrationAPIView,
    TotpSetupView,
    # TotpVerifyView,
    logout,
)


app_name = "users-api"

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="registration"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("totp/setup/", TotpSetupView.as_view(), name="totp_setup"),
    # path("totp/verify/", TotpVerifyView.as_view(), name="verify_totp"),
    path("logout/", logout, name="logout"),
]
