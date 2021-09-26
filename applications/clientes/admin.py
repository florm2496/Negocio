from django.contrib import admin

# Register your models here.
from .models import Clientes




class ClienteAdmin(admin.ModelAdmin):
    list_display=('dni','nombre','apellido','id')


admin.site.register(Clientes,ClienteAdmin)