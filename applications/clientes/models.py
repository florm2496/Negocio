from django.db import models

# Create your models here.
class Clientes(models.Model):
    nombre= models.CharField(max_length=60,verbose_name="Nombre")
    apellido= models.CharField(max_length=60,verbose_name="Apellido")
    dni=models.PositiveIntegerField(("DNI"))
    direccion=models.CharField(("Direccion"), max_length=50)
    telefono=models.PositiveIntegerField(("Telefono"))
    sueldo=models.FloatField(("Sueldo"))
    boleta_sueldo=models.PositiveIntegerField(("Numero de boleta de sueldo"))

    def __str__(self):
        
        return self.nombre
    