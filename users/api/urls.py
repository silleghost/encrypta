
from django.urls import path
from .views import RegistrationAPIView, getRoutes

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users-api"

urlpatterns = [
    path('', getRoutes),
    path('registration/', RegistrationAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]