from django.urls import path

from vault import views

app_name = "vault"

urlpatterns = [
    path("", views.vault, name="vault"),
]
