# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion_sam', '__first__'),
        ('requisicion_sam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requisicion',
            name='carga_horario',
        ),
        migrations.AddField(
            model_name='requisicion',
            name='periodo_lectivo',
            field=models.ForeignKey(default=1, to='configuracion_sam.Carga_Horario'),
            preserve_default=False,
        ),
    ]
