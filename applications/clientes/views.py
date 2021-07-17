from django.shortcuts import render
from rest_framework import viewsets
from .models import Clientes
from .serializers import clientesSerializer
# Create your views here.

class clientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = clientesSerializer

