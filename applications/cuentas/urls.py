from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views as cuentas_views


router = DefaultRouter()
router.register(r'', cuentas_views.cuentasViewSet, basename='cuentas')

urlpatterns = [
    path('lista', include(router.urls)),
    path('nuevacuenta', cuentas_views.NuevaCuenta.as_view(),name="nueva_cuenta"),
]   