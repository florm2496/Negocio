# Generated by Django 3.2.5 on 2021-09-06 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='tipo',
            field=models.CharField(choices=[('ELECTRODOMESTICOS', 'Electrodomesticos'), ('INDUMENTARIA', 'Indumentaria'), ('BAZAR', 'Bazar'), ('REGALERIA', 'Regaleria')], max_length=30),
        ),
    ]