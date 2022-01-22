from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import getClientesCuenta,clientesViewSet,bajaCliente


router = DefaultRouter()
router.register(r'',clientesViewSet, basename='clientes')

urlpatterns = [
    path('viewset/', include(router.urls)),
    #path('apiclientes/<int:pk>',clienteAPIVIEW.as_view() ,name="cliente-apiview"),
    path('getclientecuenta/',getClientesCuenta.as_view() ,name="cliente-cuenta"),
    path('bajacliente/',bajaCliente.as_view(),name='baja-cliente')
    
]   