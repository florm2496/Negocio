from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views as cuentas_views


router = DefaultRouter()
router.register(r'inicio', cuentas_views.cuentasViewSet, basename='cuentas')
urlpatterns = [
    path('', include(router.urls))
]   