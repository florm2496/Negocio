from django.db import models

# Create your models here.
class Clientes(models.Model):
    
    tipos=[
        ('garante','garante'),
        ('solicitante','solicitante'),
    ]
    nombre= models.CharField(max_length=60,verbose_name="Nombre")
    apellido= models.CharField(max_length=60,verbose_name="Apellido")
    dni=models.CharField(max_length=9,verbose_name="DNI", unique=True)
    tipo=models.CharField(choices=tipos , default="solicitante",max_length=15)
    direccion=models.CharField(verbose_name="Direccion", max_length=50)
    telefono=models.CharField(max_length=30,verbose_name="Telefono")
    sueldo=models.CharField(max_length=30,verbose_name="Sueldo")
    boleta_sueldo=models.CharField(max_length=30,verbose_name="Numero de boleta de sueldo")

    class Meta:
        unique_together = ['dni','apellido']
        ordering = ['apellido']
    def __str__(self):
        
        return '{}-{}'.format(self.apellido,self.dni)
    