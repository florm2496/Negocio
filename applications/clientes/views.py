from django.shortcuts import render
from rest_framework import viewsets , permissions
from rest_framework.response import Response

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
from .models import Clientes
from .serializers import clientesSerializer
# Create your views here.

class clientesViewSet(viewsets.ModelViewSet):
    #permission_classes=(permissions.IsAuthenticated,)
    queryset = Clientes.objects.all().order_by('apellido')
    serializer_class = clientesSerializer
    
  

    def get_queryset(self):
        
        dni=self.request.query_params.get('dni',None)
        tipo=self.request.query_params.get('tipo',None)
       
        clientes=Clientes.objects.all()
        if dni is None:
            objs=clientes
        else:
            objs=clientes.filter(dni__icontains=dni)
            
            if tipo is not None:
                print(objs)
                if tipo=='garante':
                    objs=objs.filter(garante=True)
                    
                else:
                    objs=objs.filter(solicitante=True)
                     
        return objs


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
        

