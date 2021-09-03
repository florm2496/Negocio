from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Cuentas, Cuotas
from applications.clientes.models import Clientes
from .serializers import NuevaCuentaSerializer, cuentasSerializer
from rest_framework.decorators import  api_view,action
from rest_framework import viewsets , permissions
import datetime as dt
from .functions import generarfechas
from applications.cuentas import serializers 

# Create your views here.

class cuentasViewSet(viewsets.ModelViewSet):
    #permission_classes=(permissions.IsAuthenticated,)
    queryset = Cuentas.objects.all()
    serializer_class = cuentasSerializer

    # @action(detail=True, methods=['get'])
    # def cuentas_cliente(self,request,pk=None):
    #     datos=Cuentas.objects.all()
    #     serializer=self.get_serializer(datos,many=True)
    #     return Response(serializer.data)

class CuentasByCliente(ListAPIView):
    
    serializer_class = cuentasSerializer
    queryset=Cuentas.objects.all()
    #permission_classes = [IsAdminUser]

    def get(self, request):
        cliente=request.query_params.get('cliente')
        queryset = Cuentas.objects.filter(cliente__dni=int(cliente))
        serializer = cuentasSerializer(queryset, many=True)
        return Response(serializer.data)

class NuevaCuenta(APIView):
    serializer_class=NuevaCuentaSerializer
    #permission_classes=(permissions.IsAuthenticated,)
    # authenticaction_classes=(TokenAuthentication,)
    # permission_classes=[IsAuthenticated]
 
    def post(self,request):
        
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dni=serializer.data.get('dni')
        importe=serializer.data.get('importe')
        cuotas=serializer.data.get('cant_cuotas')
        fi=serializer.data.get('dia_inicio').replace('-','/')
        fi_aux=dt.datetime.strptime(fi,'%Y/%m/%d')
        dia_inicio=fi_aux.date()
        ff=serializer.data.get('dia_venc').replace('-','/')
        ff_aux=dt.datetime.strptime(ff,'%Y/%m/%d')
        
        dia_venc=ff_aux.date()
        importe_cuota=serializer.data.get('importe_cuota')
        cliente=Clientes.objects.get(dni=int(dni))
        
        cuenta=Cuentas(
            cliente=cliente,
            garante= serializer.data.get('garante'),
            importe= serializer.data.get('importe'),
            fecha= dt.datetime.now(),
            numero_cuenta= serializer.data.get('numero_cuenta'),
            #saldo = serializer.data.get('saldo'),
            #productos = serializer.data.get('productos'),
        )
        cuenta.save()
        
        lista_cuotas=[]
        
        fechas_inicio,fechas_venc=generarfechas(dia_inicio,dia_venc,cuotas)
        i=1

        for c in range(cuotas):
                          
            cuota=Cuotas(cuenta=cuenta,
                         numero_cuota=i,
                         importe=importe_cuota,
                         saldo=0,
                         fecha_inicio=fechas_inicio[c],
                         fecha_vencimiento=fechas_venc[c],
                         recargo=0,
                         descuento=0
                         )
            lista_cuotas.append(cuota)
            i=i+1
        
        Cuotas.objects.bulk_create(lista_cuotas)
          
        print('final del proceso')    
        return Response(
            {
                'enabled':'hola',
            }
        )
        