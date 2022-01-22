from django.contrib import admin

# Register your models here.
from .models import Productos,Ingresos,DetalleIngreso,Rubros

class ProductosAdmin(admin.ModelAdmin):
    list_display=['codigo','nombre','rubro','activo']

admin.site.register(Productos,ProductosAdmin)
admin.site.register(Rubros)
admin.site.register(Ingresos)
admin.site.register(DetalleIngreso)