from email.policy import default
from django.db import models

# Create your models here.
class CommonFields(models.Model):

    activo = models.BooleanField(default=True)

    class Meta:

        abstract=True


class Configuraciones(models.Model):

    recargo_interes = models.IntegerField(default=0)
    dias_regalia = models.IntegerField(default=0)
    password_utilidades = models.CharField(max_length=20 , default=' ')


    def __str__(self):
        return f'Configuraciones'

