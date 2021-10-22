from django.urls import path,include
from .views import ProductosViewSet , NuevosIngresos,ReporteIngresos,DetallesByIngreso
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ProductosViewSet, basename='productos')


urlpatterns = [
    path('', include(router.urls)),
    path('nuevosingresos',NuevosIngresos.as_view() ,name='nuevosigresos'),
    path('listaingresos',ReporteIngresos.as_view() ,name='listaingresos'),
    path('detallesingresos',DetallesByIngreso.as_view() ,name='detallesingreso'),
    #path('nuevoproducto', Productos.as_view(),name="nuevo_producto"),
]   