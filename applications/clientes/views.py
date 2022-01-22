from django.shortcuts import render
from rest_framework import viewsets , permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from django.db.models import Q

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
from .models import Clientes
from .serializers import clientesSerializer,bajaSerializer
# Create your views here.

class clientesViewSet(viewsets.ModelViewSet):
    #permission_classes=(permissions.IsAuthenticated,)
    queryset = Clientes.objects.all().order_by('apellido')
    serializer_class = clientesSerializer


    def get_queryset(self):
        queryset = super(clientesViewSet, self).get_queryset()
        return queryset.filter(activo=True)

  

class getClientesCuenta(APIView):
    #permission_classes=(permissions.IsAuthenticated,)

    serializer_class = clientesSerializer

    def get(self,request):

        busqueda=self.request.query_params.get('busqueda')

        
        clientes=Clientes.objects.all()

        if busqueda.isnumeric():
            
            coincidencias=clientes.filter(dni__icontains=busqueda)
        else:

            nombre=busqueda.split(' ')

            if len(nombre) == 2:
                n=nombre[0]
                a=nombre[1]
                coincidencias=clientes.filter(Q(nombre__icontains=n) & Q(apellido__icontains=a))

            else:
                a=nombre[0]
                coincidencias=clientes.filter(Q(apellido__icontains=a))

        serializer=self.serializer_class(coincidencias,many=True)
        return Response(serializer.data)
    



class bajaCliente(APIView):

    serializer_class=bajaSerializer


    def post(self,request):

        print(request.data)
        
        s=self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        datos=s.validated_data
        id=datos['id']
        dni=datos['dni']

        cliente=Clientes.objects.get(id=id , dni=dni)
        cliente.activo=False
        cliente.save()

        return Response({'status':200})

# class clienteAPIVIEW(APIView):

#     def get_object(self, pk):
#         try:
#             return Clientes.objects.get(pk=pk)
#         except Clientes.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         Clientes = self.get_object(pk)
#         serializer = clientesSerializer(Clientes)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         Clientes = self.get_object(pk)
#         serializer = clientesSerializer(Clientes, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         Clientes = self.get_object(pk)
#         Clientes.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

   


    # def update(self,request,pk=None):
    #     print('en pudate')
        # @action(methods=['get'],detail=False,
    #         url_path='bydni/')

    # def by_name(self,request,pk=None,dni=None):
    #     print(dni)
    #     obj=Clientes.objects.filter(nombre__icontains=dni)
        

    #     if not obj:
    #         response={'detail':'No se encontro cliente'}
           
    #     else:
    #         response=clientesSerializer(obj,many=True).data
    #     return Response(response)
        