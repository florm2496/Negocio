from django.shortcuts import render
from rest_framework import viewsets , permissions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
from .models import Clientes
from .serializers import clientesSerializer
# Create your views here.

class clientesViewSet(viewsets.ModelViewSet):
    permission_classes=(permissions.IsAuthenticated,)
    queryset = Clientes.objects.all().order_by('apellido')
    serializer_class = clientesSerializer

