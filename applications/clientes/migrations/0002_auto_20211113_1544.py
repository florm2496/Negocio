# Generated by Django 3.2.5 on 2021-11-13 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='tipo',
        ),
        migrations.AddField(
            model_name='clientes',
            name='garante',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clientes',
            name='solicitante',
            field=models.BooleanField(default=False),
        ),
    ]
