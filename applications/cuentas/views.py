from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cuentas, Cuotas, Pagos
from applications.clientes.models import Clientes
from .serializers import NuevaCuentaSerializer, cuentasSerializer
from rest_framework.decorators import  api_view
from rest_framework import viewsets , permissions
import datetime as dt
from .functions import generarfechas 
# Create your views here.

class cuentasViewSet(viewsets.ModelViewSet):
    permission_classes=(permissions.IsAuthenticated,)
    queryset = Cuentas.objects.all()
    serializer_class = cuentasSerializer

class NuevaCuenta(APIView):
    serializer_class=NuevaCuentaSerializer
    #permission_classes=(permissions.IsAuthenticated,)
    # authenticaction_classes=(TokenAuthentication,)
    # permission_classes=[IsAuthenticated]
 
    def post(self,request):
        
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        id_cliente=serializer.data.get('id_cliente')
        importe=serializer.data.get('importe')
        cuotas=serializer.data.get('cant_cuotas')
        dia_inicio=serializer.data.get('dia_inicio')
        dia_venc=serializer.data.get('dia_venc')
        importe_cuota=serializer.data.get('importe_cuota')
        cliente=Clientes.objects.get(pk=int(id_cliente))
        
        cuenta=Cuentas(
            cliente=cliente,
            garante= serializer.data.get('garante'),
            importe= serializer.data.get('importe'),
            fecha= dt.datetime.now(),
            numero_cuenta= serializer.data.get('numero_cuenta'),
            saldo = serializer.data.get('saldo'),
            productos = serializer.data.get('productos'),
        )
        cuenta.save()
        
        lista_cuotas=[]
        print(dia_inicio, dia_venc)
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
          
            
        return Response(
            {
                'enabled':'hola',
            }
        )
        