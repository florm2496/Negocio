from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Productos
from .serializers import productosSerializer
from applications.cuentas.models import Cuentas
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
# Create your views here.

class Productos(viewsets.ModelViewSet):
    #permission_classes=(IsAuthenticated,)
    queryset = Productos.objects.all()
    serializer_class = productosSerializer




@receiver(post_save, sender=Cuentas)
def gestion_stock(sender, **kwargs):
    pass
    #instancia.pro
    #print(instance)

