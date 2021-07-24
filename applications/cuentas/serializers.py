from rest_framework import serializers
from .models import Cuentas

class cuentasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cuentas
        fields='__all__'
