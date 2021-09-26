from django.contrib import admin

# Register your models here.
from .models import Productos

class ProductosAdmin(admin.ModelAdmin):
    list_display=['codigo','nombre','stock']

admin.site.register(Productos,ProductosAdmin)