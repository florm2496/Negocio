from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields import BooleanField



class Productos(models.Model):
    rubro = [
        ('ELECTRODOMESTICOS', 'Electrodomesticos'),
        ('INDUMENTARIA', 'Indumentaria'),
        ('BAZAR', 'Bazar'),
        ('REGALERIA', 'Regaleria'),
   
    ]

    nombre = models.CharField(max_length=50)
    codigo = models.IntegerField()
    stock  = models.IntegerField()
    precio = models.FloatField()
    tipo = models.CharField(choices=rubro,max_length=30)
    estado=models.BooleanField(default=True)

    class Meta:
        

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre



