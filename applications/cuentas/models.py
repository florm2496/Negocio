from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    ('pagada','cancelada'),
    ('refinanciada','refinanciada')
]
class Cuentas(models.Model):
    solicitante=models.ForeignKey(Clientes,null=True,blank=True,on_delete=models.CASCADE ,related_name='cliente_solicitante')
    garante1=models.ForeignKey(Clientes,null=True,blank=True,on_delete=models.CASCADE,related_name='garante1')
    garante2=models.ForeignKey(Clientes,null=True,blank=True,on_delete=models.CASCADE,related_name='garante2')

    
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
        return str(self.cuota.id) + '-' + str(self.importe)




@receiver(post_save, sender=Pagos)
def actualizar_cuenta(instance, **kwargs):
    cuota_id=instance.cuota.id
    importe_pago=instance.importe
    cuenta_id=instance.cuota.cuenta.id
    cuenta=Cuentas.objects.get(pk=cuenta_id)

    cuota=Cuotas.objects.get(pk=cuota_id)
    cuota.saldo -=  importe_pago



    if cuota.saldo <= 0:
        cuota.estado = 'pagada'
    
    cuota.save()

    total_pagado = Pagos.objects.filter(cuota__cuenta__numero_cuenta=0).aggregate(suma=models.Sum('importe'))['suma']
    if total_pagado is None:
        total_pagado=0

    
    cuenta.saldo -= float(total_pagado)

    if cuenta.saldo <= 0:
        cuenta.estado = 'pagada'

    cuenta.save()

    


