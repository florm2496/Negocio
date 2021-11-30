# Generated by Django 3.2.5 on 2021-11-13 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_auto_20211113_1544'),
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentas',
            name='garante',
        ),
        migrations.RemoveField(
            model_name='cuentas',
            name='solicitante',
        ),
        migrations.AddField(
            model_name='cuentas',
            name='cliente',
            field=models.ManyToManyField(to='clientes.Clientes'),
        ),
    ]
