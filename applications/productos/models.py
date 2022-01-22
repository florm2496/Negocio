from email.policy import default
from django.db import models
from applications.base.models import CommonFields




class Rubros(CommonFields):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Rubro'
        verbose_name_plural = 'Rubros'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Rubros, self).save(*args, **kwargs)




class Productos(CommonFields):


    nombre = models.CharField(max_length=50)
    codigo = models.CharField(unique=True,max_length=10)
    codigo_ref = models.CharField(max_length=10)
    stock  = models.IntegerField(default=0)
    precio = models.FloatField(default=0)
    rubro = models.ForeignKey(Rubros, on_delete=models.CASCADE)
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

