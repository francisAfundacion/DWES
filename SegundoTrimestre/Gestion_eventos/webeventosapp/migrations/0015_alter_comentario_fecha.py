# Generated by Django 5.1.5 on 2025-02-10 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webeventosapp', '0014_alter_comentario_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 10, 22, 34, 59, 323910)),
        ),
    ]
