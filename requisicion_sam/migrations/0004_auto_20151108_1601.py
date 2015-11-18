# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requisicion_sam', '0003_auto_20151108_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisicion',
            name='profesor',
            field=models.ForeignKey(to='configuracion_sam.Profesor'),
            preserve_default=True,
        ),
    ]
