# Generated by Django 5.1.5 on 2025-01-20 09:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webeventosapp', '0006_evento_url_img_alter_comentario_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 20, 10, 4, 20, 262567)),
        ),
        migrations.AlterField(
            model_name='evento',
            name='url_img',
            field=models.URLField(blank=True, max_length=350, null=True),
        ),
    ]
