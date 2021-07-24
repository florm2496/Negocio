from django.shortcuts import render
from rest_framework import viewsets
from .models import Cuentas
from .serializers import cuentasSerializer
# Create your views here.

class cuentasViewSet(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = cuentasSerializer

