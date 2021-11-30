from django.db import models


class Domicilio(models.Model):
    direccion=models.CharField( max_length=50)
    localidad=models.CharField(max_length=50)
    codigo_postal=models.CharField(max_length=10)
    
# Create your models here.
class Clientes(models.Model):
    
  
    nombre= models.CharField(max_length=60,verbose_name="Nombre")
    apellido= models.CharField(max_length=60,verbose_name="Apellido")
    referente= models.CharField(max_length=60,verbose_name="Referente",default='')
    numero_cliente=models.CharField(max_length=20,default=0)
    email=models.EmailField(blank=True,null=True)
    fecha_nacimiento=models.DateField(blank=True,null=True)
    lugar_trabajo=models.CharField(max_length=60,blank=True,null=True)
    dni=models.CharField(max_length=9,verbose_name="DNI", unique=True)
    garante=models.BooleanField(default=False)
    solicitante=models.BooleanField(default=False)
    domicilio=models.ForeignKey(Domicilio,on_delete=models.CASCADE,blank=True,null=True)
    edad=models.IntegerField(default=0)
    telefono=models.CharField(max_length=30,verbose_name="Telefono")
    sueldo=models.CharField(max_length=30,verbose_name="Sueldo")
    boleta_sueldo=models.CharField(max_length=30,verbose_name="Numero de boleta de sueldo")

    class Meta:
        unique_together = ['dni','apellido']
        ordering = ['apellido']
    def __str__(self):
        
        return '{}-{}'.format(self.apellido,self.dni)
    