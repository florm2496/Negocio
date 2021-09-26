from django.db import models
from applications.clientes.models import Clientes
from applications.productos.models import Productos

# Create your models here.

metodos=[
    ('contado','contado'),
    ('tarjeta','tarjeta'),
]
estado=[
    ('activa','activa'),
    ('morosa','morosa'),
    ('inactiva','inactiva'),
    ('saldada','saldada'),
]
class Cuentas(models.Model):
    solicitante= models.ForeignKey(Clientes, on_delete=models.CASCADE ,related_name='solicitante',default=None)
    garante = models.ForeignKey(Clientes, on_delete=models.CASCADE , related_name='garante')
    importe = models.FloatField(verbose_name="Total de la venta")
    fecha = models.DateField(verbose_name="Fecha y hora de la venta")
    numero_cuenta= models.CharField(max_length=30,verbose_name="Numero de cuenta")
    saldo = models.FloatField(verbose_name="Saldo",default=0)
    estado = models.CharField(verbose_name='Estado',max_length=20,choices=estado, default="activa")
    baja = models.BooleanField(default=False)  # este campo es para dar de baja la cuenta
    anticipo=models.FloatField(default=0)
    metodo_pago=models.CharField(choices=metodos,max_length=20,default="contado")
    
    def __str__(self):
        return '{}'.format(self.numero_cuenta)


class DetalleCuenta(models.Model):
    cuenta = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    subtotal = models.FloatField()
    descuento = models.FloatField(default=0)
    cantidad = models.IntegerField()

    def __str__(self):
        return str(self.subtotal) + str(self.cuenta.id)

estado_cuota=[
    ('impaga','impaga'),
    ('pagada','pagada'),
    ('morosa','morosa'),
] 
class Cuotas(models.Model):
    cuenta=models.ForeignKey(Cuentas,on_delete=models.CASCADE)
    numero_cuota=models.IntegerField(verbose_name="Numero de cuota",default=0)
    importe=models.FloatField(verbose_name="importe")
    saldo=models.FloatField(verbose_name="saldo")
    fecha_vencimiento=models.DateTimeField()
    estado = models.CharField(max_length=20,verbose_name='Estado de la cuota',choices=estado_cuota, default="impaga")
    vencida = models.BooleanField(default=False)
    recargo=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    
    class Meta:
        ordering= ('numero_cuota',)

    def __str__(self):
        return '{}'.format(self.numero_cuota)

    


class Pagos(models.Model):
    cuota = models.ForeignKey(Cuotas, on_delete=models.CASCADE)
    importe = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    metodo_pago=models.CharField(choices=metodos,max_length=20,default="contado")

    #def save(self, *args, **kwargs):

    def __str__(self):
        return str(self.cuota.id) + str(self.importe)
