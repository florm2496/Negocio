from rest_framework import serializers
from .models import *


class domicilioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Domicilio
        fields='__all__'

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
        
        ultimo=Clientes.objects.all().last()
        
        if ultimo is None:
            num=0
        else:
            num=ultimo.numero_cliente
            
        calc=int(num) + 1
        cliente.numero_cliente=f'{calc}'
        
        cliente.save()
        
        return cliente
        
        
    
    def update(self,instance,validated_data):
        print('en UPDATE')
        # call model method for instance level computation
        datos_domicilio=validated_data.pop('domicilio')
        clientes=Clientes.objects.all()
        
        cliente_actual=clientes.filter(dni=validated_data.get('dni'))
        cliente_actual.update(**validated_data)
        
        cliente=cliente_actual.first()
        
        dom=cliente.domicilio.id
        
        Domicilio.objects.filter(pk=dom).update(**datos_domicilio)
        
        return cliente
        # cliente=Clientes.objects.update(**validated_data)
    
        # domicilio=Domicilio.objects.update(**datos_domicilio)
        # call super to now save modified instance along with the validated data
        #return super().update(instance, validated_data)  
        # datos_domicilio=validated_data.pop('domicilio')
        # cliente=Clientes.objects.create(**validated_data)
    
        # domicilio=Domicilio.objects.create(**datos_domicilio)
        

