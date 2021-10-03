from rest_framework import serializers
from .models import DetalleIngreso, Ingresos, Productos
from applications.cuentas.models import DetalleCuenta
from django.db.models import Sum, fields


class productosSerializer(serializers.ModelSerializer):
    cant_vendida = serializers.SerializerMethodField()
    class Meta:
        model=Productos
        fields=('nombre','codigo','codigo_ref','tipo','estado','precio','stock','cant_vendida')

    def get_cant_vendida(self,obj):
        cant=DetalleCuenta.objects.filter(producto=obj).aggregate(cant=Sum('cantidad'))
        return cant['cant']


class IngresosSerializer(serializers.ModelSerializer):
    detalles=serializers.SerializerMethodField()

    class Meta:
        model=Ingresos
        fields=('fecha','total','detalles')


    def get_detalles(self,obj):
        detalles=DetalleIngreso.objects.filter(ingreso=obj)
        return detalles



