from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Productos , DetalleIngreso , Ingresos , Rubros
from .serializers import DetallesIngresosSerializers,NuevosIngresosSerializers,IngresosSerializer,ABMProductosSerializer,RubrosSerializer,ProductosSerializer2
from applications.cuentas.models import Cuentas
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt
from .functions import actualizar_stock



class ABMProducto(APIView):
    serializer_class = ABMProductosSerializer

    def put(self, request, codigo):
        
        producto = Productos.objects.get(codigo=codigo)
        serializer = self.serializer_class(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,codigo):

        producto = Productos.objects.get(codigo=codigo)
        producto.activo=False
        producto.save()

        return Response(status=status.HTTP_200_OK)




#######################

class RubrosViewSet(viewsets.ModelViewSet):

    serializer_class = RubrosSerializer
    queryset =Rubros.objects.all()


class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.filter(activo=True)
    serializer_class = ProductosSerializer2

    



    
#########################



class DetallesByIngreso(ListAPIView):
    serializer_class=DetallesIngresosSerializers

    def get_queryset(self):
        ingreso=self.request.query_params.get('cliente',None)
        detalles=DetalleIngreso.objects.all()

        if ingreso is None:
            detalles=detalles
        else:
            detalles=detalles.filter(ingreso__id=ingreso.id)

        datos=DetallesIngresosSerializers(detalles,many=True)
        return datos.data

#############################

class ReporteIngresos(ListAPIView):
    serializer_class=IngresosSerializer

    def get_queryset(self):

        ingresos=Ingresos.objects.all()
    
        
        #serializer = ReporteCuentas(queryset, many=True)
        return ingresos

class NuevosIngresos(APIView):
    serializers_class=NuevosIngresosSerializers
    
    def get(self,request):
        ingresos=Ingresos.objects.all()
        queryset=IngresosSerializer(ingresos,many=True)
        return Response(queryset.data)

    def post(self,request):
        serializer = self.serializers_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos=serializer.validated_data
        prods=datos['productos']
        cantidades=datos['cantidades']
        subtotales=datos['subtotales']
        observacion=datos['observacion']
        total=datos['total']
        fecha=dt.date.today()

        ings=Ingresos.objects.all()
        if ings.count() == 0:
            num=1
        else:
            num=ings.last().id + 1

        nuevo_ingreso=Ingresos(
            numero=num,
            fecha=fecha,
            observacion=observacion,
            total=total,
        )
        
        
        productos=[Productos.objects.get(codigo=p) for p in prods]

        dets=DetalleIngreso.objects.all()

        if dets.count() == 0:
            numero=0
            

        else:
            last_det=DetalleIngreso.objects.all().last()
            numero=last_det.id
 
        detalles_ingresos=[DetalleIngreso(
                    numero=numero + 1,
                    ingreso=nuevo_ingreso,
                    producto=p,
                    cantidad=c,
                    subtotal=s)  
                for p,c,s in zip(productos,cantidades,subtotales)]

        nuevo_ingreso.save()

        print(detalles_ingresos)
        DetalleIngreso.objects.bulk_create(detalles_ingresos)


        #Actualizar stock
        actualizar_stock(productos,cantidades,'ingresos')


        return Response({'status':200})

@receiver(post_save, sender=Cuentas)
def gestion_stock(sender, **kwargs):
    pass
    #instancia.pro
    #print(instance)

