from django.urls import path

from vault import views

app_name = "vault"

urlpatterns = [
    path("", views.vault, name="vault"),
    path("new-record", views.save_new_record, name="save"),
]
