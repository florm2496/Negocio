from django.db import models
from applications.base.models import CommonFields

class Domicilio(models.Model):
    direccion=models.CharField( max_length=50)
    localidad=models.CharField(max_length=50)
    codigo_postal=models.CharField(max_length=10)
    
# Create your models here.
class Clientes(CommonFields):
    
  
    nombre= models.CharField(max_length=60,verbose_name="Nombre")
    apellido= models.CharField(max_length=60,verbose_name="Apellido")
    referente= models.CharField(max_length=60,verbose_name="Referente",blank=True,null=True)
    numero_cliente=models.CharField(max_length=20,default=0)
    email=models.EmailField(blank=True,null=True)
    fecha_nacimiento=models.DateField(blank=True,null=True)
    lugar_trabajo=models.CharField(max_length=60,blank=True,null=True)
    dni=models.CharField(max_length=9,verbose_name="DNI", unique=True)
    domicilio=models.ForeignKey(Domicilio,on_delete=models.CASCADE,blank=True,null=True)
    edad=models.IntegerField(default=0,blank=True,null=True)
    telefono=models.CharField(max_length=30,verbose_name="Telefono",blank=True,null=True)
    sueldo=models.CharField(max_length=30,verbose_name="Sueldo",blank=True,null=True)
    boleta_sueldo=models.CharField(max_length=30,verbose_name="Numero de boleta de sueldo",blank=True,null=True)

    class Meta:
        unique_together = ['dni','apellido']
        # ordering = ['apellido']
    def __str__(self):
        
        return '{}-{}'.format(self.apellido,self.dni)
    