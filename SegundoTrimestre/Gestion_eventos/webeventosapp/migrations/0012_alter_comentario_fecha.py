# Generated by Django 5.1.5 on 2025-02-10 19:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webeventosapp', '0011_alter_comentario_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 10, 20, 34, 45, 818164)),
        ),
    ]
