# Generated by Django 3.2.5 on 2021-09-09 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0011_alter_cuentas_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentas',
            name='fecha',
            field=models.DateField(verbose_name='Fecha y hora'),
        ),
    ]