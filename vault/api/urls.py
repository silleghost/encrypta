from django.urls import include, path
from . import views

from rest_framework import routers

app_name = "api"

router = routers.DefaultRouter()
router.register(r'records', views.RecordsViewSet)
router.register(r'categories', views.CategoriesViewSet)


urlpatterns = [
    path('', include(router.urls))
]