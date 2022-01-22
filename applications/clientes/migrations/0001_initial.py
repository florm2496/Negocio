# Generated by Django 3.2.5 on 2022-01-18 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=50)),
                ('localidad', models.CharField(max_length=50)),
                ('codigo_postal', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(default=True)),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=60, verbose_name='Apellido')),
                ('referente', models.CharField(default='', max_length=60, verbose_name='Referente')),
                ('numero_cliente', models.CharField(default=0, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('lugar_trabajo', models.CharField(blank=True, max_length=60, null=True)),
                ('dni', models.CharField(max_length=9, unique=True, verbose_name='DNI')),
                ('edad', models.IntegerField(default=0)),
                ('telefono', models.CharField(max_length=30, verbose_name='Telefono')),
                ('sueldo', models.CharField(max_length=30, verbose_name='Sueldo')),
                ('boleta_sueldo', models.CharField(max_length=30, verbose_name='Numero de boleta de sueldo')),
                ('domicilio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clientes.domicilio')),
            ],
            options={
                'ordering': ['apellido'],
                'unique_together': {('dni', 'apellido')},
            },
        ),
    ]
