from django.db import models
from applications.clientes.models import Clientes

# Create your models here.
class Cuentas(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    garante= models.CharField(max_length=50, verbose_name="Garante")
    importe= models.CharField(max_length=30,verbose_name="Importe")
    fecha= models.DateTimeField(verbose_name="Fecha", auto_now=False, auto_now_add=False)
    numero_cuenta= models.CharField(max_length=30,verbose_name="Numero de cuenta")
    saldo = models.FloatField(verbose_name="Saldo")
    productos = models.CharField(max_length=200, verbose_name="Productos")
    estado = models.BooleanField(verbose_name='Activo',default=True)
    
