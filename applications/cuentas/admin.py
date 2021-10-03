from django.contrib import admin

# Register your models here.
from .models import Cuentas,Cuotas,DetalleCuenta,Pagos

class CuentaAdmin(admin.ModelAdmin):
    list_display=('numero_cuenta','id','solicitante','garante','importe')

class PagoAdmin(admin.ModelAdmin):
    list_display=('cuota','importe','metodo_pago')


class DetalleCuentaAdmin(admin.ModelAdmin):
    list_display=('cuenta', 'producto','cantidad','descuento','subtotal')

class CuotasAdmin(admin.ModelAdmin):
    list_display=('cuenta','importe','numero_cuota','id','fecha_vencimiento','estado','cuenta')

admin.site.register(Cuentas,CuentaAdmin)
admin.site.register(Cuotas,CuotasAdmin)
admin.site.register(DetalleCuenta,DetalleCuentaAdmin)
admin.site.register(Pagos,PagoAdmin)