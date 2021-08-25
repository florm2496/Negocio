from rest_framework import serializers
from .models import Cuentas, Cuotas, Pagos


class cuentasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cuentas
        fields='__all__'

class NuevaCuentaSerializer(serializers.Serializer):
    id_cliente=serializers.CharField(required=True)
    garante=serializers.CharField(required=True)
    importe=serializers.FloatField(required=True)
    numero_cuenta=serializers.FloatField(required=True)
    cant_cuotas=serializers.IntegerField(required=True)
    saldo=serializers.FloatField(required=True)
    productos=serializers.CharField(required=True)
    dia_inicio= serializers.IntegerField(required=True)
    dia_venc= serializers.IntegerField(required=True)
    importe_cuota = serializers.FloatField(required=True)

    """
    cliente= models.ForeignKey(Clientes, on_delete=models.CASCADE)
    garante= models.CharField(max_length=50, verbose_name="Garante")
    importe= models.FloatField(verbose_name="Importe")
    fecha= models.DateTimeField(verbose_name="Fecha", auto_now=False, auto_now_add=False)
    numero_cuenta= models.CharField(max_length=30,verbose_name="Numero de cuenta")
    saldo = models.FloatField(verbose_name="Saldo")
    productos = models.CharField(max_length=200, verbose_name="Productos")
    estado = models.CharField(verbose_name='Estado',max_length=20)
    """
   

class pagosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pagos
        fields='__all__'
