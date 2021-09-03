from rest_framework import serializers
from .models import Cuentas
from applications.clientes.serializers import clientesSerializer

class cuentasSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField()
    cliente_dni = serializers.SerializerMethodField()
    class Meta:
        model=Cuentas
        fields=('importe','fecha','cliente','cliente_nombre','cliente_dni','garante','numero_cuenta','estado')

    def get_cliente_nombre(self,obj):
        return obj.cliente.nombre

    def get_cliente_dni(self,obj):
        return obj.cliente.dni


class NuevaCuentaSerializer(serializers.Serializer):
    dni=serializers.CharField(required=True)
    garante=serializers.CharField(required=True)
    importe=serializers.FloatField(required=True)
    numero_cuenta=serializers.IntegerField(required=True)
    cant_cuotas=serializers.IntegerField(required=True)
    #saldo=serializers.FloatField(required=False)
    #productos=serializers.CharField(required=True)
    dia_inicio= serializers.DateField(required=True)
    dia_venc= serializers.DateField(required=True)
    importe_cuota = serializers.FloatField(required=True)
    #productos=serializers.Ma

