from django.urls import include, path

from vault import views

app_name = "vault"

urlpatterns = [
    path("", views.vault, name="vault"),
    path("save-record/", views.save_record, name="save"),
    path("change-record/", views.get_record_form, name="change"),
    path("delete-record/", views.delete_record, name="delete"),
    path("new-category/", views.new_category, name="new-category"),
    path("api/", include("vault.api.urls", namespace="vault-api")),
]
