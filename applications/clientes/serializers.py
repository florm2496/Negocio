from rest_framework import serializers
from .models import *


class domicilioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Domicilio
        fields='__all__'


class bajaSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(required=True)
    dni = serializers.CharField(required=True)

class clientesSerializer(serializers.ModelSerializer):
    domicilio=domicilioSerializer()
    class Meta:
        model=Clientes
        fields='__all__'
    
    def create(self,validated_data):
        
        
        datos_domicilio=validated_data.pop('domicilio')
        cliente=Clientes.objects.create(**validated_data)
    
        domicilio=Domicilio.objects.create(**datos_domicilio)
        
        cliente.domicilio=domicilio

        clientes=Clientes.objects.all()

        num_cliente= clientes.count()
        cliente.numero_cliente=f'{num_cliente}'
        
        cliente.save()
        
        return cliente
        
        
    
    def update(self,instance,validated_data):
  
        datos_domicilio=validated_data.pop('domicilio')
        clientes=Clientes.objects.all()
        
        cliente_actual=clientes.filter(dni=validated_data.get('dni'))
        cliente_actual.update(**validated_data)
        
        cliente=cliente_actual.first()
        
        dom=cliente.domicilio.id
        
        Domicilio.objects.filter(pk=dom).update(**datos_domicilio)
        
        return cliente
    

