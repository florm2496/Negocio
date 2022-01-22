from django.contrib import admin

# Register your models here.
from .models import Clientes,Domicilio




class ClienteAdmin(admin.ModelAdmin):
    list_display=('dni','nombre','apellido','id','numero_cliente')


admin.site.register(Clientes,ClienteAdmin)
admin.site.register(Domicilio)