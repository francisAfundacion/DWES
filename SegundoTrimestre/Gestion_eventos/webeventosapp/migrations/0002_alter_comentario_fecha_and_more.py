# Generated by Django 5.1.5 on 2025-01-18 17:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webeventosapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 18, 18, 16, 44, 851063)),
        ),
        migrations.AlterField(
            model_name='usuariopersonalizado',
            name='biografia',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
