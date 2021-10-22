from django.contrib import admin

# Register your models here.
from .models import Productos,Ingresos,DetalleIngreso

class ProductosAdmin(admin.ModelAdmin):
    list_display=['codigo','nombre','stock']

admin.site.register(Productos,ProductosAdmin)
admin.site.register(Ingresos)
admin.site.register(DetalleIngreso)