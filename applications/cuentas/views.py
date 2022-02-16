import datetime as dt
import pytz
utc=pytz.UTC
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Cuentas, Cuotas, DetalleCuenta,Pagos
from applications.clientes.models import Clientes
from .serializers import (NuevaCuentaSerializer, PagosSerializer, cuentasSerializer,detalleCuentaClienteSerializer,
                        ListaCuotasSerializer,CuotasCuentaSerializer,NuevoPagoSerializer,DetallesCuentaSerializer,refinanciarCuentaSerializer)

from rest_framework import viewsets
import datetime as dt
from applications.cuentas import serializers 
from django.db.models import Max
from applications.productos.models import Productos
from django.utils import timezone
from .functions import generar_fechas , get_cuentas , update_dues,actualizar_estado_cuotas
from applications.productos.functions import actualizar_stock
from rest_framework import status
from django.db.models import Q
# Create your views here.




class RefinanciarCuenta(APIView):
    serializer_class=refinanciarCuentaSerializer

    def post(self,request):
        
        #datos serializados
        ds=self.serializer_class(request.data)

        num_cuenta=ds.data.get('cuenta')
        cuenta=Cuentas.objects.get(numero_cuenta=num_cuenta)
        saldo=cuenta.saldo

        cant_cuotas=ds.data.get('cant_cuotas')
        importe_cuota=saldo/cant_cuotas

        fc=ds.data.get('fecha_venc')
        fecha_venc=dt.datetime.strptime(fc,'%Y-%m-%d')

 
        fechas_venc=generar_fechas(fecha_venc,cant_cuotas)
        
        ultima_cuota=Cuotas.objects.all().last()
        i=ultima_cuota.numero_cuota
        
        lista_cuotas=[]
        Cuotas.objects.filter(Q(cuenta__pk=cuenta.id) and ~Q(saldo=0)).update(refinanciada=True)
        
        for c in range(cant_cuotas):
            i+=1          
            cuota=Cuotas(cuenta=cuenta,
                         numero_cuota=i,
                         importe=importe_cuota,
                         saldo=importe_cuota,
                         fecha_vencimiento=fechas_venc[c],
                         recargo=0,
                         descuento=0,
                         refinanciada=False,
                         )
            lista_cuotas.append(cuota)
            
        Cuotas.objects.bulk_create(lista_cuotas)

        
        cuenta.estado='refinanciada'
        cuenta.save()


        return Response({'status':200})

class NuevoPago(APIView):
    serializer_class = NuevoPagoSerializer

    def post(self,request):
        serializer = NuevoPagoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos=serializer.validated_data
        num_cuota=datos['numero_cuota']
        id_cuota=datos['id_cuota']
        cuenta=Cuentas.objects.get(numero_cuenta=datos['numero_cuenta'],pk=datos['id_cuenta'])
        cuota=Cuotas.objects.get(numero_cuota=num_cuota,pk=id_cuota,cuenta__id=cuenta.pk)

        monto_pago=datos['monto']
        metodo_pago=datos['metodo']
        excedente=datos['excedente']

        if excedente == 0:
            #se crea el nuevo pago , nunca sera menor a 0 por validaciones del front
            nuevo_pago=Pagos(
                cuota=cuota,
                importe=monto_pago,
                metodo_pago=metodo_pago,
                fecha=dt.datetime.now(),

            )
            nuevo_pago.save()
        
            #se descuenta del saldo de la cuota lo pagado


            nuevo_saldo=cuota.saldo - monto_pago
            cuota.saldo=nuevo_saldo
            if nuevo_saldo <=0:
                cuota.estado='pagada'
            
            cuota.save()
        
            #luego se verifica si el excedente es mayor a 0 , si hay excedente se descontara de la siguiente cuota
        else:
            pago_total=excedente + monto_pago
            while pago_total>0:
                
                cuota=Cuotas.objects.filter(numero_cuota=num_cuota,cuenta__id=cuenta.pk)
                
                if cuota.count() > 0:
                    cuota=cuota[0]
                    if pago_total > cuota.saldo:
     
                        cobrar=cuota.saldo

                        cuota.saldo=0
                        cuota.estado='pagada'
                        cuota.save()

                        
                    elif pago_total < cuota.saldo:
                        cobrar=pago_total
                        
                        cuota.saldo= cuota.saldo - cobrar   

                        print('el pago es menor a la cuotota',cuota.saldo)
                        cuota.save()

                    pago_ste_cuota=Pagos(
                    cuota=cuota,
                    importe=cobrar,
                    metodo_pago=metodo_pago,
                    fecha=dt.datetime.now(),

                    )
                    pago_ste_cuota.save()

                    num_cuota += 1

                    pago_total= pago_total-cobrar
                else:
                    break

                
                
        #pago_serializado=PagosSerializer(nuevo_pago)
        return Response({'response':'ok','status':200})





class cuentasViewSet(viewsets.ModelViewSet):
    #permission_classes=(permissions.IsAuthenticated,)
    queryset = Cuentas.objects.all()
    serializer_class = cuentasSerializer

    def get_queryset(self):

        cuentas=super().get_queryset()

        
        actualizar_estado_cuotas(cuentas)

        
        return super().get_queryset()
    

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
        garante_dni1=datos['garante1']
        garante_dni2=datos.get('garante2',None)
        cant_cuotas=datos['cant_cuotas']
        num_cuenta=datos['num_cuenta']
        fecha_venc=datos['dia_venc']
        metodo_pago=datos['metodo_pago']
        #extraer datos para los detalles de cuenta
        prods=datos['productos']
        cants=datos['cantidades']
        subts=datos['subtotales']
        descs=datos['descuentos']
        anticipo=datos['anticipo']
        descuento=datos['descuento']

        #crear cuenta
        solicitante=Clientes.objects.get(dni=int(solicitante_dni))
        garante1=Clientes.objects.get(dni=int(garante_dni1))
        
        if garante_dni2 is None:
            garante2=None
        else:
            garante2=Clientes.objects.get(dni=int(garante_dni2))

        cuenta=Cuentas(
            solicitante=solicitante,
            garante1= garante1,
            garante2=garante2,
            importe= importe_cuenta,
            anticipo=anticipo,
            descuento=descuento,
            fecha= timezone.now(),
            numero_cuenta= num_cuenta,
            metodo_pago=metodo_pago,
            saldo=importe_cuenta,
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

        actualizar_stock(productos,cants,'ventas')
        #crear cuotas
        Cuotas.objects.bulk_create(lista_cuotas)
        
        return Response({'mensaje':'cuenta creada'})


class ReporteVentas(ListAPIView):
    serializer_class=detalleCuentaClienteSerializer

    def get_queryset(self):
        cliente=self.request.query_params.get('cliente',None)
        cuenta=self.request.query_params.get('numero_cuenta')
        cuentas=Cuentas.objects.all()
        
        print(cliente,cuenta)
        if cliente is None:
            queryset=cuentas
        else:
            queryset = cuentas.filter(solicitante__dni=cliente)
            
        if cuenta is not None:
            queryset=queryset.filter(numero_cuenta=cuenta)
        
        #serializer = ReporteCuentas(queryset, many=True)
        print(queryset)
        return queryset


class detalleCuentaCliente(APIView):
    serializer_class=detalleCuentaClienteSerializer

    def get(self,request):

        dni_cliente=self.request.query_params.get('cliente')
        numero_cuenta=self.request.query_params.get('numero_cuenta',None)

        cuentas_cliente=Cuentas.objects.filter(solicitante__dni=dni_cliente)


        if numero_cuenta is not None:

            cuentas=cuentas_cliente.filter(numero_cuenta=numero_cuenta)


        cuenta_serializada = self.serializer_class(cuentas,many=True)

        return Response(cuenta_serializada.data)



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
        
            num_cuenta=00310001
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
    
        return Response({'datos':'datos'})
    
    
    
class DetallesCuenta(ListAPIView):
    serializer_class=DetallesCuentaSerializer

    def get_queryset(self):
        cliente=self.request.query_params.get('dni_solicitante')
        cuenta=self.request.query_params.get('numero_cuenta')
      
        detalles=DetalleCuenta.objects.filter(cuenta__numero_cuenta=cuenta,cuenta__solicitante__dni=cliente)
        
        #serializer = ReporteCuentas(queryset, many=True)
        return detalles