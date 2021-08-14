from django.shortcuts import render
from rest_framework import viewsets
from .models import Cuentas
from .serializers import cuentasSerializer
from rest_framework import viewsets , permissions
# Create your views here.

class cuentasViewSet(viewsets.ModelViewSet):
    permission_classes=(permissions.IsAuthenticated,)
    queryset = Cuentas.objects.all()
    serializer_class = cuentasSerializer

