from django.urls import include, path

from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("settings/", views.settings, name="settings"),
    path("logout/", views.logout, name="logout"),
    path("delete-user/", views.delete, name="delete"),
    path("api/", include("users.api.urls", namespace="users-api")),
]
