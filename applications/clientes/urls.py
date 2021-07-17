from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views as clientes_views


router = DefaultRouter()
router.register(r'inicio', clientes_views.clientesViewSet, basename='clientes')
urlpatterns = [
    path('', include(router.urls))
]   