# Generated by Django 3.2.5 on 2021-08-28 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0003_alter_cuentas_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentas',
            name='productos',
        ),
    ]
