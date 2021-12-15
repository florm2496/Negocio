from rest_framework import serializers

from applications.clientes.models import Clientes
from .models import Cuentas, DetalleCuenta,Cuotas, Pagos
from applications.clientes.serializers import clientesSerializer

from applications.productos.models import Productos
from applications.productos.serializers import ProductosSerializer2




class refinanciarCuentaSerializer(serializers.Serializer):
    cuenta=serializers.IntegerField(required=True)
    cant_cuotas=serializers.IntegerField(required=True)
    fecha_venc=serializers.DateField(required=True)


# class CuotasSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Cuotas
#         fields=('__all__')
class NuevoPagoSerializer(serializers.Serializer):
    numero_cuenta=serializers.CharField(required=True)
    id_cuenta=serializers.CharField(required=True)
    numero_cuota=serializers.IntegerField(required=True)
    id_cuota=serializers.IntegerField(required=True)
    monto=serializers.FloatField(required=True)
    metodo=serializers.CharField(required=True)
    excedente=serializers.FloatField(required=True)
    #fecha=serializers.DateField(required=True)

class PagosSerializer(serializers.ModelSerializer):

    class Meta:
        model=Pagos
        fields=('__all__')



class ListaCuotasSerializer(serializers.ModelSerializer):
    fecha_vencimiento = serializers.SerializerMethodField()
    vencida=serializers.SerializerMethodField()
    recargo=serializers.SerializerMethodField()
    pagos_cuotas=serializers.SerializerMethodField()
    pagada=serializers.SerializerMethodField()
    refinanciada=serializers.SerializerMethodField()


    class Meta:
        model=Cuotas
        fields=('id','saldo','importe','numero_cuota','fecha_vencimiento','vencida','estado','recargo','pagos_cuotas','pagada','refinanciada')
 

    def get_pagos_cuotas(self,obj):
        pagos_=Pagos.objects.filter(cuota=obj.id)
        pagos_serializados=PagosSerializer(pagos_,many=True)
        return pagos_serializados.data

    def get_fecha_vencimiento(self,obj):

        return obj.fecha_vencimiento.date()

    def get_vencida(self,obj):
        if obj.vencida:
            value= "SI"
        else:
            value = "NO"
        return value

    def get_refinanciada(self,obj):
        if obj.refinanciada:
            value= "SI"
        else:
            value = "NO"
        return value
    
    def get_recargo(self,obj):

        return round(obj.recargo)

    def get_pagada(self,obj):

        if obj.estado == 'pagada':
            estado=True
        else:
            estado=False
        return estado



class CuotasCuentaSerializer(serializers.ModelSerializer):
    cuotas=serializers.SerializerMethodField()
    saldo=serializers.SerializerMethodField()
    garante1=serializers.SerializerMethodField()
    garante2=serializers.SerializerMethodField()
    
    class Meta:
        model=Cuentas
        fields=('solicitante',
                'fecha',
                'garante1',
                'garante2',
                'importe',
                'numero_cuenta',
                'estado',
                'metodo_pago',
                'anticipo',
                'cuotas',
                'saldo',
                'importe',
                
              
    
        )
        

    def get_cuotas(self,obj):
        
        cuotas_=Cuotas.objects.filter(cuenta__numero_cuenta=obj.numero_cuenta)
        
        cuotas_serializadas=ListaCuotasSerializer(cuotas_ , many=True).data

        return cuotas_serializadas
    
    def get_saldo(self,obj):
    
        cuots=Cuotas.objects.filter(cuenta__numero_cuenta=obj.numero_cuenta)
        
        saldo=0
        
        saldos=[s.saldo for s in cuots]
        
        saldo=sum(saldos)
        return saldo

    def get_garante1(self,obj):
        return f'{obj.garante1.nombre} {obj.garante1.apellido}'

    def get_garante2(self,obj):
        try:
            nombre=f'{obj.garante2.nombre} {obj.garante2.apellido}'
        except:
            nombre=None
        
        return nombre
 
class cuentasSerializer(serializers.ModelSerializer):
    solicitante_nombre = serializers.SerializerMethodField()
    solicitante_dni = serializers.SerializerMethodField()
    garante1 = serializers.SerializerMethodField()
    garante2 = serializers.SerializerMethodField()
    class Meta:
        model=Cuentas
        fields=('id','importe','fecha','solicitante','solicitante_nombre','solicitante_dni','garante1','garante2','numero_cuenta','estado')

    def get_solicitante_nombre(self,obj):
        return obj.solicitante.nombre

    def get_solicitante_dni(self,obj):
        return obj.solicitante.dni

    def get_garante1(self,obj):
        return f'{obj.garante1.nombre} {obj.garante1.apellido}'

    def get_garante2(self,obj):
        try:
            nombre=f'{obj.garante2.nombre} {obj.garante2.apellido}'
        except:
            nombre=None
        
        return nombre

class CantidadesSerializer(serializers.ListField):
    child = serializers.IntegerField()

class ProductosSerializer(serializers.ListField):
    child = serializers.IntegerField()

class SubtotalesSerializer(serializers.ListField):
    child = serializers.FloatField()

class DescuentosSerializer(serializers.ListField):
    child = serializers.FloatField()


class NuevaCuentaSerializer(serializers.Serializer):
    solicitante=serializers.CharField(required=True)
    garante1=serializers.CharField(required=True)
    garante2=serializers.CharField(required=False)
    importe=serializers.FloatField(required=True)
    cant_cuotas=serializers.IntegerField(required=True)
    dia_venc= serializers.DateField(required=True)
    importe_cuota = serializers.FloatField(required=True)
    anticipo=serializers.FloatField(required=True)
    metodo_pago=serializers.CharField(required=True)
    num_cuenta=serializers.IntegerField(required=True)
    cantidades=CantidadesSerializer()
    productos=ProductosSerializer()
    descuentos=DescuentosSerializer()
    subtotales=SubtotalesSerializer()

class DetallesCuentaSerializer(serializers.ModelSerializer):
    producto=serializers.SerializerMethodField()
    class Meta:
        model=DetalleCuenta
        fields=('__all__')
        
    def get_producto(self,obj):
        producto=Productos.objects.get(pk=obj.producto.id)
        
        producto_serializado=ProductoSerializer(producto)
        
        return producto_serializado.data

class ReporteCuentas(serializers.ModelSerializer):
    detalles=serializers.SerializerMethodField()
    garante = serializers.SerializerMethodField()
    class Meta:
        model=Cuentas
        fields=('id',
                'solicitante',
                'fecha',
                'garante',
                'importe',
                'numero_cuenta',
                'estado',
                'metodo_pago',
                'anticipo',
                'detalles'
    
        )
    def get_garante(self,obj):

        return obj.garante.dni

    def get_detalles(self,obj):
        
        detalles=DetalleCuenta.objects.filter(cuenta__numero_cuenta=obj.numero_cuenta)
        
        detalles_serializados=DetallesCuentaSerializer(detalles , many=True).data

        return detalles_serializados
    






    
    


   