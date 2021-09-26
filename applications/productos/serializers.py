from rest_framework import serializers
from .models import Productos
from applications.cuentas.models import DetalleCuenta
from django.db.models import Sum


class productosSerializer(serializers.ModelSerializer):
    cant_vendida = serializers.SerializerMethodField()
    class Meta:
        model=Productos
        fields=('nombre','codigo','codigo_ref','tipo','estado','precio','stock','cant_vendida')

    def get_cant_vendida(self,obj):
        cant=DetalleCuenta.objects.filter(producto=obj).aggregate(cant=Sum('cantidad'))
        return cant['cant']




