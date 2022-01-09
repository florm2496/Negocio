
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views as cuentas_views


router = DefaultRouter()
router.register(r'', cuentas_views.cuentasViewSet, basename='cuentas')
#router.register(r'cuotas', cuentas_views.CuotasView , basename="cuotas")

urlpatterns = [
    path('lista', include(router.urls)),
    path('registrarcuenta',cuentas_views.RegistrarCuenta.as_view(),name="registrar_cuenta"),
    path('nuevacuenta', cuentas_views.NuevaCuenta.as_view(),name="nueva_cuenta"),
    path('cuentascliente', cuentas_views.CuentasByCliente.as_view(),name="cuentascliente"),
    path('nuevodetallecuenta', cuentas_views.NuevoDetalleCuenta.as_view(),name="nuevodetallecuenta"),
    path('detallescuenta', cuentas_views.DetallesCuenta.as_view(),name="detallescuenta"),
    path('numerocuenta', cuentas_views.get_num_cuenta.as_view(),name="numcuenta"),
    path('reportescuentas', cuentas_views.ReporteVentas.as_view(),name="cuentas"),
    #path('cuotas', cuentas_views.CuotasView.as_view(),name="cuotas"),
    path('cuotascuenta', cuentas_views.CuotasCuentaViews.as_view(),name="cuotas"),
    path('nuevopago', cuentas_views.NuevoPago.as_view(),name="nuevopago"),
    path('refinanciarcuenta', cuentas_views.RefinanciarCuenta.as_view(),name="refinanciar-cuenta"),

    
    
]   