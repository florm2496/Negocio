from django.db import models




class Productos(models.Model):
    rubro = [
        ('ELECTRODOMESTICOS', 'ELECTRODOMESTICOS'),
        ('INDUMENTARIA', 'INDUMENTARIA'),
        ('BAZAR', 'BAZAR'),
        ('REGALERIA', 'REGALERIA'),
   
    ]

    nombre = models.CharField(max_length=50)
    codigo = models.IntegerField()
    codigo_ref = models.CharField(default="A" , max_length=10)
    stock  = models.IntegerField(default=0)
    precio = models.FloatField()
    tipo = models.CharField(choices=rubro,max_length=30)
    estado=models.BooleanField(default=True)

    class Meta:

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre




class Ingresos(models.Model):
    numero=models.IntegerField(default=0)
    fecha=models.DateField()
    total=models.FloatField()
    observacion=models.CharField(max_length=100)


    def __str__(self):
        return str(self.id)

class DetalleIngreso(models.Model):
    numero=models.IntegerField(default=0)
    ingreso=models.ForeignKey(Ingresos ,null=True, on_delete=models.SET_NULL)
    producto=models.ForeignKey(Productos,on_delete=models.CASCADE)
    cantidad=models.FloatField()
    subtotal=models.FloatField()

    def __str__(self):
        return '{} {}'.format(self.ingreso , self.producto)

