# Generated by Django 3.2.5 on 2021-11-15 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0006_clientes_numero_cliente'),
        ('cuentas', '0002_auto_20211113_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentas',
            name='cliente',
        ),
        migrations.AddField(
            model_name='cuentas',
            name='garante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_garante', to='clientes.clientes'),
        ),
        migrations.AddField(
            model_name='cuentas',
            name='solicitante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_solicitante', to='clientes.clientes'),
        ),
        migrations.AlterField(
            model_name='cuentas',
            name='estado',
            field=models.CharField(choices=[('activa', 'activa'), ('morosa', 'morosa'), ('inactiva', 'inactiva'), ('pagada', 'cancelada'), ('refinanciada', 'refinanciada')], default='activa', max_length=20, verbose_name='Estado'),
        ),
    ]
