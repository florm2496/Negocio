# Generated by Django 3.2.5 on 2021-09-02 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
        ('cuentas', '0005_alter_cuentas_saldo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuotas',
            name='productos',
            field=models.ManyToManyField(blank=True, null=True, to='productos.Productos'),
        ),
        migrations.DeleteModel(
            name='Pagos',
        ),
    ]