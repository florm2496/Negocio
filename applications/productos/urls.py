from django.urls import path,include
from .views import Productos
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', Productos, basename='productos')

urlpatterns = [
    path('', include(router.urls)),
    #path('nuevoproducto', Productos.as_view(),name="nuevo_producto"),
]   