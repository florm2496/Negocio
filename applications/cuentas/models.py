from django.db import models
from applications.clientes.models import Clientes
from applications.productos.models import Productos

# Create your models here.


class Cuentas(models.Model):
    cliente= models.ForeignKey(Clientes, on_delete=models.CASCADE)
    garante= models.CharField(max_length=50, verbose_name="Garante")
    importe= models.FloatField(verbose_name="Importe")
    fecha= models.DateField(verbose_name="Fecha")
    numero_cuenta= models.CharField(max_length=30,verbose_name="Numero de cuenta")
    saldo = models.FloatField(verbose_name="Saldo",default=0)
    #productos = models.CharField(max_length=200, verbose_name="Productos")
    estado = models.CharField(verbose_name='Estado',max_length=20, default="activa")
    
    def __str__(self):
        return '{} {}'.format(self.id,self.cliente)


class DetalleCuenta():
    #cuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    subtotal = models.FloatField()
    cantidad = models.IntegerField()

    def __str__(self):
        return str(self.subtotal) + self.producto.nombre

    
class Cuotas(models.Model):
    cuenta=models.ForeignKey(Cuentas,on_delete=models.CASCADE)
    numero_cuota=models.IntegerField(verbose_name="Numero de cuota",default=0)
    importe=models.FloatField(verbose_name="importe")
    saldo=models.FloatField(verbose_name="importe")
    fecha_inicio=models.DateField()
    fecha_vencimiento=models.DateField()
    estado = models.CharField(max_length=20,verbose_name='Estado', default="impaga")
    recargo=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    productos = models.ManyToManyField(Productos,blank=True,null=True)
    
    def __str__(self):
        return 'Cuota {} , cuenta {}'.format(self.numero_cuota,self.cuenta)
