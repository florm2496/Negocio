from django.urls import path,include

from applications.productos.serializers import RubrosSerializer
from .views import  ProductosViewSet , NuevosIngresos,ReporteIngresos,DetallesByIngreso,RubrosViewSet,ABMProducto
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'lista', ProductosViewSet, basename='productos')
router.register(r'rubros',RubrosViewSet,basename='rubros')


urlpatterns = [
    path('', include(router.urls)),
    path('nuevosingresos',NuevosIngresos.as_view() ,name='nuevosigresos'),
    path('altaproducto',ABMProducto.as_view() ,name='alta-producto'),
    path('actualizarproducto/<int:codigo>',ABMProducto.as_view() ,name='actualizar-producto'),
    path('bajaproducto/<str:codigo>',ABMProducto.as_view() ,name='baja-producto'),
    path('listaingresos',ReporteIngresos.as_view() ,name='listaingresos'),
    path('detallesingresos',DetallesByIngreso.as_view() ,name='detallesingreso'),
    #path('nuevoproducto', Productos.as_view(),name="nuevo_producto"),
]   