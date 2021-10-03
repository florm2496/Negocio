import datetime as dt
import pytz
utc=pytz.UTC
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Cuentas, Cuotas, DetalleCuenta,Pagos
from applications.clientes.models import Clientes
from .serializers import (NuevaCuentaSerializer, PagosSerializer, cuentasSerializer,ReporteCuentas,
                        ListaCuotasSerializer,CuotasCuentaSerializer,NuevoPagoSerializer)

from rest_framework import viewsets
import datetime as dt
from applications.cuentas import serializers 
from django.db.models import Max
from applications.productos.models import Productos
from django.utils import timezone
from .functions import generar_fechas , get_cuentas , update_dues,actualizarstock
from rest_framework import status
# Create your views here.



class NuevoPago(APIView):
    serializer_class = NuevoPagoSerializer

    def post(self,request):
        serializer = NuevoPagoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos=serializer.validated_data
        cuenta=Cuentas.objects.get(numero_cuenta=datos['numero_cuenta'],pk=datos['id_cuenta'])
        cuota=Cuotas.objects.get(numero_cuota=datos['numero_cuota'],pk=datos['id_cuota'])

        monto_pago=datos['monto']
        metodo_pago=datos['metodo']
        fecha=dt.datetime.now()
        
        nuevo_pago=Pagos(
            cuota=cuota,
            importe=monto_pago,
            metodo_pago=metodo_pago,
            fecha=fecha,

        )
        nuevo_pago.save()


        


        pago_serializado=PagosSerializer(nuevo_pago)
        return Response({'response':'ok','status':200,'pago':pago_serializado.data})





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
        queryset = Cuentas.objects.filter(solicitante__dni=int(cliente))
        serializer = cuentasSerializer(queryset, many=True)
        return Response(serializer.data)


#class CuotasView(viewsets.ModelViewSet):
class CuotasView(ListAPIView):
    serializer_class = ListaCuotasSerializer
    queryset=Cuotas.objects.all()

    def get(self, request):
        cuenta=request.query_params.get('cuenta',None)
        queryset = Cuotas.objects.filter(cuenta__numero_cuenta=int(cuenta))
        serializer = ListaCuotasSerializer(queryset, many=True)
        return Response(serializer.data)

# class CuotasCuenta(serializers.ListAPIView):
#     serializer_class = CuotasCuenta

#     def get(self, request):
#         cuenta=request.query_params.get('cuenta',None)
#         queryset = Cuotas.objects.filter(cuenta__numero_cuenta=int(cuenta))
#         serializer = ListaCuotasSerializer(queryset, many=True)
#         return Response(serializer.data)




class CuotasCuentaViews(ListAPIView):
    serializer_class = CuotasCuentaSerializer
    
    def get(self, request):
        cuenta=request.query_params.get('num_cuenta',None)
        cuentas=Cuentas.objects.all()
        queryset = get_cuentas(cuentas,cuenta)
        serializer = CuotasCuentaSerializer(queryset)
        return Response(serializer.data)


class RegistrarCuenta(CreateAPIView):
    serializer_class=NuevaCuentaSerializer
    

    def create(self,request):
        #validar y obtene los datos del serializador
        serializer = NuevaCuentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos=serializer.validated_data
        #extraer datos para la cuenta
        solicitante_dni=datos['solicitante']
        importe_cuenta=datos['importe']
        importe_cuota=datos['importe_cuota']
        garante_dni=datos['garante']
        cant_cuotas=datos['cant_cuotas']
        num_cuenta=datos['num_cuenta']
        fecha_venc=datos['dia_venc']
        metodo_pago=datos['metodo_pago']
        #extraer datos para los detalles de cuenta
        prods=datos['productos']
        cants=datos['cantidades']
        subts=datos['subtotales']
        descs=datos['descuentos']

        #crear cuenta
        solicitante=Clientes.objects.get(dni=int(solicitante_dni))
        garante=Clientes.objects.get(dni=int(garante_dni))

        cuenta=Cuentas(
            solicitante=solicitante,
            garante= garante,
            importe= importe_cuenta,
            fecha= timezone.now(),
            numero_cuenta= num_cuenta,
            metodo_pago=metodo_pago,
        )

        
        #obtener los objetos de los productos de los detalles de cuentas
        productos=Productos.objects.filter(
            codigo__in=prods
        )
        #crear los objetos detalles de cuentas
        detalles=[DetalleCuenta(
                    cuenta=cuenta,
                    producto=p,
                    cantidad=c,
                    subtotal=s,
                    descuento=d,) for p,c,s,d in zip(productos,cants,subts,descs)]
            

        fechas_venc=generar_fechas(fecha_venc,cant_cuotas)

        #crear las cuotas
        cuotas=range(1,cant_cuotas+1)
        fechas=range(cant_cuotas)

        lista_cuotas=[Cuotas(cuenta=cuenta,
                         numero_cuota= c,
                         importe=importe_cuota,
                         saldo=importe_cuota,
                         fecha_vencimiento=fechas_venc[f],
                         recargo=0,
                         descuento=0
                         ) for c,f in zip(cuotas,fechas)]
        #crear cuenta
        cuenta.save()
        #crear los detalles 
        DetalleCuenta.objects.bulk_create(detalles)

        actualizarstock(productos,cants)
        #crear cuotas
        Cuotas.objects.bulk_create(lista_cuotas)
        
        return Response({'mensaje':'cuenta creada'})


class ReporteVentas(ListAPIView):
    serializer_class=ReporteCuentas

    def get_queryset(self):
        cliente=self.request.query_params.get('cliente',None)
        cuentas=Cuentas.objects.all()
        if cliente is None:
            queryset=cuentas
        else:
            queryset = cuentas.filter(solicitante__dni=int(cliente))
        
        #serializer = ReporteCuentas(queryset, many=True)
        return queryset

class NuevaCuenta(APIView):
    serializer_class=NuevaCuentaSerializer
    #permission_classes=(permissions.IsAuthenticated,)
    # authenticaction_classes=(TokenAuthentication,)
    # permission_classes=[IsAuthenticated]
 
    def post(self,request):
        
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        solicitante_dni=serializer.data.get('solicitante')
        importe_cuota=serializer.data.get('importe')
        garante_dni=serializer.data.get('garante')
        cuotas=serializer.data.get('cant_cuotas')
        num_cuenta=serializer.data.get('num_cuenta')
    
        ff=serializer.data.get('dia_venc').replace('-','/')
        ff_aux=dt.datetime.strptime(ff,'%Y/%m/%d')
        dia_venc=ff_aux.date()

        importe_cuota=serializer.data.get('importe_cuota')
        solicitante=Clientes.objects.get(dni=int(solicitante_dni))
        garante=Clientes.objects.get(dni=int(garante_dni))

        cuenta=Cuentas(
            solicitante=solicitante,
            garante= garante,
            importe= serializer.data.get('importe'),
            fecha= dt.datetime.now(),
            numero_cuenta= num_cuenta,

            #saldo = serializer.data.get('saldo'),
            #productos = serializer.data.get('productos'),
        )
        cuenta.save()
        
        lista_cuotas=[]
        
        fechas_venc=generar_fechas(dia_venc,cuotas)
        i=1

        for c in range(cuotas):
                          
            cuota=Cuotas(cuenta=cuenta,
                         numero_cuota=i,
                         importe=importe_cuota,
                         saldo=0,
                         fecha_vencimiento=fechas_venc[c],
                         recargo=0,
                         descuento=0
                         )
            lista_cuotas.append(cuota)
            i+=1
        
        Cuotas.objects.bulk_create(lista_cuotas)
          
         
        return Response(
            {
                'estado':'200',
            }
        )

class get_num_cuenta(APIView):

    def get(self,request):

        cuenta=Cuentas.objects.aggregate(max_num=Max('numero_cuenta'))
        cuenta=cuenta['max_num']

        if cuenta is None:
        
            num_cuenta=0
        else:
            num_cuenta=int(cuenta)+1
        return Response({'num_cuenta':num_cuenta})



class NuevoDetalleCuenta(APIView):
    #queryset=DetalleCuenta.objects.all()
    

    def post(self,request):
        detalles = [DetalleCuenta(cantidad=4,precio=6,producto=66),
                    DetalleCuenta(cantidad=4,precio=6,producto=66),
                    DetalleCuenta(cantidad=4,precio=6,producto=66),]
        serializer_class=serializers.DetalleCuentaSerializer(detalles,many=True)
        serializer=serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)

        return Response({'datos':'datos'})