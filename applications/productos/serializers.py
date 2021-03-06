
from rest_framework import serializers
from .models import DetalleIngreso, Ingresos, Productos, Rubros
from applications.cuentas.models import DetalleCuenta
from django.db.models import Sum




class ABMProductosSerializer(serializers.ModelSerializer):

    class Meta:
        model=Productos
        fields=('__all__')

class RubrosSerializer(serializers.ModelSerializer):

    class Meta:
        model=Rubros
        fields=('__all__')


#LO USO PARA EL MODAL
class ProductosSerializer(serializers.ModelSerializer):
        class Meta:
            model=Productos
            fields=('__all__')
    


#ESTE SE USA PARA LA TABLA GENERAL
class ProductosSerializer2(serializers.ModelSerializer):
    #cant_vendida = serializers.SerializerMethodField()
    rubro = serializers.SerializerMethodField()
    class Meta:
        model=Productos
        fields=('nombre','codigo','codigo_ref','rubro','precio','stock')

    # def get_cant_vendida(self,obj):
    #     cant=DetalleCuenta.objects.filter(producto=obj).aggregate(cant=Sum('cantidad'))['cant']
    #     if cant is None:
    #         cant=0
    #     return cant

    def get_rubro(self,obj):
        rubro=Rubros.objects.get(pk=obj.rubro.id)

        return RubrosSerializer(rubro).data



class CantidadesSerializer(serializers.ListField):
    child = serializers.IntegerField()

class ProductosSerializer(serializers.ListField):
    child = serializers.IntegerField()

class SubtotalesSerializer(serializers.ListField):
    child = serializers.FloatField()




class DetallesIngresosSerializers(serializers.Serializer):
    
    class Meta:
        model=DetalleIngreso
        fields=('producto','cantidad','subtotal')

class NuevosIngresosSerializers(serializers.Serializer):
    observacion=serializers.CharField(required=True)
    total=serializers.FloatField(required=True)
    cantidades=CantidadesSerializer(required=True)
    productos=ProductosSerializer(required=True)
    subtotales=SubtotalesSerializer(required=True)


class IngresosSerializer(serializers.ModelSerializer):
    detalles=serializers.SerializerMethodField()
    cant_prods=serializers.SerializerMethodField()

    class Meta:
        model=Ingresos
        fields=('numero','fecha','total','observacion','detalles','cant_prods')


    def get_detalles(self,obj):
        lista=DetalleIngreso.objects.filter(ingreso__id=obj.id)
        serializer=DetallesIngresosSerializers(lista,many=True)
        return serializer.data

    def get_cant_prods(self,obj):
        cant_ing=DetalleIngreso.objects.filter(ingreso__pk=obj.pk)
        
        cants=[det.cantidad for det in cant_ing]

        return sum(cants)






