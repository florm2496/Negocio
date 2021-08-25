from django.contrib import admin

# Register your models here.
from .models import Cuentas
from .models import Cuotas

admin.site.register(Cuentas)
admin.site.register(Cuotas)