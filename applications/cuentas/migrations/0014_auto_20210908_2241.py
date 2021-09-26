# Generated by Django 3.2.5 on 2021-09-09 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_clientes_tipo'),
        ('cuentas', '0013_alter_cuotas_fecha_vencimiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentas',
            name='cliente',
        ),
        migrations.AddField(
            model_name='cuentas',
            name='solicitante',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='solicitante', to='clientes.clientes'),
        ),
        migrations.AddField(
            model_name='detallecuenta',
            name='descuento',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='cuentas',
            name='estado',
            field=models.CharField(choices=[('activa', 'activa'), ('morosa', 'morosa'), ('inactiva', 'inactiva')], default='activa', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='cuentas',
            name='fecha',
            field=models.DateField(verbose_name='Fecha y hora de la venta'),
        ),
        migrations.AlterField(
            model_name='cuotas',
            name='estado',
            field=models.CharField(choices=[('impaga', 'impaga'), ('vencida', 'vencida'), ('pagada', 'pagada')], default='impaga', max_length=20, verbose_name='Estado de la cuota'),
        ),
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importe', models.FloatField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('metodo_pago', models.CharField(choices=[('contado', 'contado'), ('tarjeta', 'tarjeta')], default='contado', max_length=20)),
                ('cuota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuentas.cuotas')),
            ],
        ),
    ]
