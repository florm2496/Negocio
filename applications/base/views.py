from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count,Q
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ConfigsSerialzier
from .models import Configuraciones
from .functions import estado_clientes

from applications.cuentas.models import *
from applications.clientes.models import *

import json





class ConfiguracionesAPIView(APIView):

    serializer_class=ConfigsSerialzier

    def get(self,request):

        configs=Configuraciones.objects.all().first()

        data=ConfigsSerialzier(configs).data


        return Response(data)

    def post(self,request):

        datos=json.loads(request.body.decode('utf-8'))

        print(datos,type(datos))

        campo=datos['campo']
        dato=datos['dato']


        configs=Configuraciones.objects.all().first()

        if campo == 'recargo':
            configs.recargo_interes = dato
            configs.save()
            response=200
        
        elif campo == 'regalia':
            configs.dias_regalia = dato
            configs.save()
            response=200
        
        else:
            response=400


        return Response(response)




class Estadisticas(APIView):
    #serializer_class=

    def get(self,request):

        cuentas=Cuentas.objects.all()
        clientes=Clientes.objects.filter(activo=True)


        #cantidad total de ventas
        cuentas_totales=cuentas.aggregate(cantidad=Count('id'))

        #cantidad de clientes al dia (clientes solo tengan cuentas al dia ,es decir en estado activo o pagadas) y cantidad de clientes morosos
        

        clientes_aldia,clientes_morosos=estado_clientes(cuentas,clientes)

        #cuentas al dia (con los pagos hechos en tiempo y forma)

        cuentas_aldia=cuentas.filter(estado='activa').aggregate(cantidad=Count('id'))

        #cuentas pagadas totalmente
        cuentas_saldadas=cuentas.filter(estado='pagada').aggregate(cantidad=Count('id'))

        #cuentas con alguna de las cuotas retrasadas
        cuentas_morosas=cuentas.filter(estado='morosa').aggregate(cantidad=Count('id'))

        estadisticas={
            'numero_cuentas':cuentas_totales['cantidad'],
            'clientes_aldia': clientes_aldia,
            'clientes_morosos':clientes_morosos,
            'clientes_activos':clientes.aggregate(cantidad=Count('id'))['cantidad'],
            'cuentas_aldia':cuentas_aldia['cantidad'],
            'cuentas_morosas':cuentas_morosas['cantidad'],
            'cuentas_saldadas':cuentas_saldadas['cantidad'],

        }

        return Response(estadisticas)